# Quarto Scripts

## Troubleshooting

### Math displays as raw delimiters

> If inline math appears as literal `\( ... \)` in a Quarto HTML page, inspect the browser console for MathJax initialization errors.

Plotly's notebook HTML output can inject MathJax 3, which conflicts with Quarto's MathJax 4.
The `plotly_mimetype` renderer is not supported by Quarto HTML and can produce an "Unable to display output" message.
Render the figure as HTML with Plotly's MathJax injection disabled:

```python
from IPython.display import HTML, display

display(HTML(figure.to_html(full_html=False, include_plotlyjs="cdn", include_mathjax=False)))
```

This keeps the Plotly figure interactive without adding a conflicting MathJax script.
After changing the renderer, rerender the page and reload the preview.
