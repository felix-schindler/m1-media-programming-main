from os import path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

from const import BASE_PATH, FEATURE_SCHEMA, PASS_MODEL_PATH, SCORE_MODEL_PATH

app = Flask(__name__, template_folder=path.join(BASE_PATH, "data", "templates"))

# Pipelines laden (enthalten Preprocessing + Modell)
score_pipeline = joblib.load(SCORE_MODEL_PATH)
pass_pipeline = joblib.load(PASS_MODEL_PATH)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", schema=FEATURE_SCHEMA)


@app.route("/predictions", methods=["POST"])
def predictions():
    try:
        data = request.get_json()

        # Eingaben in einen DataFrame konvertieren
        input_df = pd.DataFrame([data])

        # Typkonvertierung basierend auf Schema erzwingen
        for feature, config in FEATURE_SCHEMA.items():
            if feature in input_df.columns:
                if config["type"] == "number":
                    input_df[feature] = pd.to_numeric(input_df[feature])
                elif config["type"] == "binary":
                    input_df[feature] = (
                        input_df[feature].astype(float).fillna(0).astype(int)
                    )

        # Vorhersage (Pipeline kümmert sich um Encoding!)
        score_pred = score_pipeline.predict(input_df)[0]
        pass_pred_raw = pass_pipeline.predict(input_df)[0]

        # Clamp Score (kann bei Regression theoretisch > 100 oder < 0 sein)
        score_pred = max(0, min(100, score_pred))

        return jsonify(
            {
                "success": True,
                "final_exam_score": round(float(score_pred), 2),
                "passed_exam_raw": int(pass_pred_raw),
                "passed_exam_label": "Bestanden"
                if pass_pred_raw == 1
                else "Nicht bestanden",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
