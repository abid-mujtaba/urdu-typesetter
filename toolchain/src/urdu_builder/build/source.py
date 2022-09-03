"""Read yaml source file and fetch data."""

from datetime import date
from pathlib import Path
from typing import Any, Dict

from ruyaml import YAML
from schema import Or, Regex, Schema
from schema import Optional as SOptional


Data = Dict[str, Any]


def read_source(source_dir: Path) -> Data:
    """Read yaml data from source."""
    data = _read_file(source_dir / "source.yaml")
    _validate_source(data)
    return data


def read_format(source_dir: Path) -> Data:
    """Read yaml data from format.yaml."""
    format_file = source_dir / "format.yaml"

    if format_file.exists():
        data = _read_file(source_dir / "format.yaml")
    else:
        data = {}

    return _validate_format(data)


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
        "category": Or("prose", "poetry"),
        "title": str,
        "author": str,
        SOptional("date", default=""): Or(date, int),
        SOptional("description", default=""): str,
        "text": object,
    }

    Schema(core).validate(data)

    text = data["text"]

    if "category" == "prose":
        Schema([str]).validate(text)

    if "category" == "poetry":
        Schema([[str]]).validate(text)


def _validate_format(data: Data) -> Data:
    """Validate format data."""
    # The pdf width is the factor multiplied by \textwidth to constrain each misra
    # The pdf separation is the factor multiplied by \baselineskip to vertically
    # separate the shair or bund (stanzas)
    pdf_default = {"width": 0.5, "separation": 0.5}
    poetry_default = {"pdf": pdf_default}

    pdf = {
        SOptional("pdf", default=pdf_default): {
            SOptional("width", default=pdf_default["width"]): float,
            SOptional("separation", default=pdf_default["separation"]): float,
        }
    }
    html = {SOptional("html"): {"width": Regex(r"\d+(em|px)")}}

    schema = {SOptional("poetry", default=poetry_default): {**html, **pdf}}

    return Schema(schema).validate(data)
