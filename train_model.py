import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. Load training data
# ============================================================

DATA_FILE = "data/training_data.csv"

df = pd.read_csv(DATA_FILE)

print("=" * 60)
print("YouTube Comment Intelligence - ML Training")
print("=" * 60)

print(f"\nTotal training examples: {len(df)}")

print("\nCategory distribution:")
print(df["Category"].value_counts())


# ============================================================
# 2. Remove missing data
# ============================================================

df = df.dropna(
    subset=["Comment", "Category"]
)

df["Comment"] = df["Comment"].astype(str)
df["Category"] = df["Category"].astype(str)


# ============================================================
# 3. Split dataset
# ============================================================

X = df["Comment"]
y = df["Category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining comments:", len(X_train))
print("Testing comments:", len(X_test))


# ============================================================
# 4. Create ML pipeline
# ============================================================

model = Pipeline([
    
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])


# ============================================================
# 5. Train model
# ============================================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


# ============================================================
# 6. Test model
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# 7. Accuracy
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# 8. Classification report
# ============================================================

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 9. Confusion matrix
# ============================================================

print("\nConfusion Matrix:\n")

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print(
    pd.DataFrame(
        cm,
        index=labels,
        columns=labels
    )
)


# ============================================================
# 10. Save model
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)

MODEL_FILE = "models/comment_classifier.pkl"

joblib.dump(
    model,
    MODEL_FILE
)

print("\nModel saved successfully!")

print(
    f"Location: {MODEL_FILE}"
)

print("\nTraining finished.")