.DEFAULT_GOAL := help
PORT ?= 0 # The port to serve the Quarto site on, default is 0 (random port)
LECTURE_01_VIDEO_SCENES := BinaryCounting FloatingPoint IntegerModuloCircle

.PHONY: help install render render-videos preview serve sphinx-render sphinx-open

help:
	@printf '%s\n' 'Available targets:' '  make install          Install system and Python docs/visuals dependencies' '  make render           Render videos and the Quarto site' '  make render-videos    Render the lecture 1 MP4s' '  make preview          Preview the Quarto site' '  make serve            Serve the rendered Quarto site on a random HTTP port' '  make sphinx-render    Build the Sphinx API docs' '  make sphinx-open      Build and open the Sphinx API docs'

install:
	sudo apt-get update
	sudo apt-get install -y --no-install-recommends libcairo2-dev libpango1.0-dev pkg-config unzip
	uv sync --group docs --group visuals

render: render-videos
	cd docs/quarto && quarto render

render-videos:
	uv run --group visuals python -m cs00_visuals.render --quality web --only $(LECTURE_01_VIDEO_SCENES) --movie-only

preview:
	cd docs/quarto && quarto preview

serve: # render
	python3 -m http.server --bind 127.0.0.1 --directory docs/quarto/_site "$(PORT)"

sphinx-render:
	LC_ALL=C.UTF-8 uv run --no-sync sphinx-build -W -b html docs/sphinx docs/quarto/_site/api

sphinx-open: sphinx-render
	@test -n "$$BROWSER" || { printf '%s\n' 'Set BROWSER to open the generated Sphinx index.'; exit 1; }
	"$$BROWSER" "file://$(CURDIR)/docs/quarto/_site/api/index.html"

