import hashlib
import json
import math
import re
from pathlib import Path


FIELDS = {
    "id",
    "fact_text",
    "structured_value",
    "tier",
    "volatility_class",
    "shareability",
    "verified_at",
}
MANIFEST_FIELDS = {"exported_at", "active_count", "total_count", "sha256"}
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "or", "that",
    "the", "this", "to", "was", "were", "will", "with", "you", "your",
}
TOKEN_RE = re.compile(r"[a-z0-9]+")


class PackError(Exception):
    pass


def _tokens(value):
    return {token for token in TOKEN_RE.findall(str(value).lower())
            if token not in STOPWORDS}


def _structured_tokens(value):
    if isinstance(value, dict):
        tokens = set()
        for key, item in value.items():
            tokens.update(_tokens(key))
            tokens.update(_structured_tokens(item))
        return tokens
    if isinstance(value, list):
        tokens = set()
        for item in value:
            tokens.update(_structured_tokens(item))
        return tokens
    if value is None:
        return set()
    return _tokens(value)


class Pack:
    def __init__(self, rows):
        self._rows = rows
        self._fact_tokens = []
        document_frequency = {}
        for row in rows:
            tokens = _tokens(row["fact_text"])
            tokens.update(_structured_tokens(row["structured_value"]))
            self._fact_tokens.append(tokens)
            for token in tokens:
                document_frequency[token] = document_frequency.get(token, 0) + 1
        count = len(rows)
        self._idf = {token: math.log(count / frequency)
                     for token, frequency in document_frequency.items()}

    def search(self, query_text, top_k=6):
        query_tokens = _tokens(query_text)
        matches = []
        for row, fact_tokens in zip(self._rows, self._fact_tokens):
            score = sum(self._idf[token] for token in query_tokens & fact_tokens)
            if score <= 0:
                continue
            score /= math.sqrt(len(fact_tokens))
            matches.append({
                "id": row["id"],
                "fact_text": row["fact_text"],
                "shareability": row["shareability"],
                "verified_at": row["verified_at"],
                "score": score,
            })
        matches.sort(key=lambda match: match["score"], reverse=True)
        return matches[:top_k]


def load_pack(pack_path, manifest_path):
    pack_path = Path(pack_path)
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        raise PackError("manifest does not exist")
    try:
        pack_bytes = pack_path.read_bytes()
        manifest = json.loads(manifest_path.read_text())
        rows = json.loads(pack_bytes)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PackError(str(error)) from error

    if not isinstance(manifest, dict) or not MANIFEST_FIELDS.issubset(manifest):
        raise PackError("manifest is missing required fields")
    active_count = manifest.get("active_count")
    total_count = manifest.get("total_count")
    if type(active_count) is not int or type(total_count) is not int:
        raise PackError("manifest counts must be integers")
    digest = hashlib.sha256(pack_bytes).hexdigest()
    if digest != manifest.get("sha256"):
        raise PackError("pack sha256 does not match manifest")
    if not isinstance(rows, list) or len(rows) != active_count:
        raise PackError("pack row count does not match active_count")
    if active_count >= total_count:
        raise PackError("active_count must be below total_count")
    if not rows or any(not isinstance(row, dict) or set(row) != FIELDS
                       for row in rows):
        raise PackError("pack rows must contain exactly the required fields")
    return Pack(rows)
