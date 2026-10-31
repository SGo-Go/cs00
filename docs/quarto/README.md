# CS00 course website

The site is built with [Quarto](https://quarto.org/) and structured like the Stanford CS231n course page.

Pages:

- `index.qmd`: course overview, announcements, grading
- `schedule.qmd`: weekly schedule
- `syllabus.qmd`: policies and workload
- `assignments.qmd`: homework and final project
- `resources.qmd`: setup and learning materials
- `glossary.qmd`: course terms, linked from the other pages
- `staff.qmd`: teaching staff and office hours

Run the commands from the repository root.
The path argument is relative to the current directory, so `quarto render docs/quarto` fails with `No valid input files passed to render` anywhere else.
Inside `docs/quarto/`, run `quarto render` and `quarto preview` without an argument.

Preview with live reload:

```sh
quarto preview docs/quarto
```

Render to `docs/quarto/_site`:

```sh
quarto render docs/quarto
```

Each lecture in `lectures/` is also rendered to a separate PDF with [Typst](https://typst.app/), which is bundled with Quarto.
Formats are set in `lectures/_metadata.yml`, and the PDFs are written next to the HTML pages, for example `_site/lectures/01-data-encoding.pdf`.
`quarto preview` shows only the HTML, so run `quarto render` to build the PDFs.
Each lecture page links to its PDF in the sidebar, and the schedule links to it too.

## Publishing

The site is published at <https://sgo-go.github.io/cs00/>.
The [publish-site workflow](../../.github/workflows/publish-site.yml) deploys it to GitHub Pages.
It also builds the Sphinx API reference from `docs/sphinx` and publishes it at <https://sgo-go.github.io/cs00/api/>.
GitHub Pages serves one site per repository, so both are deployed together in a single artifact.
One-time setup: open the [Pages settings](https://github.com/SGo-Go/cs00/settings/pages) and set **Source** to **GitHub Actions**.
