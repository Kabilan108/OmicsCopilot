FROM kabilan108/runpod-base:0.1.0-cuda11.8.0

ARG MODEL_PATH
ARG EMBEDDING_MODEL

COPY builder/free_disk_space.sh builder/pyproject.toml /
RUN /bin/bash /free_disk_space.sh \
    && rm /free_disk_space.sh \
    && poetry install --only main --no-interaction --no-ansi \
    && rm /pyproject.toml \
    && rm -rf /root/.cache/pypoetry

EXPOSE 8000

ADD src .

CMD python -u /handler.py
