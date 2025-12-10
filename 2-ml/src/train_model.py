from os import path
from pathlib import Path

import joblib
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from cost import base_path

# 1. Daten laden
print("Lade Daten...")
data = load_wine()
X, y = data.data, data.target

# Feature Namen speichern (wichtig für deine spätere Web-App!)
feature_names = data.feature_names
print(f"Features: {feature_names}")

# 2. Trainings- und Testdaten splitten (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Modell trainieren
print("Trainiere Modell...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 4. Genauigkeit prüfen
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Modell Genauigkeit: {accuracy:.2f}")

# 5.1 Zielpfad für das Modell erstellen
target_path = path.join(base_path, "data", "ml")
Path(target_path).mkdir(parents=True, exist_ok=True)

# 5.2 Modell exportieren
joblib.dump(model, path.join(target_path, "model.pkl"))
joblib.dump(feature_names, path.join(target_path, "feature_names.pkl"))
print("Modell gespeichert als 'model.pkl'")
