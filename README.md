# DaisyCrux_Cognovoid

Stress risk estimation web app using a regression pipeline.

## Overview

This project predicts a continuous stress score (`0-10`) from daily behavior inputs, then derives a risk score (`0-100`) and risk band for visualization.

Current pipeline:

- Frontend quiz collects regression features.
- Backend predicts stress using `XGBRegressor`.
- Result page renders:
  - Cognitive stability vs risk doughnut
  - Risk-driver radar chart
  - Energy curve
  - Generalized guidance text

## Project Structure

```text
DaisyCrux_Cognovoid/
  backend/
    app.py
    train_model.py
    requirements.txt
    regression_model.pkl
    regression_meta.pkl
    dataset/
      mental_health.csv
  frontend/
    index.html
    quiz.html
    quiz.js
    quiz.css
    result.html
    result.css
```

## Regression Dataset Schema

The regression model expects these inputs:

- `sleep_hours`
- `screen_time`
- `exercise_minutes`
- `daily_pending_tasks`
- `interruptions`
- `fatigue_level`
- `social_hours`
- `coffee_cups`
- `diet_quality` (categorical: `poor|average|good`)
- `weather` (categorical: `sunny|cloudy|rainy|snowy`)
- `mood_score`

Target:

- `stress_level` (continuous, `0-10`)

## Backend

### `backend/train_model.py`

Responsibilities:

- Loads synthetic regression dataset.
- Selects regression features and target (`stress_level`).
- One-hot encodes categorical columns (`diet_quality`, `weather`).
- Trains `XGBRegressor`.
- Prints regression metrics:
  - `MAE`
  - `RMSE`
  - `R2`
- Saves artifacts:
  - `regression_model.pkl`
  - `regression_meta.pkl` (contains `feature_columns`, `features`, `categorical`)

### `backend/app.py`

Responsibilities:

- Loads regression artifacts.
- Accepts quiz payload on `POST /predict`.
- Preprocesses payload to aligned dataframe (same one-hot columns as training).
- Predicts:
  - `predicted_stress_level` (`0-10`)
- Computes:
  - `model_risk_component = predicted_stress_level * 10`
  - `feature_risk_component` from per-feature scaled risk
  - `risk_score = 0.7 * model_risk + 0.3 * feature_risk`
- Returns risk band state:
  - `Low`, `Moderate`, `Elevated`, `High`
- Returns generalized guidance.

## Frontend

### `frontend/quiz.js`

- Collects all regression features.
- Supports:
  - numeric slider questions
  - categorical select questions (`diet_quality`, `weather`)
- Stores answers in `localStorage` (`cognovoidQuizData`).

### `frontend/result.html`

- Reads saved quiz data.
- Calls `http://localhost:5000/predict`.
- Renders:
  - doughnut (`risk_score`)
  - radar (`feature_scores`)
  - line curve (derived from `risk_score`)
- Shows:
  - `state`
  - `predicted_stress_level`
  - guidance text

## API Contract

### `POST /predict`

Request JSON example:

```json
{
  "sleep_hours": 7,
  "screen_time": 4.5,
  "exercise_minutes": 25,
  "daily_pending_tasks": 3,
  "interruptions": 5,
  "fatigue_level": 4,
  "social_hours": 2,
  "coffee_cups": 1,
  "diet_quality": "average",
  "weather": "cloudy",
  "mood_score": 6
}
```

Response JSON example:

```json
{
  "state": "Moderate Stress Outlook",
  "risk_score": 48,
  "predicted_stress_level": 4.9,
  "model_risk_component": 49.0,
  "feature_risk_component": 45.2,
  "inputs": { "...": "..." },
  "feature_scores": { "...": "..." },
  "message": "Predicted stress level is 4.9/10. Current risk band: Moderate.",
  "extra_guidance": []
}
```

## Setup

From `backend/`:

```bash
pip install -r requirements.txt
```

## Train Model

From `backend/`:

```bash
python train_model.py
```

Expected artifacts:

- `backend/regression_model.pkl`
- `backend/regression_meta.pkl`

## Run App

1. Start backend:

```bash
cd backend
python app.py
```

2. Open frontend pages (live server/static server):

- `frontend/index.html`
- `frontend/quiz.html`
- `frontend/result.html`

## Troubleshooting

### `ModuleNotFoundError: pandas`

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

### `regression_model.pkl` not found

Run training first:

```bash
cd backend
python train_model.py
```

### Predictions look stale/unchanged

- Ensure backend restarted after retraining.
- Hard refresh browser (`Ctrl+Shift+R`).
- Verify `POST /predict` response in browser devtools.

## Notes

- Output is decision-support, not clinical diagnosis.
- Guidance is generalized and should not be treated as medical advice.
