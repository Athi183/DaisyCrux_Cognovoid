import os
import pickle


from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DATASET_CANDIDATES = [
    "dataset/synthetic_mental_health_dataset.csv",
    os.path.expanduser("~/Downloads/synthetic_mental_health_dataset.csv"),
]

FEATURES = [
    "sleep_hours",
    "screen_time",
    "exercise_minutes",
    "daily_pending_tasks",
    "interruptions",
    "fatigue_level",
    "social_hours",
    "coffee_cups",
    "diet_quality",
    "weather",
    "mood_score",
]
TARGET = "stress_level"
CATEGORICAL = ["diet_quality", "weather"]


def _load_dataset():
    for path in DATASET_CANDIDATES:
        if os.path.exists(path):
            print(f"Using dataset: {path}")
            return pd.read_csv(path)
    raise FileNotFoundError(
        "Could not find synthetic_mental_health_dataset.csv in dataset/ or ~/Downloads/"
    )


df = _load_dataset()
missing = [name for name in FEATURES + [TARGET] if name not in df.columns]
if missing:
    raise ValueError(f"Dataset missing required columns: {missing}")

X_raw = df[FEATURES].copy()
y = pd.to_numeric(df[TARGET], errors="coerce").fillna(0.0)

# One-hot encode categorical columns and keep training column order for inference.
X = pd.get_dummies(X_raw, columns=CATEGORICAL, dtype=float)
feature_columns = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBRegressor(
    random_state=42,
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="reg:squarederror",
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2: {r2:.4f}")

pickle.dump(model, open("regression_model.pkl", "wb"))
pickle.dump(
    {
        "feature_columns": feature_columns,
        "features": FEATURES,
        "categorical": CATEGORICAL,
    },
    open("regression_meta.pkl", "wb"),
)

print("Regression model saved to regression_model.pkl + regression_meta.pkl")
