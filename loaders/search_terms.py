from __future__ import annotations

import os

import pandas as pd

from config import SEARCH_TERMS_PATH, TOP_N_SEARCH_TERMS, USE_CASE_MAP


REQUIRED_COLUMNS = ["search_term", "frequency"]


def _assign_use_case(text: str) -> str:
    text_lc = (text or "").lower()
    for key, value in USE_CASE_MAP.items():
        if key in text_lc:
            return value
    return "UC-Unknown"


def _ensure_sample_csv(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    df = pd.DataFrame(
        [
            {"search_term": "My Pay", "frequency": 120},
            {"search_term": "mypay", "frequency": 80},
            {"search_term": "Workday benefits", "frequency": 60},
            {"search_term": "VPN", "frequency": 55},
            {"search_term": "Password reset", "frequency": 50},
            {"search_term": "People Finder", "frequency": 45},
            {"search_term": "Concur expense", "frequency": 42},
            {"search_term": "Coupa travel", "frequency": 39},
            {"search_term": "IT access", "frequency": 35},
            {"search_term": "GetHelp ticket", "frequency": 33},
            {"search_term": "Knowledge base", "frequency": 30},
            {"search_term": "My Learning", "frequency": 28},
        ]
    )
    df.to_csv(path, index=False)


def load() -> list[dict]:
    path = SEARCH_TERMS_PATH
    if not os.path.exists(path):
        print(f"[search_terms] File not found: {path}")
        print("[search_terms] Creating a small sample CSV file for local testing.")
        _ensure_sample_csv(path)

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Search terms CSV missing required columns: {missing}. Columns found: {list(df.columns)}"
        )

    df["search_term"] = df["search_term"].astype(str).str.lower().str.strip()
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce").fillna(0).astype(int)

    df = df.groupby("search_term", as_index=False)["frequency"].sum()
    df = df.sort_values("frequency", ascending=False).head(TOP_N_SEARCH_TERMS)

    items: list[dict] = []
    for _, row in df.iterrows():
        term = row["search_term"]
        items.append(
            {
                "text": term,
                "label": term,
                "category": "Search Query",
                "subcategory": "User Search Term",
                "source": "Search Logs Jan-Mar",
                "record_count": None,
                "frequency": int(row["frequency"]),
                "type": "keyword",
                "use_case": _assign_use_case(term),
            }
        )

    return items

