"""Tiny local retrieval: markdown chunking and TF-IDF cosine search. No external dependencies, no network."""
import math
import pathlib
import re
from collections import Counter
from dataclasses import dataclass

WORD = re.compile(r"[a-z0-9]+")
STOP = set("the a an and or of to in is are for on with by as it be this that from at how what why which when does do can should "
           "you your its into than so not no only use used using one each".split())


def tokens(text):
    return [w for w in WORD.findall(text.lower()) if w not in STOP and len(w) > 1]


@dataclass
class Chunk:
    source: str
    title: str
    text: str


def chunk_markdown(text, source):
    """One chunk per '## ' section; the '# ' title is kept as context for each chunk."""
    doc_title, chunks, head, buf = source, [], None, []
    for line in text.splitlines():
        if line.startswith("# "):
            doc_title = line[2:].strip()
        elif line.startswith("## "):
            if buf:
                chunks.append(Chunk(source, f"{doc_title}: {head}" if head else doc_title, " ".join(buf).strip()))
            head, buf = line[3:].strip(), []
        elif line.strip():
            buf.append(line.strip())
    if buf:
        chunks.append(Chunk(source, f"{doc_title}: {head}" if head else doc_title, " ".join(buf).strip()))
    return chunks


class Store:
    def __init__(self, chunks=()):
        self.chunks = []
        self.add(list(chunks))

    @classmethod
    def from_dirs(cls, *dirs):
        chunks = []
        for d in dirs:
            for f in sorted(pathlib.Path(d).glob("*.md")):
                chunks += chunk_markdown(f.read_text(encoding="utf-8"), f.name)
        return cls(chunks)

    def add(self, chunks):
        self.chunks += chunks
        docs = [Counter(tokens(c.title + " " + c.text)) for c in self.chunks]
        df = Counter(w for d in docs for w in d)
        n = len(docs)
        self.idf = {w: math.log((1 + n) / (1 + df[w])) + 1 for w in df}
        self.vecs = [self._vec(d) for d in docs]

    def _vec(self, counts):
        v = {w: c * self.idf.get(w, 0.0) for w, c in counts.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / norm for w, x in v.items()}

    def search(self, query, k=3):
        q = self._vec(Counter(tokens(query)))
        scored = [(sum(q.get(w, 0.0) * x for w, x in v.items()), c) for v, c in zip(self.vecs, self.chunks)]
        return [(s, c) for s, c in sorted(scored, key=lambda t: -t[0])[:k] if s > 0]
