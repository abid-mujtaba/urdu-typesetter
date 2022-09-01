"""Read yaml source file and fetch data."""

from pathlib import Path
from typing import Any, Dict

from ruyaml import YAML


Data = Dict[str, Any]


def read(source_dir: Path) -> Data:
    """Read yaml data from source."""
    return _read(source_dir / "source.yaml")


def artifact_name(source: Path) -> str:
    """Read the name of the folder containing source.yaml; this is the artifact name."""
    return str(source.relative_to(source.parent))


def _read(source_file: Path) -> Data:
    """Read yaml data from source file."""
    yaml = YAML(typ="safe")

    with source_file.open(encoding="UTF-8") as fin:
        data = yaml.load(fin)

    _validate_source(data)
    return data


def _validate_source(data: Data) -> None:
    """Validate source data."""
    assert "category" in data
    category = data["category"]
    assert category in ("prose", "poetry")

    assert "title" in data
    assert "author" in data
    assert "date" in data
    assert "description" in data
    assert "text" in data

    assert isinstance(data["text"], list)

    if category == "prose":
        for line in data["text"]:
            assert isinstance(line, str)

    elif category == "poetry":
        for section in data["text"]:
            assert isinstance(section, list)

            for line in section:
                assert isinstance(line, str)
