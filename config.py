import os
from pathlib import Path

# ── Embedding model selection ─────────────────────────────────────────────────
# Options: "sentence_transformer" | "azure_openai"
# Default is the recommended local/offline embedder.
EMBEDDER = os.getenv("EMBEDDER", "sentence_transformer")

# ── Sentence Transformer settings ─────────────────────────────────────────────
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

# ── Azure OpenAI settings (read from environment variables only) ──────────────
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "text-embedding-ada-002")
AZURE_OPENAI_BATCH_SIZE = 16  # items per API call

# ── Input data paths ─────────────────────────────────────────────────────────
# Can be .xlsx (original) or .csv (taxonomy export)
# Keep paths stable regardless of the current working directory.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
# Main input file (taxonomy / golden dataset)
GOLDEN_DATASET_PATH = str(DATA_DIR / "kbs_example_taxonomy.csv")

# Optional secondary input (unused by default pipeline now)
SEARCH_TERMS_PATH = str(DATA_DIR / "search_terms_-_Jan_-_Mar.csv")

# ── Data filtering ───────────────────────────────────────────────────────────
TOP_N_SEARCH_TERMS = 100  # Keep only top N search terms by frequency
INCLUDE_SUMMARY_ROWS = False  # If True, include Excel rows where Subcategory == "ALL"

# ── Output ───────────────────────────────────────────────────────────────────
OUTPUT_DIR = "output"
VECTORS_FILENAME = "vectors.tsv"
METADATA_FILENAME = "metadata.tsv"
PREVIEW_FILENAME = "preview_2d.png"

# ── 2D Visualisation ─────────────────────────────────────────────────────────
# Options: "pca" | "umap"
# Use "pca" first — it needs no extra install.
# Switch to "umap" for better cluster separation (requires: pip install umap-learn)
REDUCTION_METHOD = os.getenv("REDUCTION_METHOD", "pca")
PREVIEW_COLOR_BY = "category"  # metadata column to use for color-coding

# Keys are lowercase substrings to match against the text field.
# First match wins. Items that match nothing get "UC-Unknown".
USE_CASE_MAP = {
    "workday": "UC-01: Enterprise Apps",
    "my pay": "UC-01: Enterprise Apps",
    "mypay": "UC-01: Enterprise Apps",
    "benefits": "UC-01: Enterprise Apps",
    "my benefits": "UC-01: Enterprise Apps",
    "power of you": "UC-01: Enterprise Apps",
    "kb": "UC-02: IT Help / KB",
    "knowledge": "UC-02: IT Help / KB",
    "gethelp": "UC-02: IT Help / KB",
    "servicenow": "UC-02: IT Help / KB",
    "ticket": "UC-02: IT Help / KB",
    "people finder": "UC-03: People Finder",
    "people": "UC-03: People Finder",
    "identity central": "UC-04: Access & Identity",
    "it access": "UC-04: Access & Identity",
    "vpn": "UC-04: Access & Identity",
    "password": "UC-04: Access & Identity",
    "concur": "UC-05: Travel & Expense",
    "coupa": "UC-05: Travel & Expense",
    "travel": "UC-05: Travel & Expense",
    "amex": "UC-05: Travel & Expense",
    "expense": "UC-05: Travel & Expense",
    "my learning": "UC-06: Learning",
    "mylearning": "UC-06: Learning",
    "learning": "UC-06: Learning",
    "acronym": "UC-07: Glossary / Acronym",
    "glossary": "UC-07: Glossary / Acronym",
    "chatpg": "UC-08: AI / RAG",
    "copilot": "UC-08: AI / RAG",
    "chat": "UC-08: AI / RAG",
}

