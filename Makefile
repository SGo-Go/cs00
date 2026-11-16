.DEFAULT_GOAL := help

.PHONY: help render preview sphinx-render sphinx-open

help:
	@printf '%s\n' 'Available targets:' '  make render        Render the Quarto site' '  make preview       Preview the Quarto site' '  make sphinx-render Build the Sphinx API docs' '  make sphinx-open   Build and open the Sphinx API docs'

render:
	cd docs/quarto && quarto render

preview:
	cd docs/quarto && quarto preview

sphinx-render:
	LC_ALL=C.UTF-8 uv run --no-sync sphinx-build -W -b html docs/sphinx docs/quarto/_site/api

sphinx-open: sphinx-render
	@test -n "$$BROWSER" || { printf '%s\n' 'Set BROWSER to open the generated Sphinx index.'; exit 1; }
	"$$BROWSER" "file://$(CURDIR)/docs/quarto/_site/api/index.html"
