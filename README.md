# AI Data Cleaner: Inspect → Fix → Verify Pipeline

A reproducible, production-ready workflow for cleaning messy spreadsheet exports using Python, Pandas, and LLM-assisted normalization. Companion code for the "10-Second AI Data Cleaner" tutorial.

## The Problem

Raw business data exports are messy:
- **Country variants**: "USA", "US", "United States", "united states of america" → 20+ variants for one country
- **Mixed dates**: `2023-01-15`, `2023/03/10`, `-`, `N/A`
- **Dirty numbers**: `1250.50`, `-`, `N/A` (zeroing financial nulls corrupts totals!)
- **Silent duplicates**: 20 duplicate `customer_id` rows corrupting aggregations

## The Solution: 3-Tier Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  1️⃣  PARSE       →  Load raw, detect dtypes, flag anomalies │
│  2️⃣  NORMALIZE   →  LLM-assisted category mapping           │
│     (20 country variants → 6 canonical)                     │
│  3️⃣  VALIDATE    →  Schema guards, verification log,        │
│     human review                                            │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone and run
git clone https://github.com/TaskToFlow/ai-data-cleaner
cd ai-data-cleaner
pip install pandas numpy
python cleaner.py
```

**Output:**
- `customers_clean.csv` — cleaned, analysis-ready dataset
- `cleaning_report.md` — full audit trail with step-by-step verification

## Pipeline Steps

| Step | Operation | Key Principle |
|------|-----------|---------------|
| 1 | **Duplicate Audit** | `df.duplicated(subset=['customer_id'])` → keep first, log count |
| 2 | **Spend Cleanup** | Replace `-`/`N/A` → `NaN` (never zero!), `pd.to_numeric(errors='coerce')` |
| 3 | **Date Parsing** | `pd.to_datetime(format='mixed', errors='coerce')` handles ISO, slash, dashes |
| 4 | **Country Norm** | `str.lower().map(COUNTRY_MAP)` — 20 variants → 6 canonical, preserve unmatched |
| 5 | **Phone Format** | Regex digit extraction → E.164 (`+1XXXXXXXXXX`) |
| 6 | **Status Clean** | Lowercase → Title Case mapping |
| 7 | **Verify** | Schema checks: no dupe IDs, numeric spend, parsed dates, row count sanity |

## Example Output

```bash
$ python cleaner.py

📥 Loading messy dataset...
  ✓ Load: Loaded 40 rows × 9 columns
🔄 Step 2: Duplicate audit...
  ✓ Duplicate Audit: Found 40 rows with duplicate customer_ids (20 unique IDs affected)
  ✓ Deduplication: Removed 20 duplicate rows, kept first occurrence
💰 Step 3: Null & junk handling (total_spend)...
  ✓ Spend Cleanup: Converted 7 dashes + 0 N/A to NaN; nulls: 0 → 7
📅 Step 4: Mixed date parsing...
  ✓ Date Parse (signup_date): Parsed 20 dates; dashes→NaN: 0; unparseable→NaN: 0
  ✓ Date Parse (last_purchase): Parsed 20 dates; dashes→NaN: 0; unparseable→NaN: 0
🌍 Step 5: Category normalization (country)...
  ✓ Country Normalization: Original unique countries: 20; Mapped: 20; Unmatched (preserved): 0
📞 Step 6: Phone normalization...
  ✓ Phone Normalization: Cleaned 20 phone numbers to E.164-like format
🏷️ Step 7: Status cleanup...
  ✓ Status Cleanup: Standardized Active/Inactive casing
✅ Step 8: Final verification...
  ✓ Verification: All checks passed: True | Details: {...}

💾 Exported clean dataset: customers_clean.csv (20 rows)
📄 Report written: cleaning_report.md
```

## Verification Checks

The pipeline enforces production safety guards:

```python
checks = {
    "no_duplicate_ids": df["customer_id"].duplicated().sum() == 0,
    "spend_numeric": pd.api.types.is_numeric_dtype(df["total_spend"]),
    "dates_parsed": df["signup_date"].notna().sum() > 0,
    "countries_mapped": df["country"].isin(COUNTRY_MAP.values()).sum() > 0,
    "row_count_reasonable": 0.5 * original_rows <= len(df) <= original_rows,
}
```

## Extending for Your Data

1. **Add columns**: Extend `output_cols` in `cleaner.py`
2. **Custom mappings**: Extend `COUNTRY_MAP` or add `CATEGORY_MAP`
3. **Schema validation**: Add Pydantic models for stricter guards
4. **LLM integration**: Replace `COUNTRY_MAP` with LLM call for fuzzy matching

```python
# Example: LLM-assisted normalization
def llm_normalize(value, category, examples):
    prompt = f"Normalize '{value}' to standard {category}. Examples: {examples}"
    return llm(prompt)
```

## Files

```
ai-data-cleaner/
├── cleaner.py              # Full pipeline (Inspect → Fix → Verify)
├── customers_messy.csv     # Sample messy export (40 rows, 9 cols)
├── customers_clean.csv     # Output: cleaned data (generated)
├── cleaning_report.md      # Output: audit trail (generated)
├── render_video.py         # Tutorial video renderer (PIL + ffmpeg)
├── thumbnail.png           # Video thumbnail (generated)
├── VIDEO_METADATA.md       # YouTube title, description, tags
└── README.md               # This file
```

## Requirements

- Python 3.10+
- `pandas >= 2.0`
- `numpy >= 1.24`
- `pillow >= 10.0` (for video rendering)
- `ffmpeg` (for video stitching)

## License

MIT — Use freely in your workflows.

## Channel

**Task to Flow** — Practical AI Workflows for Business
📺 youtube.com/@TaskToFlow
💻 github.com/TaskToFlow