from os import path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

from const import (
    BASE_PATH,
    CATEGORICAL_FEATURES,
    FEATURES_PATH,
    NUMERICAL_FEATURES,
    PASS_MODEL_PATH,
    SCORE_MODEL_PATH,
)

app = Flask(__name__, template_folder=path.join(BASE_PATH, "data", "templates"))

# Models und Feature-Namen laden
score_model = joblib.load(SCORE_MODEL_PATH)
pass_model = joblib.load(PASS_MODEL_PATH)
encoded_feature_names = joblib.load(FEATURES_PATH)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        raw_features=NUMERICAL_FEATURES,
        categorical_features=CATEGORICAL_FEATURES,
    )


@app.route("/predictions", methods=["POST"])
def predictions():
    try:
        data = request.get_json()

        # Eingaben in einen DataFrame konvertieren
        input_df = pd.DataFrame([data])

        # Input trennen
        input_numerical = input_df[NUMERICAL_FEATURES].astype(float)
        input_categorical = input_df[CATEGORICAL_FEATURES]

        # One-Hot Encoding NUR der kategorialen Daten
        input_encoded_categorical = pd.get_dummies(
            input_categorical, columns=CATEGORICAL_FEATURES, drop_first=True
        )

        # Alle vorbereiteten Features zusammenführen
        input_prepared = pd.concat([input_numerical, input_encoded_categorical], axis=1)

        # Spalten des Inputs mit trainierten Features überprüfen und anpassen
        final_input = pd.DataFrame(0, index=np.arange(1), columns=encoded_feature_names)

        for col in input_prepared.columns:
            if col in final_input.columns:
                final_input[col] = input_prepared[col].iloc[0]

        # Konvertieren in ein NumPy-Array
        input_array = final_input.values

        # Vorhersagen
        score_prediction = score_model.predict(input_array)[0]
        passed_prediction_raw = pass_model.predict(input_array)[0]
        passed_prediction_label = (
            "Bestanden" if passed_prediction_raw == 1 else "Nicht bestanden"
        )

        return jsonify(
            {
                "success": True,
                "final_exam_score": round(float(score_prediction), 2),
                "passed_exam_raw": int(passed_prediction_raw),
                "passed_exam_label": passed_prediction_label,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Verarbeitungsfehler: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
