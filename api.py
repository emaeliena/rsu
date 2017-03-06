from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"versions": {"v1": "/v1"}})

if __name__ == "__main__":
    app.run()
