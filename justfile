repo := "homelab-library"

@pull:
    git submodule update --init

add-container name:
    #!/usr/bin/env bash
    cd containers
    git submodule add "git@github.com:{{repo}}/{{name}}.git"
