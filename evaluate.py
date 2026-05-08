import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from detector import detect_ai_text

# Load dataset
df = pd.read_csv("sample_dataset.csv")

predictions = []

# Run detector
for text in df["text"]:

    result = detect_ai_text(text)

    if result["score"] > 0.5:
        predictions.append("AI")
    else:
        predictions.append("Human")

# True labels
true_labels = df["label"]

# Accuracy
accuracy = accuracy_score(true_labels, predictions)

print("\n=== Evaluation Results ===")

print(f"\nAccuracy: {accuracy:.2f}")

# Classification report
print("\nClassification Report:")
print(classification_report(true_labels, predictions))

# Confusion matrix
cm = confusion_matrix(true_labels, predictions)

print("\nConfusion Matrix:")
print(cm)

# Plot confusion matrix
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["AI", "Human"]
)

disp.plot(cmap="Blues")

plt.title("Confusion Matrix")

# Save figure
plt.savefig("confusion_matrix.png")

print("\nConfusion matrix figure saved as confusion_matrix.png")

plt.show()