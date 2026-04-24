from __future__ import annotations

import os

import pandas as pd

from config import GOLDEN_DATASET_PATH, INCLUDE_SUMMARY_ROWS, USE_CASE_MAP


REQUIRED_COLUMNS = [
    "Category",
    "Subcategory",
    "Source",
    "Representative Top Terms",
    "Records",
]


def _assign_use_case(text: str) -> str:
    text_lc = (text or "").lower()
    for key, value in USE_CASE_MAP.items():
        if key in text_lc:
            return value
    return "UC-Unknown"


def _ensure_sample_excel(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    df = pd.DataFrame(
        [
            {
                "Category": "HR & Benefits",
                "Subcategory": "Leave & Time Off",
                "Source": "Workday",
                "Representative Top Terms": "maternity, adoption, paternity, vacation, sick leave, leave request",
                "Records": 1200,
                "Comments, questions": "Sample row for local testing",
            },
            {
                "Category": "IT Support",
                "Subcategory": "Access & Identity",
                "Source": "ServiceNow GetHelp Knowledge",
                "Representative Top Terms": "vpn, password reset, identity central, it access, mfa, ticket status",
                "Records": 800,
                "Comments, questions": "",
            },
        ]
    )
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)


def load() -> list[dict]:
    """
    Reads the golden dataset (Excel or CSV) and returns a flat list of items.
    """
    path = GOLDEN_DATASET_PATH
    if not os.path.exists(path):
        print(f"[golden_dataset] File not found: {path}")
        if path.lower().endswith(".xlsx"):
            print("[golden_dataset] Creating a small sample Excel file for local testing.")
            _ensure_sample_excel(path)
        else:
            print(
                "[golden_dataset] Expected an .xlsx or .csv file. "
                "Update GOLDEN_DATASET_PATH in config.py."
            )
            return []

    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    else:
        sheets = pd.read_excel(path, sheet_name=None)
        df = pd.concat(sheets.values(), ignore_index=True)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            "Golden dataset missing required columns: "
            f"{missing}. Columns found: {list(df.columns)}"
        )

    items: list[dict] = []
    for _, row in df.iterrows():
        subcat = row.get("Subcategory")
        if pd.isna(subcat):
            continue
        if (not INCLUDE_SUMMARY_ROWS) and str(subcat).strip().upper() == "ALL":
            continue

        terms_raw = row.get("Representative Top Terms", "")
        if pd.isna(terms_raw):
            continue

        for term in str(terms_raw).split(","):
            term = term.strip()
            if not term:
                continue
            items.append(
                {
                    "text": term,
                    "label": term,
                    "category": row.get("Category", ""),
                    "subcategory": row.get("Subcategory", ""),
                    "source": row.get("Source", ""),
                    "record_count": row.get("Records", None),
                    "frequency": None,
                    "type": "document",
                    "use_case": _assign_use_case(term),
                }
            )

    return items

