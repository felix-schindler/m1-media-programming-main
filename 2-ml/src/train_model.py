from os import path

import joblib
import kagglehub
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from const import CATEGORICAL_FEATURES, MODEL_DIR, NUMERICAL_FEATURES

# --- Pfade und Daten laden ---
DATA_PATH = path.join(
    # https://www.kaggle.com/datasets/emonsharkar/python-learning-and-exam-performance-dataset
    kagglehub.dataset_download(
        "emonsharkar/python-learning-and-exam-performance-dataset"
    ),
    "python_learning_exam_performance.csv",
)


# Lade den Datensatz
df = pd.read_csv(DATA_PATH)

# Zielspalten (Targets)
TARGET_SCORE = "final_exam_score"
TARGET_PASSED = "passed_exam"
TARGETS = [TARGET_SCORE, TARGET_PASSED]

# Entferne Zeilen mit fehlenden Werten (vereinfacht das Projekt)
df.dropna(inplace=True)

# One-Hot Encoding der Kategorialen Features
df_encoded_categorical = pd.get_dummies(
    df[CATEGORICAL_FEATURES].copy(), columns=CATEGORICAL_FEATURES, drop_first=True
)

# Stelle sicher, dass die binäre Zielvariable 'passed_exam' numerisch ist (0 oder 1)
X = pd.concat([df[NUMERICAL_FEATURES].copy(), df_encoded_categorical], axis=1)
y_passed = df[TARGET_PASSED].astype(int)
y_score = df[TARGET_SCORE]

# Features speichern
feature_names = X.columns.tolist()
joblib.dump(feature_names, path.join(MODEL_DIR, "encoded_feature_names.pkl"))
print(f"Kodierte Feature-Namen ({len(feature_names)}) gespeichert.")

# Training
X_train_reg, X_test_reg, y_train_score, y_test_score = train_test_split(
    X, y_score, test_size=0.2, random_state=42
)
regressor = GradientBoostingRegressor(
    n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42
)
regressor.fit(X_train_reg, y_train_score)
joblib.dump(regressor, path.join(MODEL_DIR, "score_regressor.pkl"))

X_train_clf, X_test_clf, y_train_passed, y_test_passed = train_test_split(
    X, y_passed, test_size=0.2, random_state=42
)
classifier = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
classifier.fit(X_train_clf, y_train_passed)
joblib.dump(classifier, path.join(MODEL_DIR, "pass_classifier.pkl"))

# Evaluation
predictions_reg = regressor.predict(X_test_reg)
mae = mean_absolute_error(y_test_score, predictions_reg)
r2 = r2_score(y_test_score, predictions_reg)
predictions_clf = classifier.predict(X_test_clf)
acc = accuracy_score(y_test_passed, predictions_clf)

print("\n--- Regressor (Score) ---")
print(f"Durchschnittlicher Fehler (MAE): {mae:.2f} Punkte")
print(f"Bestimmtheitsmaß (R2): {r2:.2f}/1.0")

print("\n--- Classifier (Bestanden) ---")
print(f"Genauigkeit (Accuracy): {acc:.2f}")

print("\nAlle Modelle erfolgreich in 'data/ml' gespeichert.")
