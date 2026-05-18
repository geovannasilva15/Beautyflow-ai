from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimpleRAG:
    def __init__(self, knowledge_path: str = "knowledge_base/beleza.txt") -> None:
        self.knowledge_path = Path(knowledge_path)
        self.chunks = self._load_chunks()
        self.vectorizer = TfidfVectorizer(stop_words=None)
        self.matrix = self.vectorizer.fit_transform(self.chunks) if self.chunks else None

    def _load_chunks(self) -> list[str]:
        if not self.knowledge_path.exists():
            return []
        text = self.knowledge_path.read_text(encoding="utf-8")
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        return chunks

    def retrieve(self, question: str, top_k: int = 3) -> list[str]:
        if not self.chunks or self.matrix is None:
            return []
        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        ranked = scores.argsort()[::-1][:top_k]
        return [self.chunks[i] for i in ranked if scores[i] > 0]
