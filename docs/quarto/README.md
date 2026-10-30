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

## Publishing

The site is published at <https://sgo-go.github.io/cs00/>.
The [publish-site workflow](../../.github/workflows/publish-site.yml) deploys it to GitHub Pages.
One-time setup: open the [Pages settings](https://github.com/SGo-Go/cs00/settings/pages) and set **Source** to **GitHub Actions**.
