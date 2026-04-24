import sys

from embedders import get_embedder
from exporter import tf_projector
from loaders.golden_dataset import load as load_golden
from loaders.search_terms import load as load_search_terms
from visualizer import scatter_plot


def main():
    print("=== Embedding Projector Pipeline ===\n")

    print("[1/4] Loading data...")
    golden_items = load_golden()
    search_items = load_search_terms()
    all_items = golden_items + search_items
    print(f"  Golden dataset items : {len(golden_items)}")
    print(f"  Search term items    : {len(search_items)}")
    print(f"  Total items          : {len(all_items)}\n")

    if len(all_items) == 0:
        print("ERROR: No items loaded. Check your data files and paths in config.py")
        sys.exit(1)

    print("[2/4] Generating embeddings...")
    embedder = get_embedder()
    texts = [item["text"] for item in all_items]
    vectors = embedder.embed(texts)
    print(f"  Embedding dimension  : {len(vectors[0])}\n")

    print("[3/4] Exporting TF Projector files...")
    vectors_path, metadata_path = tf_projector.export(all_items, vectors)
    print()

    print("[4/4] Generating 2D preview chart...")
    preview_path = scatter_plot.generate(all_items, vectors)
    print()

    print("=== Done ===")
    print("\nTo load in TensorFlow Projector:")
    print("  1. Go to https://projector.tensorflow.org/")
    print("  2. Click 'Load' (top left)")
    print(f"  3. Upload vectors file  : {vectors_path}")
    print(f"  4. Upload metadata file : {metadata_path}")
    print(
        "  5. Use the colour-by dropdown to colour by: category, use_case, type, etc."
    )
    print(f"\nLocal 2D preview: {preview_path}")


if __name__ == "__main__":
    main()

