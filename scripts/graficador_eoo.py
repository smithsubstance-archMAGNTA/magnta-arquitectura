"""Script de ejemplo para graficar entropy score."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render_sample(scores):
    plt.figure(figsize=(8, 4))
    plt.plot(scores, marker="o")
    plt.title("Entropy score - MAGNTA")
    plt.xlabel("Tiempo")
    plt.ylabel("Score")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("entropy_sample.png")
    plt.close()


if __name__ == "__main__":
    sample = [0.12, 0.18, 0.26, 0.35, 0.58, 0.72, 0.81, 0.66, 0.42]
    render_sample(sample)
    print("Archivo generado: entropy_sample.png")
