# src/runpod-worker/src/handler.py

import runpod

from models import EmbeddingModel


MODELS = {}


def load_models() -> None:
    """Load models into memory."""
    global MODELS

    MODELS["embedding"] = EmbeddingModel()

    return


def handler(job):
    """Handler function that will be used to process jobs."""
    job_input = job["input"]
    task = job_input["task"]

    if task == "embed":
        embed = MODELS["embedding"]
        texts = job_input["texts"]
        embeddings = embed(texts)

        return embeddings

    else:
        return {"error": f"Task {task} not supported."}


if __name__ == "__main__":
    load_models()

    runpod.serverless.start({"handler": handler})
