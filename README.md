
# AI-Based Traffic Flow Optimizer

An educational machine-learning web application that predicts traffic levels and demonstrates signal-timing recommendations.

## Features
- Random Forest traffic classification
- Flask prediction API
- Interactive traffic dashboard
- Prediction history chart
- Input validation
- Simulated signal timing recommendations

## Technologies
Python, pandas, scikit-learn, Flask, HTML, CSS, JavaScript, Chart.js.

## Run locally
1. Create and activate a Python virtual environment.
2. Install dependencies using `python -m pip install -r requirements.txt`.
3. Train the model using `python train_model.py`.
4. Start the app using `python app.py`.
5. Open http://127.0.0.1:5000 in your browser.

## API
POST `/api/predict`

Example JSON:
```json
{
  "hour": 18,
  "vehicles": 100,
  "average_speed": 20
}
```

## Data and limitations
The initial training data is synthetic and intended for demonstrating the workflow. The test score does not establish real-world predictive performance. Signal timing is simulated and does not control real traffic infrastructure.
