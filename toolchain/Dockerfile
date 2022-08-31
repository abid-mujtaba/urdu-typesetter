FROM python:3.10-slim as py-builder

RUN pip install --upgrade pip
RUN pip install --upgrade build

WORKDIR /work
COPY pyproject.toml src/ /work/

RUN python -m build


FROM texlive/texlive:latest-minimal

LABEL Maintainer Abid H. Mujtaba <abid.naqvi83@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV PACKAGES \
    python3-pip \
    texlive-xetex \
    texlive-lang-arabic

RUN apt-get update \
    && apt-get install -y $PACKAGES \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=py-builder /work/dist/*.whl /wheel/
RUN pip install /wheel/*.whl

ENTRYPOINT [ "python3.10", "-m", "urdu_builder" ]

COPY assets /assets
COPY templates /templates
RUN mkdir /build

WORKDIR /src
