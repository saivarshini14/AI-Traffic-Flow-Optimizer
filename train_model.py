
import csv
import json
import os
import random
import math

os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

random.seed(42)

# Generate sample traffic training data
rows = []

for _ in range(500):
    hour = random.randint(0, 23)
    vehicles = random.randint(5, 200)
    speed = random.randint(5, 80)

    if vehicles >= 130 or (vehicles >= 90 and speed < 25):
        traffic = "High"
    elif vehicles >= 65 or speed < 35:
        traffic = "Medium"
    else:
        traffic = "Low"

    rows.append([hour, vehicles, speed, traffic])

# Save training data
with open("data/traffic.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["hour", "vehicles", "average_speed", "traffic"])
    writer.writerows(rows)

# Build a simple decision tree using information gain
def entropy(labels):
    total = len(labels)
    counts = {}

    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )

def majority(labels):
    return max(set(labels), key=labels.count)

def build_tree(data, depth=0):
    labels = [row[3] for row in data]

    if len(set(labels)) == 1 or depth >= 6 or len(data) < 8:
        return {"class": majority(labels)}

    parent_entropy = entropy(labels)
    best_gain = 0
    best_feature = None
    best_threshold = None
    best_split = None

    for feature in range(3):
        values = sorted(set(row[feature] for row in data))

        for i in range(len(values) - 1):
            threshold = (values[i] + values[i + 1]) / 2

            left = [r for r in data if r[feature] <= threshold]
            right = [r for r in data if r[feature] > threshold]

            if not left or not right:
                continue

            gain = parent_entropy - (
                len(left) / len(data) * entropy([r[3] for r in left])
                + len(right) / len(data) * entropy([r[3] for r in right])
            )

            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_threshold = threshold
                best_split = (left, right)

    if best_feature is None:
        return {"class": majority(labels)}

    return {
        "feature": best_feature,
        "threshold": best_threshold,
        "left": build_tree(best_split[0], depth + 1),
        "right": build_tree(best_split[1], depth + 1)
    }

tree = build_tree(rows)

with open("models/traffic_model.json", "w") as file:
    json.dump(tree, file)

print("Traffic decision tree trained successfully!")
print("Training samples:", len(rows))
print("Model saved to models/traffic_model.json")
