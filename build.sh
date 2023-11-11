#!/bin/bash

# # install tesseract-ocr for unstructured.io
# apt-get update && apt-get install -y tesseract-ocr

# # install poetry
# curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# # install python dependencies
# poetry install

# download embedding models from huggingface
# huggingface-cli login --token "${HUGGINGFACE_TOKEN}"
my_array=("sentence-transformers/all-MiniLM-L6-v2" "BAAI/bge-large-en-v1.5")

for model in "${my_array[@]}"; do
    name=$(echo "${model}" | cut -d'/' -f2)

    huggingface-cli download "${model}"  \
        --local-dir "models/${name}" \
        --local-dir-use-symlinks False
done
