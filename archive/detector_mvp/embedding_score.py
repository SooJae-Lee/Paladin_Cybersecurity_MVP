"""
Control-Treatment 임베딩/유사도 점수
sklearn 있으면 TF-IDF cosine, 없으면 SequenceMatcher
"""

from __future__ import annotations
from difflib import SequenceMatcher
from typing import Dict, Any, List
import json


def _tfidf_cosine(a: str, b: str) -> float:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vec = TfidfVectorizer().fit([a or " ", b or " "])
        x = vec.transform([a or " ", b or " "])
        return float(cosine_similarity(x[0], x[1])[0][0])
    except Exception:
        return SequenceMatcher(None, a or "", b or "").ratio()


def add_embedding_scores(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for r in records:
        a = r.get("control_response") or ""
        b = r.get("treatment_response") or ""
        item = dict(r)
        item["embedding_similarity"] = round(_tfidf_cosine(a, b), 4)
        out.append(item)
    return out


if __name__ == "__main__":
    with open("data/labeled_dataset_v2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    recs = add_embedding_scores(data["records"])
    print("n=", len(recs))
    for r in recs:
        print(r["case_id"], r["label"], r["embedding_similarity"])