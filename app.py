
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

MODEL_PATH = os.path.join("models", "traffic_model.json")

with open(MODEL_PATH, "r") as file:
    model = json.load(file)

def predict_tree(tree, features):
    if "class" in tree:
        return tree["class"]

    feature = tree["feature"]
    threshold = tree["threshold"]

    if features[feature] <= threshold:
        return predict_tree(tree["left"], features)
    else:
        return predict_tree(tree["right"], features)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        hour = int(data.get("hour", 12))
        vehicles = int(data.get("vehicles", 50))
        average_speed = float(data.get("average_speed", 40))

        if not 0 <= hour <= 23:
            return jsonify({"error": "Hour must be between 0 and 23"}), 400

        if not 0 <= vehicles <= 10000:
            return jsonify({"error": "Vehicle count must be between 0 and 10000"}), 400

        if not 0 <= average_speed <= 300:
            return jsonify({"error": "Average speed must be between 0 and 300"}), 400

        traffic = predict_tree(model, [hour, vehicles, average_speed])

        signal_times = {
            "Low": 20,
            "Medium": 35,
            "High": 50
        }

        return jsonify({
            "prediction": traffic,
            "signal_seconds": signal_times[traffic],
            "hour": hour,
            "vehicles": vehicles,
            "average_speed": average_speed
        })

    except (ValueError, TypeError, AttributeError):
        return jsonify({"error": "Please enter valid numeric values."}), 400

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "model_loaded": True})


if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

    app.run(debug=True)
