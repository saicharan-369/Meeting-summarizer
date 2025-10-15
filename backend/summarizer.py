# summarizer.py
from .utils import OUTPUT_DIR
from pathlib import Path


def _local_extractive_summary(transcript: str, max_sentences: int = 5) -> str:
    """Simple extractive summarizer using TF-IDF sentence scoring."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        import re
    except Exception:
        # If sklearn not available, return first N lines as a very simple fallback
        lines = [l.strip() for l in transcript.splitlines() if l.strip()]
        return "\n".join(lines[:max_sentences])

    # Split transcript into sentences (naive)
    sentences = re.split(r'(?<=[.!?])\s+', transcript.strip())
    if not sentences:
        return ""

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    # score sentences by sum of TF-IDF weights
    scores = np.asarray(X.sum(axis=1)).ravel()
    ranked_idx = scores.argsort()[::-1]
    top_idx = sorted(ranked_idx[:max_sentences])
    selected = [sentences[i].strip() for i in top_idx]
    return "\n".join(selected)


def generate_summary_and_actions(transcript: str):
    """Generate a simple extractive summary of the transcript."""
    content = _local_extractive_summary(transcript)
    
    out = OUTPUT_DIR / "last_summary.txt"
    out.write_text(content or "", encoding="utf-8")
    return content
