import os

from config import METADATA_FILENAME, OUTPUT_DIR, VECTORS_FILENAME
from loaders.golden_dataset import load as load_golden
from loaders.search_terms import load as load_search_terms


EXPECTED_METADATA_COLUMNS = [
    "label",
    "category",
    "subcategory",
    "source",
    "type",
    "use_case",
    "frequency",
    "record_count",
]


def _read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def test():
    os.environ["EMBEDDER"] = "mock"

    import main  # noqa: PLC0415

    main.main()

    vectors_path = os.path.join(OUTPUT_DIR, VECTORS_FILENAME)
    metadata_path = os.path.join(OUTPUT_DIR, METADATA_FILENAME)

    assert os.path.exists(vectors_path), f"Missing: {vectors_path}"
    assert os.path.exists(metadata_path), f"Missing: {metadata_path}"

    vectors_lines = _read_lines(vectors_path)
    metadata_lines = _read_lines(metadata_path)

    assert len(metadata_lines) == len(vectors_lines) + 1, (
        f"metadata lines={len(metadata_lines)} should equal vectors lines={len(vectors_lines)} + 1 header"
    )

    header = metadata_lines[0].split("\t")
    assert header == EXPECTED_METADATA_COLUMNS, f"Bad metadata header: {header}"

    dims = [len(line.split("\t")) for line in vectors_lines if line.strip()]
    assert len(dims) == len(vectors_lines), "Found empty vector line(s)"
    assert len(set(dims)) == 1, f"Inconsistent vector dimensions found: {sorted(set(dims))}"

    golden_items = load_golden()
    search_items = load_search_terms()
    assert len(golden_items) >= 10, f"Expected >=10 golden items, got {len(golden_items)}"
    assert len(search_items) >= 10, f"Expected >=10 search items, got {len(search_items)}"

    print("[test] OK")


if __name__ == "__main__":
    test()

