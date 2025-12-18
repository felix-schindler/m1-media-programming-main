from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello():
    return {"status": "ok", "msg": "Hello from Docker!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
