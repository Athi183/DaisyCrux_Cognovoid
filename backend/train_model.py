import pandas as pd
from xgboost import XGBClassifier
import joblib

# Load dataset
df = pd.read_csv("mental_health.csv")

# Select features
X = df[['sleep', 'stress', 'mood', 'focus', 'screen', 'anxiety', 'fatigue']]
y = df['mental_state']  # target column

# Train model
model = XGBClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "mental_model.pkl")

print("Model trained and saved!")