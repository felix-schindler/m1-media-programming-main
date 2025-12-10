# Getting started

0. Install [uv](https://docs.astral.sh/uv/) using your favorite package manager.
0. Install requirements using `$ uv sync`.
0. (Optional) Train models usin `$ uv run src/train_model.py`.
0. Run the flask app by running `$ uv run src/__main__.py`.

# Links

* [Dataset](https://www.kaggle.com/datasets/emonsharkar/python-learning-and-exam-performance-dataset)
* [Render Dashboard](https://dashboard.render.com/web/srv-d4sintshg0os7386u7eg)
* [Render Deployment](https://m1-mp-ml.onrender.com/)

# Präsentation

## Was macht meine App?

* Gibt Prognose ob Person die Prüfung besteht oder nicht.

## Demo

* Lernt man wenig, ist nicht gut in Python, etc. -> Schlechte Chancen die Prüfung zu bestehen
* Lernt man viel, ist bereits gut, etc. -> Gute Chancen die Prüfung zu bestehen

## Welches Modell?

Zwei Modelle trainiert

* Punktzahl (0-100%): Gradient Boosting Regressor
  * **Warum?** Sagt einen exakten Zahlenwert vorher
  * **Was ist das?** Jeder Baum versucht, die Fehler der vorherigen Bäume zu korrigieren
* Bestehen (Ja/Nein): Random Forest Classifier
  * **Warum?** Sagt eine Klasse vorher
	* **Was ist das?** Viele Entscheidungsbäume, die zusammen abstimmen
* Hatte einige Problem, deshalb Modelle als Pipelines

## Was als Nächstes verbessern?

* Datenset ist viel zu klein, dadurch ungenau.
* Actionable Advice, z.B. "Wenn du 2 Stunden mehr pro Woche debuggst, steigert sich deine Note um 10%."

## Link teilen

* https://m1-mp-ml.onrender.com/
* [QR-Code](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data=https://m1-mp-ml.onrender.com/)
