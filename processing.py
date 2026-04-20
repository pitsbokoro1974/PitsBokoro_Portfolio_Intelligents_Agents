from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProcessingAgent:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    # ----------------------------
    # CLEANING 
    # ----------------------------
    def clean(self, papers):
        seen = set()
        cleaned = []

        for p in papers:
            title = str(p.get("title", "")).strip()
            year = p.get("year")
            authors = p.get("authors", [])

            if not title or not year or not authors:
                continue

            if title in seen:
                continue

            seen.add(title)

            cleaned.append({
                "title": title,
                "authors": authors,
                "year": str(year),
                "doi": p.get("doi")
            })

        return cleaned

    # ----------------------------
    # RELEVANCE SCORING (NEW)
    # ----------------------------
    def classify(self, papers, query=None):
        """
        Instead of fake labels, we compute relevance score
        based on similarity to query.
        """

        if not papers:
            return []

        titles = [p["title"] for p in papers]

        if query:
            corpus = titles + [query]
        else:
            corpus = titles

        tfidf = self.vectorizer.fit_transform(corpus)

        doc_vectors = tfidf[:-1] if query else tfidf
        query_vector = tfidf[-1] if query else None

        results = []

        for i, p in enumerate(papers):
            try:
                if query:
                    score = cosine_similarity(doc_vectors[i], query_vector)[0][0]
                else:
                    score = 1.0  

                results.append({
                    **p,
                    "relevance_score": float(score)
                })

            except Exception:
                continue

        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return results