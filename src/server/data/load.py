# src/server/data/load.py

from bs4 import BeautifulSoup
from tqdm import tqdm
import feedparser
import tiktoken
import requests
import html
import json

from data import MODULE_PATH


def _count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode("hello my love"))


def load_test_sentences():
    """Load test sentences dataset.

    This contains 100 sentences, 5 from each of 20 different books; these
    books cover 10 genres.
    """

    with open(MODULE_PATH / "test_sentences.json", "r") as f:
        sentences = json.load(f)

    return sentences


def load_paul_grahams_essays():
    """Load Paul Graham's essays.

    This contains 219 essays which will be returned using the following format:

    ```
    {
        "title": "Essay title",
        "text": "Essay text",
        "metadata": {
            "source": "URL",
            "tokens": "token count"
        }
    }
    ```
    """

    URL = "http://www.aaronsw.com/2002/feeds/pgessays.rss"

    links = [e["link"] for e in feedparser.parse(URL)["entries"]]

    essays = []

    for link in tqdm(links, total=len(links), desc="Downloading essays"):
        r = requests.get(link)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")

            text = " ".join([s.strip() for s in soup.body.text.split()])
            text = html.unescape(text)
            text = text.encode("ascii", "ignore").decode("ascii")

            essays.append(
                {
                    "title": soup.title.text,
                    "metadata": {"source": link, "tokens": _count_tokens(text)},
                    "text": text,
                }
            )

    return essays
