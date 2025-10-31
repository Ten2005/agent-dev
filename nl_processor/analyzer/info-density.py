import spacy
from typing import Optional


class InfoDensityAnalyzer:
    def __init__(self, model_name: str = "en_core_web_trf"):
        self.model_name = model_name
        self._nlp: Optional[spacy.language.Language] = None

    @property
    def nlp(self) -> spacy.language.Language:
        if self._nlp is None:
            self._nlp = spacy.load(self.model_name)
        return self._nlp

    def _calculate_depth(self, idx: int, token, cache: dict[int, int]) -> int:
        if idx in cache:
            return cache[idx]

        if token.dep_ == "ROOT" or token.head == token:
            cache[idx] = 0
            return 0

        depth = 1 + self._calculate_depth(token.head.i, token.head, cache)
        cache[idx] = depth
        return depth

    def analyze(self, text: str) -> list[dict[str, str | float]]:
        doc = self.nlp(text)

        if not doc:
            return []

        depth_cache: dict[int, int] = {}
        depths = [
            self._calculate_depth(idx, token, depth_cache)
            for idx, token in enumerate(doc)
        ]
        max_depth = max(depths, default=1) or 1

        return [
            {
                "text": token.text,
                "depth": depth / max_depth,
            }
            for token, depth in zip(doc, depths)
        ]


if __name__ == "__main__":
    text = "Apple is looking at buying U.K. startup for $1 billion"
    analyzer = InfoDensityAnalyzer("en_core_web_trf")
    results = analyzer.analyze(text)
    print(results)
