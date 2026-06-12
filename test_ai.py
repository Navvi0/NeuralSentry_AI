import pandas as pd
import joblib
import os

print("--- Neural Sentry: Evaluation Phase ---")

# Safety check for the model brain and test file
if not os.path.exists("neural_sentry_brain.pkl") or not os.path.exists("KDDTest+.txt"):
    print("❌ ERROR: Missing neural_sentry_brain.pkl or KDDTest+.txt!")
    exit()

print("Step 1: Loading test dataset...")
test_data = pd.read_csv("KDDTest+.txt", header=None)

# Extract matching features (Columns 0, 4, 5) and labels (Column 41)
X_test = test_data.iloc[:, [0, 4, 5]]
y_test = test_data.iloc[:, 41]

print("Step 2: Awakening trained intelligence model...")
model = joblib.load("neural_sentry_brain.pkl")

print("Step 3: Running deep packet inspection analysis...")
predictions = model.predict(X_test)

# Calculate precision metrics
correct = (predictions == y_test).sum()
total = len(test_data)
accuracy = (correct / total) * 100

print("\n================ SYSTEM REPORT ================")
print(f"📊 Total Network Packets Analyzed: {total}")
print(f"✅ Correctly Classified Traffic:  {correct}")
print(f"🎯 Overall Detection Accuracy:     {accuracy:.2f}%")
print("===============================================")
