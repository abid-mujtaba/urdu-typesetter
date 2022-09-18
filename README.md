# Urdu Typesetting

This repo implements a toolchain for typesetting Urdu literature.
It is designed around an explicit separation of content, formatting, and templates.

The user supplies the text and metadata for a piece of literature in a yaml file.
A minimal set of formatting information can also be provided.
This is mostly relevant for poetry where the width of each `misra` and
the vertical separation between `shair` (or stanzas)
is of critical importance.

## Sample Config

## Examples

## Usage

### Build artifacts

- pdf: `./toolchain/urdu-builder build --format=pdf <path-to-source-folder>
- html: `./toolchain/urdu-builder build --format=html <path-to-source-folder>
- epub: `./toolchain/urdu-builder build --format=epub <path-to-source-folder>

### Live Preview of HTML

There is a live reloadable preview available which helps edit the source.
With the preview open in a browser (Chrome is preferable),
every time you modify and save the `source.yaml` or `format.yaml` file,
the HTML artifact will be re-built and
the tab will refresh automatically in the browser.

To preview: `./toolchain/urdu-builder preview <path-to-source-folder>`

## Local Development

To re-build the image: `docker build -t urdu-typesetter .`
