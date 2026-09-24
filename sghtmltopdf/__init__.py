from __future__ import annotations

from typing import Any

from . import _sghtmltopdf
from .options import to_argv

__version__ = "0.1.1"


def render(html: str | bytes, **options: Any) -> bytes:
    """Render HTML to PDF bytes.

    Args:
        html: HTML content as str or bytes.
        **options: Conversion options (e.g. page_size="A4", landscape=True, grayscale=True, font="...").

    Returns:
        PDF data as bytes.
    """
    if isinstance(html, str):
        html_bytes = html.encode("utf-8")
    elif isinstance(html, (bytes, bytearray, memoryview)):
        html_bytes = bytes(html)
    else:
        raise TypeError(f"html must be str or bytes, not {type(html).__name__}")

    argv = to_argv(options)
    return _sghtmltopdf.render(html_bytes, argv)


__all__ = ["render", "__version__"]
