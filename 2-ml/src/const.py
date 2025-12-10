from os import path
from pathlib import Path

# Basis Pfade
BASE_PATH = path.dirname(path.dirname(__file__))
MODEL_DIR = path.join(BASE_PATH, "data", "ml")
Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
# Modellpfade
SCORE_MODEL_PATH = path.join(MODEL_DIR, "score_pipeline.pkl")
PASS_MODEL_PATH = path.join(MODEL_DIR, "pass_pipeline.pkl")

# --- DATA SCHEMA & CONFIGURATION ---
# Wir definieren ein Dictionary, das die Logik für Frontend UND Backend hält.
FEATURE_SCHEMA = {
    # Numerische Features mit Limits für die HTML-Validierung
    "hours_spent_learning_per_week": {
        "label": "Lernstunden pro Woche",
        "type": "number",
        "min": 0,
        "max": 168,
        "step": 0.5,
        "default": 5,
    },
    "practice_problems_solved": {
        "label": "Gelöste Übungsaufgaben",
        "type": "number",
        "min": 0,
        "max": 5000,
        "step": 1,
        "default": 10,
    },
    "projects_completed": {
        "label": "Abgeschlossene Projekte",
        "type": "number",
        "min": 0,
        "max": 500,
        "step": 1,
        "default": 2,
    },
    "tutorial_videos_watched": {
        "label": "Gesehene Tutorial-Videos",
        "type": "number",
        "min": 0,
        "max": 1000,
        "step": 1,
        "default": 10,
    },
    "debugging_sessions_per_week": {
        "label": "Debugging-Sessions pro Woche",
        "type": "number",
        "min": 0,
        "max": 100,
        "step": 1,
        "default": 1,
    },
    "self_reported_confidence_python": {
        "label": "Selbsteinschätzung (1-10)",
        "type": "number",
        "min": 1,
        "max": 10,
        "step": 1,
        "default": 5,
    },
    # Kategoriale Features
    "prior_programming_experience": {
        "label": "Vorerfahrung",
        "type": "select",
        "options": ["None", "Beginner", "Intermediate", "Advanced"],
    },
    "country": {
        "label": "Land",
        "type": "select",
        # Optionen werden idealerweise aus den Trainingsdaten geladen,
        # hier hardcoden wir die wichtigsten als Fallback.
        "options": ["Germany", "USA", "India", "UK", "Canada", "Brazil", "Other"],
    },
    # Binäre Features (Behandeln wir als Select mit Ja/Nein)
    "uses_kaggle": {
        "label": "Nutzt Kaggle",
        "type": "binary",  # 1 = Ja, 0 = Nein
    },
    "participates_in_discussion_forums": {
        "label": "Aktiv in Foren",
        "type": "binary",
    },
}

# Helper Listen für das Training
NUMERICAL_FEATURES = [k for k, v in FEATURE_SCHEMA.items() if v["type"] == "number"]
CATEGORICAL_FEATURES = [k for k, v in FEATURE_SCHEMA.items() if v["type"] == "select"]
BINARY_FEATURES = [k for k, v in FEATURE_SCHEMA.items() if v["type"] == "binary"]
