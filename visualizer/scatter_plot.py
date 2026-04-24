import os

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

from config import OUTPUT_DIR, PREVIEW_COLOR_BY, PREVIEW_FILENAME, REDUCTION_METHOD


def _reduce(vectors: np.ndarray) -> np.ndarray:
    if REDUCTION_METHOD == "umap":
        try:
            import umap

            reducer = umap.UMAP(n_components=2, random_state=42)
            return reducer.fit_transform(vectors)
        except ImportError:
            print("[visualizer] umap-learn not installed. Falling back to PCA.")
    from sklearn.decomposition import PCA

    return PCA(n_components=2).fit_transform(vectors)


def generate(items: list[dict], vectors: list[list[float]]) -> str:
    vectors_np = np.array(vectors)
    coords = _reduce(vectors_np)

    color_values = [item.get(PREVIEW_COLOR_BY, "unknown") or "unknown" for item in items]
    unique_values = sorted(set(color_values))
    color_index = {v: i for i, v in enumerate(unique_values)}
    colors = [color_index[v] for v in color_values]
    cmap = cm.get_cmap("tab20", len(unique_values))

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.scatter(
        coords[:, 0],
        coords[:, 1],
        c=colors,
        cmap=cmap,
        alpha=0.7,
        s=40,
        linewidths=0,
    )

    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=cmap(color_index[v]),
            markersize=8,
            label=v,
        )
        for v in unique_values
    ]
    ax.legend(
        handles=handles,
        title=PREVIEW_COLOR_BY.replace("_", " ").title(),
        bbox_to_anchor=(1.01, 1),
        loc="upper left",
        fontsize=7,
    )

    freq = [item.get("frequency") or 0 for item in items]
    top_indices = sorted(range(len(items)), key=lambda i: -freq[i])[:15]
    for idx in top_indices:
        ax.annotate(
            items[idx]["label"],
            (coords[idx, 0], coords[idx, 1]),
            fontsize=6,
            alpha=0.85,
            xytext=(3, 3),
            textcoords="offset points",
        )

    method_label = REDUCTION_METHOD.upper()
    ax.set_title(
        f"Embedding Space - 2D {method_label} Projection\nColoured by: {PREVIEW_COLOR_BY}",
        fontsize=12,
    )
    ax.set_xlabel(f"{method_label} Dimension 1")
    ax.set_ylabel(f"{method_label} Dimension 2")
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, PREVIEW_FILENAME)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[visualizer] Preview saved -> {out_path}")
    return out_path

