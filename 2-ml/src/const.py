from os import path
from pathlib import Path

# Basis
BASE_PATH = path.dirname(path.dirname(__file__))

# Modellpfade
MODEL_DIR = path.join(BASE_PATH, "data", "ml")
Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

SCORE_MODEL_PATH = path.join(MODEL_DIR, "score_regressor.pkl")
PASS_MODEL_PATH = path.join(MODEL_DIR, "pass_classifier.pkl")
FEATURES_PATH = path.join(MODEL_DIR, "encoded_feature_names.pkl")

# Features
NUMERICAL_FEATURES = [
    "age",
    "weeks_in_course",
    "hours_spent_learning_per_week",
    "practice_problems_solved",
    "projects_completed",
    "tutorial_videos_watched",
    "debugging_sessions_per_week",
    "self_reported_confidence_python",
]
CATEGORICAL_FEATURES = [
    "country",
    "prior_programming_experience",
    "uses_kaggle",
    "participates_in_discussion_forums",
]
