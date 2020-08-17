FROM debian:buster-slim

RUN apt-get update && apt-get install -yy curl xz-utils git && \
    curl -sL "https://github.com/proctorlabs/templar/releases/download/v0.4.1/templar-x86_64-unknown-linux-gnu.tar.xz" | \
        tar -xJ -C /usr/bin/ && \
    curl -sL "https://github.com/github/hub/releases/download/v2.14.2/hub-linux-amd64-2.14.2.tgz" | \
        tar -xz -C /usr/bin --strip-components 2 hub-linux-amd64-2.14.2/bin/hub

COPY . /templates
