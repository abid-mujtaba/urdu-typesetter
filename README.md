# Urdu Typesetting

This repo implements a toolchain for typesetting Urdu literature.
It is designed around an explicit separation of content, formatting, and templates.

The user supplies the text and metadata for a piece of literature in a yaml file.
A minimal set of formatting information can also be provided.
This is mostly relevant for poetry where the width of each `misra` and
the vertical separation between `shair` (or stanzas)
is of critical importance.

## Sample Config

Here is the config and source structure required to produce artifacts for
Faiz Ahmed Faiz's famous poem *kutay*:

### `format.yaml`

``` yaml
poetry:
  pdf:
    width: 0.45
    separation: 0.8
```

### `source.yaml`

``` yaml
category: poetry
title: کتے
author: فیض احمد فیض
date: 1941
description: Published in Faiz's first book "Naqsh-e-Faryadi"
text:
  -
    - یہ گلیوں کے آوارہ بیکار کتے
    - کہ بخشا گیا جن کو ذوقِ گدائی
    - زمانے کی پھٹکار سرمایہ اِن کا
    - جہاں بھر کی دھتکار اِن کی کمائی
  -
    - نہ آرام شب کو نہ راحت سویرے
    - غلاظت میں گھر، نالیوں میں بسیرے
    - جو بِگڑیں تو ایک دوسرے سے لڑا دو
    - ذرا ایک روٹی کا ٹکڑا دکھا دو
    - یہ ہر ایک کی ٹھوکریں کھانے والے
    - یہ فاقوں سے اُکتا کے مر جانے والے
  -
    - یہ مظلوم مخلوق گر سر اٹھائے
    - تو انسان سب سرکشی بھول جائے
    - یہ چاہیں تو دنیا کو اپنا بنا لیں
    - یہ آقاؤں کی ہڈّیاں تک چبا لیں
    - کوئی ان کو احساسِ ذِلّت دلا دے
    - کوئی اِن کی سوئی ہوئی دم ہلا دے
```

## Examples

The artifacts produced by the source above can be found [here](https://abid-mujtaba.github.io/urdu-typesetter/).

This link contains many example of rendered Urdu literature.

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
