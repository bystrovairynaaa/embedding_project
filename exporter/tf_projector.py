import os

from config import METADATA_FILENAME, OUTPUT_DIR, VECTORS_FILENAME


METADATA_COLUMNS = [
    "label",
    "category",
    "subcategory",
    "source",
    "type",
    "use_case",
    "frequency",
    "record_count",
]


def export(items: list[dict], vectors: list[list[float]]) -> tuple[str, str]:
    """
    items   — list of item dicts (from loaders)
    vectors — list of embedding vectors (same length and order as items)
    Returns paths to (vectors_path, metadata_path)
    """
    assert len(items) == len(vectors), f"Mismatch: {len(items)} items but {len(vectors)} vectors"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    vectors_path = os.path.join(OUTPUT_DIR, VECTORS_FILENAME)
    metadata_path = os.path.join(OUTPUT_DIR, METADATA_FILENAME)

    with open(vectors_path, "w", encoding="utf-8") as f:
        # Write without a trailing blank line (some tools count it as an extra row).
        lines = ["\t".join(f"{v:.6f}" for v in vec) for vec in vectors]
        f.write("\n".join(lines))

    with open(metadata_path, "w", encoding="utf-8") as f:
        lines = ["\t".join(METADATA_COLUMNS)]
        for item in items:
            row = [str(item.get(col, "") or "") for col in METADATA_COLUMNS]
            lines.append("\t".join(row))
        f.write("\n".join(lines))

    print(f"[export] Written {len(items)} items")
    print(f"  vectors  -> {vectors_path}")
    print(f"  metadata -> {metadata_path}")
    return vectors_path, metadata_path

