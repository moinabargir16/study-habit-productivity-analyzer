
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load the demonstration dataset
data = pd.read_csv("productivity_data.csv")

# 2. Separate inputs (X) and target labels (y)
X = data[
    ["study_hours", "sleep_hours", "task_completion"]
]

y = data["productivity_level"]

# 3. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# 4. Create and train the model
model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

model.fit(X_train, y_train)

# 5. Evaluate the model on the held-out test set
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

# 6. Save the trained model
joblib.dump(model, "productivity_model.joblib")

print("\nModel saved successfully!")
