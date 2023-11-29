# src/runpod-worker/src/models.py

from optimum.onnxruntime import (
    AutoOptimizationConfig,
    ORTModelForFeatureExtraction,
    ORTOptimizer,
)
from transformers import AutoTokenizer
import torch

from typing import Any, List
import logging
import os

from settings import settings


logger = logging.getLogger(__name__)


def _download_embedding_model() -> None:
    """Download the Embedding model from HuggingFace and Optimize it with ONNX."""

    model_dir = settings.MODEL_PATH / "onnx" / settings.EMBEDDING_MODEL

    if not model_dir.exists():
        model_dir.mkdir(parents=True)

        try:
            model = ORTModelForFeatureExtraction.from_pretrained(
                settings.EMBEDDING_MODEL, export=True, provider="CUDAExecutionProvider"
            )
            optim = ORTOptimizer.from_pretrained(model)
            config = AutoOptimizationConfig.O4()

            optim.optimize(save_dir=model_dir, optimization_config=config)
            logger.info(f"Optimized model saved to {model_dir}")

            os.environ["ONNX_EMBEDDING_MODEL"] = str(model_dir)
            settings.ONNX_EMBEDDING_MODEL = model_dir

        except Exception as e:
            logger.error(f"Error optimizing model: {e}")
            model_dir.rmdir()
            raise e

    return


class EmbeddingModel:
    """Text embedding model using ONNX & BetterTransformers."""

    def _cls_pooling(self, model_output: Any) -> Any:
        """Use CLS token as pooling token."""
        return model_output[0][:, 0]

    def _mean_pooling(self, model_output: Any, attention_mask: Any) -> Any:
        """Mean pooling - take attention mask into account for correct averaging."""

        token_embeddings = model_output[0]
        attention_mask = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )

        return torch.sum(token_embeddings * attention_mask, 1) / torch.clamp(
            attention_mask.sum(1), min=1e-9
        )

    def __init__(
        self, batch_size: int = 8, pooling: str = "cls", normalize: bool = True
    ):
        """Initialize the model."""

        assert pooling in ["cls", "mean"], f"Pooling {pooling} not supported."

        _download_embedding_model()

        self.pooling = pooling
        self.normalize = normalize
        self.batch_size = batch_size

        self.tokenizer = AutoTokenizer.from_pretrained(settings.ONNX_EMBEDDING_MODEL)
        self.model = ORTModelForFeatureExtraction.from_pretrained(
            settings.ONNX_EMBEDDING_MODEL, provider="CUDAExecutionProvider"
        )

        self.device = self.model.device

    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts."""

        encodings = self.tokenize(texts)
        embeddings = self.embed(encodings)

        return embeddings

    def tokenize(self, texts: List[str]) -> Any:
        """Tokenize inputs"""

        return self.tokenizer(
            texts, padding=True, truncation=True, return_tensors="pt"
        ).to(self.device)

    def embed(self, encodings: Any) -> Any:
        """Embed encoded tokens"""

        model_output = self.model(**encodings)

        if self.pooling == "cls":
            embeddings = self._cls_pooling(model_output)
        elif self.pooling == "mean":
            embeddings = self._mean_pooling(model_output, encodings["attention_mask"])

        if self.normalize:
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

        return embeddings.tolist()


if __name__ == "__main__":
    # Download models
    _download_embedding_model()
