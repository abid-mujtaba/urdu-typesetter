"""Read yaml source file and fetch data."""

from pathlib import Path
from typing import Any, Dict

from ruyaml import YAML


Data = Dict[str, Any]


def read(source_dir: Path) -> Data:
    """Read yaml data from source."""
    return _read(source_dir / "story.yaml")


def _read(source_file: Path) -> Data:
    """Read yaml data from source file."""
    yaml = YAML(typ="safe")

    with source_file.open(encoding="UTF-8") as fin:
        data = yaml.load(fin)

    _validate_story(data)
    return data


def _validate_story(data: Data) -> None:
    """Validate story data."""
    # Validate data
    assert "title" in data
    assert "author" in data
    assert "date" in data
    assert "description" in data
    assert "story" in data

    assert isinstance(data["story"], list)

    for line in data["story"]:
        assert isinstance(line, str)

    return data
