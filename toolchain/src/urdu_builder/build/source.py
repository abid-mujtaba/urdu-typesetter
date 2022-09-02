"""Read yaml source file and fetch data."""

from pathlib import Path
from typing import Any, Dict, Optional

from ruyaml import YAML
from schema import Or, Regex, Schema
from schema import Optional as SOptional


Data = Dict[str, Any]


def read_source(source_dir: Path) -> Data:
    """Read yaml data from source."""
    data = _read_file(source_dir / "source.yaml")
    _validate_source(data)
    return data


def read_format(source_dir: Path) -> Optional[Data]:
    """Read yaml data from format.yaml."""
    format_file = source_dir / "format.yaml"

    if format_file.exists():
        data = _read_file(source_dir / "format.yaml")
        _validate_format(data)
        return data

    return None


def artifact_name(source: Path) -> str:
    """Read the name of the folder containing source.yaml; this is the artifact name."""
    return str(source.relative_to(source.parent))


def _read_file(source_file: Path) -> Data:
    """Read yaml data from source file."""
    yaml = YAML(typ="safe")

    with source_file.open(encoding="UTF-8") as fin:
        data = yaml.load(fin)

    return data


def _validate_source(data: Data) -> None:
    """Validate source data."""
    core = {
        "title": str,
        "author": str,
        SOptional("date", default=""): str,
        SOptional("description", default=""): str,
    }

    prose = {"category": "prose", "text": [str], **core}
    poetry = {"category": "poetry", "text": [[str]], **core}

    schema = Or(prose, poetry)

    validator = Schema(schema)
    validator.validate(data)


def _validate_format(data: Data) -> None:
    """Validate format data."""
    schema = {SOptional("poetry"): {SOptional("html"): {"width": Regex(r"\d+(em|px)")}}}
    validator = Schema(schema)
    validator.validate(data)
