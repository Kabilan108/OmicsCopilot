#!/bin/bash

set -e

models=("BAAI/bge-small-en-v1.5")



if [ -d "src/server/models" ]; then
    for model in "${models[@]}"; do
        name=$(echo "${model}" | cut -d'/' -f2)

        huggingface-cli download "${model}"  \
            --local-dir "src/server/models/${name}" \
            --local-dir-use-symlinks False
    done
fi
