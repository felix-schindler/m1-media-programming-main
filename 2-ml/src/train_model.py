from os import path

import joblib
import kagglehub
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from const import (
    BINARY_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    PASS_MODEL_PATH,
    SCORE_MODEL_PATH,
)

# Dataset laden
print("Lade Datensatz...")
data_path = path.join(
    kagglehub.dataset_download(
        "emonsharkar/python-learning-and-exam-performance-dataset"
    ),
    "python_learning_exam_performance.csv",
)
df = pd.read_csv(data_path)
df.dropna(inplace=True)  # Cleanup

# Features und Targets definieren
feature_cols = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES

X = df[feature_cols]
y_score = df["final_exam_score"]
y_passed = df["passed_exam"]

# Preprocessing: Pipeline erstellen
numeric_transformer = StandardScaler()  # numerische Werte standardisieren
categorical_transformer = OneHotEncoder(
    handle_unknown="ignore", sparse_output=False
)  # kategoriale Werte: OneHotEncoder
binary_transformer = "passthrough"  # binäre Werte bleiben gleich

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, NUMERICAL_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ("bin", binary_transformer, BINARY_FEATURES),
    ]
)

# Training: Regression (Score)
print("Trainiere Regressor...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_score, test_size=0.2, random_state=42
)

reg_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            GradientBoostingRegressor(
                n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42
            ),
        ),
    ]
)

reg_pipeline.fit(X_train, y_train)

# Evaluation: Regressor
y_pred = reg_pipeline.predict(X_test)
print(f"Regressor MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"Regressor R2: {r2_score(y_test, y_pred):.2f}")

joblib.dump(reg_pipeline, SCORE_MODEL_PATH)

# Training: Classifier (Passed)
print("Trainiere Classifier...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_passed, test_size=0.2, random_state=42
)

clf_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),  # Wir nutzen denselben Preprocessor Logik
        (
            "classifier",
            RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42),
        ),
    ]
)

clf_pipeline.fit(X_train, y_train)

# Evaluation: Classifier
y_pred = clf_pipeline.predict(X_test)
print(f"Classifier Accuracy: {accuracy_score(y_test, y_pred):.2f}")

joblib.dump(clf_pipeline, PASS_MODEL_PATH)
print("Modelle gespeichert.")
