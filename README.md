# sghtmltopdf

A Python binding for [sghtmltopdf](https://github.com/waka/sghtmltopdf), converting HTML to PDF using Servo's layout and rendering components.

## Requirements

- Python >= 3.10
- Rust toolchain (for building from source)

## Installation

```bash
pip install sghtmltopdf
```

## Usage

```python
import sghtmltopdf

html = "<html><body><h1>Hello, World!</h1><p>Generate PDF from HTML with Servo engine.</p></body></html>"
pdf_bytes = sghtmltopdf.render(html)

with open("output.pdf", "wb") as f:
    f.write(pdf_bytes)
```

### In-memory rendering with CSS and images (no filesystem dependency)

You can pass `bytes` directly and embed styles/images in-memory using `data:` URLs or inline tags without touching the filesystem:

```python
import base64
import sghtmltopdf

# 1. In-memory HTML & CSS (via <style> tag or <link>)
css_bytes = b"h1 { color: #0066cc; } p { font-size: 14px; }"
css_b64 = base64.b64encode(css_bytes).decode("ascii")

# 2. In-memory image (via data: URL)
image_bytes = b"..."  # PNG/JPEG bytes
img_b64 = base64.b64encode(image_bytes).decode("ascii")

html_bytes = f"""<!DOCTYPE html>
<html>
<head>
  <!-- <link> with data: URL -->
  <link rel="stylesheet" href="data:text/css;base64,{css_b64}">
  <!-- or inline <style>: <style>{css_bytes.decode('utf-8')}</style> -->
</head>
<body>
  <h1>Title</h1>
  <p>Hello from in-memory HTML!</p>
  <img src="data:image/png;base64,{img_b64}">
</body>
</html>""".encode("utf-8")

pdf_bytes = sghtmltopdf.render(html_bytes)
```

### Rendering with local assets

To allow loading local resources (e.g. images, stylesheets) from specified directories:

```python
import sghtmltopdf

html = '<html><head><link rel="stylesheet" href="/path/to/assets/style.css"></head><body><img src="/path/to/assets/logo.png"></body></html>'
pdf_bytes = sghtmltopdf.render(
    html,
    allow_path="/path/to/assets",  # Pass a list for multiple paths: ["/path/to/assets", "/path/to/fonts"]
)
```

### Rendering with remote assets (HTTP/HTTPS)

To allow fetching remote resources such as images or stylesheets via HTTP/HTTPS:

```python
import sghtmltopdf

html = '<html><body><img src="https://example.com/logo.png"></body></html>'
pdf_bytes = sghtmltopdf.render(html, allow_remote_assets=True)
```

### Options

Supported options correspond to `sghtmltopdf` CLI arguments:

- `page_size`: `"A4"`, `"A3"`, `"A5"`, `"Letter"`, `"Legal"`
- `orientation`: `"Portrait"`, `"Landscape"`
- `page_width`: e.g. `"210mm"`
- `page_height`: e.g. `"297mm"`
- `margin_top`, `margin_bottom`, `margin_left`, `margin_right`: e.g. `"10mm"`, `"1in"`
- `grayscale`: `True` / `False`
- `dpi`: e.g. `96.0`
- `zoom`: e.g. `1.0`
- `title`, `author`, `subject`, `keywords`: PDF metadata strings
- `font`: Font path or list of font paths/dicts (e.g. `font="font.ttf"` or `font={"path": "font.ttc", "index": 1}`)
- `header_left`, `header_center`, `header_right`: Header text (supports `[page]`, `[topage]`)
- `footer_left`, `footer_center`, `footer_right`: Footer text
- `toc`: `True` to insert a table of contents before the document body
- `allow` / `allow_path`: Allowed directory paths for local resources

## Testing

```bash
pip install -e .
pytest
```

## License

MIT License
