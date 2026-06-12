import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("--- Neural Sentry: Advanced Training Phase ---")

if not os.path.exists("KDDTrain+.txt"):
    print("❌ ERROR: KDDTrain+.txt dataset missing!")
    exit()

print("Step 1: Loading full NSL-KDD Training Dataset...")
df = pd.read_csv("KDDTrain+.txt", header=None)

# Select a powerful mix of continuous and categorical features
feature_indices = [0, 1, 2, 3, 4, 5, 22]
X_raw = df.iloc[:, feature_indices]
y = df.iloc[:, 41]

print("Step 2: Encoding network protocols and security flags...")
# Convert text columns (Protocol, Service, Flag) into mathematical dummy variables
X = pd.get_dummies(X_raw, columns=[1, 2, 3])

# 🔥 CRITICAL FIX LINE: Force all column names to be strings so scikit-learn doesn't crash
X.columns = X.columns.astype(str)

# Save the exact column structure so our testing script can match it perfectly later
joblib.dump(X.columns, "model_columns.pkl")

print(f"Dataset expanded! Training matrix shape: {X.shape}")

print("Step 3: Training Deep Random Forest Classifier (100 Trees)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("Step 4: Serializing upgraded intelligence architecture...")
joblib.dump(model, "neural_sentry_brain.pkl")
print("🏆 SUCCESS: Advanced neural_sentry_brain.pkl generated and saved!")
