repo := "homelab-library"

@pull:
    git submodule update --init --remote
    git submodule foreach -q 'branch="$(git config -f $toplevel/.gitmodules submodule.$name.branch)"; git checkout $branch'

add-container name:
    #!/usr/bin/env bash
    cd containers
    git submodule add "git@github.com:{{repo}}/{{name}}.git"

new-container name: (template "container-init" name) (template "container" name)
    #!/usr/bin/env bash
    docker run --rm -it -u "$UID:$UID" \
        -v "$PWD/containers:/output" -v "$HOME/.config/hub:/.config/hub" \
        -w '/output/{{name}}' \
        $(docker build -q templates) \
        hub create -d "'{{name}}' container for homelab-library" "{{repo}}/{{name}}"

template t target:
    #!/usr/bin/env bash
    git init "containers/{{target}}"
    touch "containers/{{target}}/library.yml"

    docker run --rm -it -u "$UID:$UID" \
        -v "$PWD/containers:/output" \
        $(docker build -q templates) \
        templar -rf -s "name={{target}}" -d "/templates/defaults.yml" -t "/templates/{{t}}" -o "/output/{{target}}"

template-shell:
    #!/usr/bin/env bash
    docker run --rm -it -u "$UID:$UID" \
        -v "$PWD/containers:/output" \
        $(docker build -q templates)
