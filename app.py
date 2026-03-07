from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/api/predictions")
def predictions():

    with open("output/predictions.json") as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
