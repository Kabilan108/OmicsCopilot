# src/server/data/load.py

import json

from data import MODULE_PATH


def load_test_sentences():
    """Load test sentences dataset.

    This contains 100 sentences, 5 from each of 20 different books; these
    books cover 10 genres.
    """

    with open(MODULE_PATH / "test_sentences.json", "r") as f:
        sentences = json.load(f)

    return sentences
