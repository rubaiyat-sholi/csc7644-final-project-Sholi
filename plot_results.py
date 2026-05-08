import matplotlib.pyplot as plt

# Metrics
metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
values = [0.75, 0.83, 0.75, 0.73]

# Create chart
plt.figure(figsize=(8, 5))

bars = plt.bar(metrics, values)

# Labels
plt.ylim(0, 1.0)
plt.ylabel("Score")
plt.title("Evaluation Metrics")

# Add values on bars
for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width()/2,
        value + 0.02,
        f"{value:.2f}",
        ha='center'
    )

# Save image
plt.savefig("evaluation_metrics.png")

print("Chart saved as evaluation_metrics.png")

plt.show()