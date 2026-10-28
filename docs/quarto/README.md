# CS00 course website

The site is built with [Quarto](https://quarto.org/) and structured like the Stanford CS231n course page.

Pages:

- `index.qmd`: course overview, announcements, grading
- `schedule.qmd`: weekly schedule
- `syllabus.qmd`: policies and workload
- `assignments.qmd`: homework and final project
- `resources.qmd`: setup and learning materials
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
