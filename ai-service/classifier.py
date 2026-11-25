import json
import os
from pathlib import Path

import joblib

from preprocessing import clean_text

FOLDER = Path(__file__).resolve().parent / "artifacts" / "intent"

class IntentClassifier:
    def __init__(self, folder=FOLDER):
        try:
            config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
            self.tfidf = joblib.load(folder / "tfidf_vectorizer.joblib")
            self.model = joblib.load(folder / "logreg.joblib")
            self.le = joblib.load(folder / "label_encoder.joblib")
        except FileNotFoundError as e:
            raise SystemExit(f"Artefak model tidak lengkap di {folder} : {e}. " "")
        self.threshold = float((os.getenv("INTENT_THRESHOLD", config.get("threshold", 0.5))))

    def predict(self, pesan):
        bersih = clean_text(pesan)
        if not bersih:
            return "lainnya", 0.0
        proba = self.model.predict_proba(self.tfidf.transform([bersih]))[0]
        i = int(proba.argmax())
        intent = str(self.le.classes_[int(self.model.classes_[i])])
        confidance = float(proba[i])
        if confidance < self.threshold:
            intent = "lainnya"
        return intent, round(confidance, 4)