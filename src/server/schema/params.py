# src/server/schema/params.py

from pydantic import BaseModel, Field


class PCA(BaseModel):
    """Parameters for PCA."""

    n_components: int = Field(2, ge=1, description="Number of components to keep.")


class TSNE(BaseModel):
    """Parameters for t-SNE."""

    n_components: int = Field(2, ge=1, description="Number of components to keep.")
    perplexity: float = Field(30, ge=1, description="Perplexity of the model.")
    learning_rate: float = Field(200, ge=1, description="Learning rate of the model.")
