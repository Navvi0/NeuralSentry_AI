import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

print("--- Neural Sentry: Expanded Deep Analytics Suite ---")

# Verify core assets exist
required_files = ["neural_sentry_brain.pkl", "model_columns.pkl", "KDDTest+.txt"]
missing_files = [f for f in required_files if not os.path.exists(f)]
if missing_files:
    print(f"❌ ERROR: Missing required assets: {missing_files}")
    exit()

print("Step 1: Loading verification dataset telemetry...")
test_data = pd.read_csv("KDDTest+.txt", header=None)

# Extract matching raw feature slices
feature_indices = [0, 1, 2, 3, 4, 5, 22]
X_raw = test_data.iloc[:, feature_indices]
y_test = test_data.iloc[:, 41]

print("Step 2: Processing and encoding testing matrix columns...")
# One-hot encode the text columns
X_encoded = pd.get_dummies(X_raw, columns=[1, 2, 3])
X_encoded.columns = X_encoded.columns.astype(str)

# Load the exact column structure from the training phase to align data shapes
model_columns = joblib.load("model_columns.pkl")

# Reindex the test columns to match the training columns perfectly
# This fills missing columns with 0 if a specific network flag didn't appear in the test set
X_test = X_encoded.reindex(columns=model_columns, fill_value=0)

print("Step 3: Awakening advanced AI Core for diagnostic inspection...")
model = joblib.load("neural_sentry_brain.pkl")
predictions = model.predict(X_test)

# Calculate precision metrics
correct = (predictions == y_test).sum()
total = len(test_data)
accuracy = (correct / total) * 100

print("\n================ SYSTEM PERFORMANCE REPORT ================")
print(f"📊 Total Network Packets Analyzed: {total}")
print(f"✅ Correctly Classified Traffic:  {correct}")
print(f"🎯 Overall Upgraded Accuracy:      {accuracy:.2f}%")
print("===========================================================")

print("\n📋 GENERATING COMPREHENSIVE CLASSIFICATION REPORT...")
report = classification_report(y_test, predictions, zero_division=0)
print(report)
