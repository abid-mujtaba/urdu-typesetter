FROM ubuntu:kinetic

LABEL Maintainer Abid H. Mujtaba <abid.naqvi83@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV PACKAGES \
    texlive-xetex \
    texlive-lang-arabic

RUN apt-get update \
    && apt-get install -y $PACKAGES \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /src
