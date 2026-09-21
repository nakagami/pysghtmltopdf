from __future__ import annotations

from typing import Any

ALIAS_KEYS = {
    "allow": "allow_path",
    "allow_paths": "allow_path",
    "user_stylesheets": "user_style_sheet",
    "user_style_sheets": "user_style_sheet",
}

FONT_FLAGS = {
    "font",
    "gothic-font",
    "serif-font",
    "mono-font",
}


def canonical_key(key: str) -> str:
    return ALIAS_KEYS.get(key, key)


def flag_name(key: str) -> str:
    return key.replace("_", "-")


def _font_pairs(name: str, value: Any) -> list[tuple[str, str | None]]:
    if value is None or value is False:
        return []
    if isinstance(value, (list, tuple)):
        pairs = []
        for elem in value:
            pairs.extend(_font_pairs(name, elem))
        return pairs
    if isinstance(value, dict):
        path = value.get("path")
        if path is None:
            raise ValueError(f"{name} dict requires 'path': {value}")
        index = value.get("index")
        pairs = [(name, str(path))]
        if index is not None:
            pairs.append((f"{name}-index", str(index)))
        return pairs
    return [(name, str(value))]


def _replace_pairs(value: Any) -> list[tuple[str, str | None]]:
    if value is None or value is False:
        return []
    if isinstance(value, dict):
        return [("replace", f"{k}={v}") for k, v in value.items()]
    if isinstance(value, (list, tuple)):
        if (
            len(value) == 2
            and not isinstance(value[0], (list, tuple, dict))
            and not (isinstance(value[0], str) and "=" in value[0])
        ):
            return [("replace", f"{value[0]}={value[1]}")]
        pairs = []
        for elem in value:
            pairs.extend(_replace_pairs(elem))
        return pairs
    return [("replace", str(value))]


def _pairs_for(key: str, value: Any) -> list[tuple[str, str | None]]:
    name = flag_name(key)
    if name in FONT_FLAGS:
        return _font_pairs(name, value)
    if name == "replace":
        return _replace_pairs(value)
    if name == "landscape":
        if value is True:
            return [("orientation", "Landscape")]
        elif value is False:
            return [("orientation", "Portrait")]
        return []
    if name == "portrait":
        if value is True:
            return [("orientation", "Portrait")]
        elif value is False:
            return [("orientation", "Landscape")]
        return []

    if value is None or value is False:
        return []
    if value is True:
        return [(name, None)]
    if isinstance(value, (list, tuple)):
        pairs = []
        for elem in value:
            pairs.extend(_pairs_for(key, elem))
        return pairs
    if isinstance(value, dict):
        raise ValueError(
            f"Cannot pass dict to {key}. Use flattened options instead."
        )
    return [(name, str(value))]


def to_argv(options: dict[str, Any]) -> list[str]:
    argv: list[str] = []
    for key, value in options.items():
        key = canonical_key(key)
        for name, arg in _pairs_for(key, value):
            argv.append(f"--{name}")
            if arg is not None:
                argv.append(arg)
    return argv

