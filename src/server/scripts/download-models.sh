#!/bin/bash

set -e

models=("BAAI/bge-small-en-v1.5")

if [ -d "models/" ]; then
    for model in "${models[@]}"; do
        huggingface-cli download "${model}"  \
            --local-dir "models/${model}" \
            --local-dir-use-symlinks False

        optimum-cli export onnx \
            --model "models/${model}" \
            --framework pt \
            --task feature-extraction \
            --optimize O4 \
            --device cuda \
            "models/${model}-onnx-O4"
    done
fi
