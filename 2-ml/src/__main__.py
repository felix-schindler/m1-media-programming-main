from os import path

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

from cost import base_path

app = Flask(__name__, template_folder=path.join(base_path, "data", "templates"))

MODEL_DIR = path.join(base_path, "data", "ml")
MODEL_PATH = path.join(MODEL_DIR, "model.pkl")
FEATURE_NAMES_PATH = path.join(MODEL_DIR, "feature_names.pkl")

# Platzhalter für das Modell und die Feature-Namen
model = None
feature_names = []

try:
    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)
    # Wine Class Labels: 0, 1, 2. Wir geben die Bedeutung zurück.
    # Abhängig vom Datensatz müsstest du das anpassen.
    wine_classes = ["Class 0", "Class 1", "Class 2"]
    print(f"ML Model und {len(feature_names)} Features erfolgreich geladen.")
except Exception as e:
    print(f"FEHLER beim Laden der Dateien in {MODEL_DIR}: {e}")
    # Das Programm wird dennoch starten, aber Vorhersagen werden fehlschlagen
    wine_classes = ["Model Error"]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", feature_names=feature_names)


@app.route("/predictions", methods=["POST"])
def predictions():
    """
    1. Empfängt die Formulardaten.
    2. Konvertiert sie in ein NumPy-Array.
    3. Macht die Vorhersage.
    4. Gibt das Ergebnis als JSON zurück.
    """
    if model is None:
        return jsonify({"error": "ML model not loaded."}), 500

    try:
        # Die Daten kommen als JSON im Body des POST-Requests
        data = request.get_json()

        # Sicherstellen, dass alle 13 Features übergeben wurden (der erwartete Input)
        if len(data) != len(feature_names):
            return jsonify(
                {
                    "error": f"Erwarte {len(feature_names)} Werte, aber erhielt {len(data)}."
                }
            ), 400

        # Werte von Python-Liste zu NumPy-Array (für das Modell) konvertieren
        # Das Modell erwartet ein 2D-Array: [[feature_1, feature_2, ...]]
        input_data = np.array([data]).astype(float)

        # Vorhersage treffen (gibt z.B. 0, 1 oder 2 zurück)
        prediction_index = model.predict(input_data)[0]

        # Wahrscheinlichkeiten (optional, aber nützlich)
        probabilities = model.predict_proba(input_data)[0]

        # Ergebnis-Label
        result_label = wine_classes[prediction_index]

        # Ergebnis als JSON zurückgeben
        return jsonify(
            {
                "success": True,
                "prediction_label": result_label,
                "prediction_index": int(prediction_index),
                "probabilities": probabilities.tolist(),
            }
        )

    except Exception as e:
        # Fängt Fehler bei der Datenkonvertierung oder der Vorhersage ab
        return jsonify({"error": f"Verarbeitungsfehler: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
