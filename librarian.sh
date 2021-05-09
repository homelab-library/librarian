#!/usr/bin/env bash
set -Eeuo pipefail
touch .env

exec docker run --rm -it --net host --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD:/workspace \
    -v "${HOME}/.gitconfig:/home/librarian/.gitconfig" \
    -v "${HOME}/.ssh:/home/librarian/.ssh" \
    -u $UID:$UID \
    --env-file .env \
    "$(docker build -q librarian/)" "$@"
