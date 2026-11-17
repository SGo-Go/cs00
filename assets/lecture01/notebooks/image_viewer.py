# Copyright (C) 2026 SGo-Go. All rights reserved.
# /// script
# requires-python = ">=3.12"
# dependencies = ["marimo>=0.25.2", "pillow>=12"]
# ///
"""Explore RGB and grayscale pixels with Pillow and native Marimo controls."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full")

with app.setup(hide_code=True):
    import html
    from io import BytesIO
    from typing import NamedTuple

    import marimo as mo
    from PIL import Image, ImageDraw, ImageOps, UnidentifiedImageError

    class PixelRegion(NamedTuple):
        """A selected crop and its byte offsets in the decoded source image."""

        x: int
        y: int
        pixels: Image.Image
        hex_dump: str


@app.function
def load_image(contents: bytes) -> Image.Image:
    """Decode an uploaded image, applying orientation and bounding memory use."""
    with Image.open(BytesIO(contents)) as opened:
        if opened.width * opened.height > 16_000_000:
            raise ValueError("Максимальна роздільність — 16 МП.")
        opened.load()
        oriented = ImageOps.exif_transpose(opened)
        return oriented.convert("L" if oriented.mode in {"1", "L", "LA"} else "RGB")


@app.function
def sample_image(mode: str = "RGB") -> Image.Image:
    """Create a small sample with known channel values."""
    sample = Image.new("RGB", (16, 12))
    sample.putdata([(column * 17, row * 23, 128) for row in range(12) for column in range(16)])
    return sample.convert(mode)


@app.function
def inspect_region(image: Image.Image, start_x: int, start_y: int, size: int) -> PixelRegion:
    """Extract a bounded region and hex rows with full decoded-image offsets."""
    if image.mode not in {"RGB", "L"}:
        raise ValueError("Expected an 8-bit RGB or grayscale image.")
    origin_x = min(max(int(start_x), 0), image.width - 1)
    origin_y = min(max(int(start_y), 0), image.height - 1)
    side = min(max(int(size), 1), 16)
    crop = image.crop((origin_x, origin_y, min(origin_x + side, image.width), min(origin_y + side, image.height)))
    channels = len(image.getbands())
    raw = crop.tobytes()
    row_bytes = crop.width * channels
    rows = []
    for row_index in range(crop.height):
        row = raw[row_index * row_bytes : (row_index + 1) * row_bytes]
        pixels = [row[index : index + channels].hex(" ").upper() for index in range(0, len(row), channels)]
        offset = ((origin_y + row_index) * image.width + origin_x) * channels
        rows.append(f"{offset:08X}  {' | '.join(pixels)}")
    return PixelRegion(origin_x, origin_y, crop, "\n".join(rows))


@app.function
def magnify_pixels(image: Image.Image, scale: int) -> Image.Image:
    """Enlarge a bounded pixel region without interpolating colors."""
    factor = min(max(int(scale), 1), 32)
    return image.resize((image.width * factor, image.height * factor), resample=Image.Resampling.NEAREST)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Пікселі та байти зображення
    """)
    return


@app.cell(hide_code=True)
def _():
    upload = mo.ui.file(kind="area", label="Відкрити або перетягнути зображення", max_size=100_000_000)
    sample_mode = mo.ui.dropdown(
        options={"Зразок RGB": "RGB", "Зразок сірого": "L"}, value="Зразок RGB", label="Без завантаженого файлу"
    )
    mo.vstack([upload, sample_mode])
    return sample_mode, upload


@app.cell(hide_code=True)
def _(sample_mode, upload):
    problem = ""
    source_image = None
    source_name = ""
    try:
        if upload.value:
            source_name = upload.value[0].name
            source_image = load_image(upload.value[0].contents)
        else:
            source_name = "Зразок RGB" if sample_mode.value == "RGB" else "Зразок сірого"
            source_image = sample_image(sample_mode.value)
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as error:
        problem = f"Не вдалося відкрити зображення: {error}"
    mo.stop(source_image is None, mo.callout(mo.md(problem), kind="warn"))
    return source_image, source_name


@app.cell(hide_code=True)
def _():
    channel_mode = mo.ui.dropdown(
        options={"Авто": "auto", "RGB · 3 байти/піксель": "RGB", "Сіре · 1 байт/піксель": "L"},
        value="Авто",
        label="Канали",
    )
    channel_mode
    return (channel_mode,)


@app.cell(hide_code=True)
def _(channel_mode, source_image):
    selected_mode = source_image.mode if channel_mode.value == "auto" else channel_mode.value
    decoded_image = source_image.convert(selected_mode)
    return (decoded_image,)


@app.cell(hide_code=True)
def _(decoded_image):
    origin_x = mo.ui.number(start=0, stop=decoded_image.width - 1, step=1, value=0, label="X")
    origin_y = mo.ui.number(start=0, stop=decoded_image.height - 1, step=1, value=0, label="Y")
    region_size = mo.ui.number(start=1, stop=16, step=1, value=8, label="Сторона ділянки")
    zoom = mo.ui.slider(steps=[1, 2, 4, 8, 16, 32], value=16, show_value=True, label="Масштаб ×")
    mo.vstack([mo.hstack([origin_x, origin_y, region_size], justify="start", wrap=True), zoom])
    return origin_x, origin_y, region_size, zoom


@app.cell(hide_code=True)
def _(decoded_image, origin_x, origin_y, region_size):
    region = inspect_region(decoded_image, int(origin_x.value), int(origin_y.value), int(region_size.value))
    return (region,)


@app.cell(hide_code=True)
def _(decoded_image, region, source_name, zoom):
    overview = decoded_image.convert("RGB")
    drawing = ImageDraw.Draw(overview)
    bounds = (region.x, region.y, region.x + region.pixels.width - 1, region.y + region.pixels.height - 1)
    drawing.rectangle(bounds, outline="#ff00ff", width=1)
    overview_width = max(decoded_image.width, min(decoded_image.width * int(zoom.value), 4096))
    overview_html = mo.image(
        overview,
        alt="Зображення з позначеною ділянкою",
        width=overview_width,
        style={"image-rendering": "pixelated", "max-width": "none", "width": f"{overview_width}px"},
    )
    mo.vstack(
        [
            mo.Html(
                f"<p>{html.escape(source_name)} · {decoded_image.width} × {decoded_image.height} · "
                f"{decoded_image.mode} · {len(decoded_image.getbands()) * 8} біт/піксель</p>"
            ),
            mo.Html(f'<div style="overflow:auto;max-height:360px;max-width:100%">{overview_html.text}</div>'),
        ]
    )
    return


@app.cell(hide_code=True)
def _(region, zoom):
    detail = magnify_pixels(region.pixels, int(zoom.value))
    detail_html = mo.image(
        detail,
        alt="Вибрана ділянка без згладжування",
        width=detail.width,
        style={"image-rendering": "pixelated", "max-width": "none"},
    )
    mo.vstack(
        [
            mo.md(f"### Вибрана ділянка ({region.x}, {region.y}) · {region.pixels.width} × {region.pixels.height}"),
            mo.Html(f'<div style="overflow:auto;max-width:100%">{detail_html.text}</div>'),
            mo.Html(
                f'<pre style="overflow:auto;max-height:360px;padding:12px;background:#f0f5f3;color:#20302b">'
                f"{html.escape(region.hex_dump)}</pre>"
            ),
            mo.md(
                "Hex: декодовані 8-бітові пікселі, не байти стисненого файлу. "
                "RGB: R G B; сіре: L. Альфа-канал не включено. "
                "Зміщення зліва — у декодованому масиві вибраного режиму."
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
