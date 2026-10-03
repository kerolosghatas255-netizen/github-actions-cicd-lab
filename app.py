import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(
        message="CI/CD Release Pipeline Lab",
        status="running",
    )


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


@app.get("/version")
def version():
    return jsonify(
        version=os.getenv("APP_VERSION", "dev"),
        commit=os.getenv("GIT_SHA", "local"),
        environment=os.getenv("APP_ENV", "local"),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
