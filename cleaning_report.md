# Cleaning Report: customers_messy.csv
Generated: 2026-11-25T14:49:37.829334

## Summary
- Original rows: 40
- Final rows: 20
- Rows removed (duplicates): 20
- Spend nulls remaining: 1
- Countries mapped to canonical: 1
- All verification checks passed: True

## Step-by-Step Log
### Load
- Time: 2026-11-25T14:49:37.817885
- Loaded: 40 rows × 9 columns
- Rows before: 40
- Rows after: 40

### Duplicate Audit
- Time: 2026-11-25T14:49:37.821608
- Found: 40 rows with duplicate customer_ids (20 unique IDs affected)
- Rows before: 40
- Rows after: 40

### Deduplication
- Time: 2026-11-25T14:49:37.822640
- Removed: 20 duplicate rows, kept first occurrence
- Rows before: 40
- Rows after: 20

### Spend Cleanup
- Time: 2026-11-25T14:49:37.823083
- Converted: 7 dashes/N/A to NaN; nulls: 0 → 7
- Rows before: 20
- Rows after: 20

### Date Parse (signup_date)
- Time: 2026-11-25T14:49:37.824368
- Parsed: 20 dates; dashes→NaN: 0; unparseable→NaN: 0
- Rows before: 20
- Rows after: 20

### Date Parse (last_purchase)
- Time: 2026-11-25T14:49:37.824701
- Parsed: 20 dates; dashes→NaN: 0; unparseable→NaN: 0
- Rows before: 20
- Rows after: 20

### Country Normalization
- Time: 2026-11-25T14:49:37.826771
- Original unique countries: 20 ({'United States': 1, 'USA': 1, 'US': 1, 'United Kingdom': 1, 'UK': 1, 'Germany': 1, 'Deutschland': 1, 'France': 1, 'FR': 1, 'Canada': 1, 'CA': 1, 'Australia': 1, 'AU': 1, 'Japan': 1, 'JP': 1, 'Brazil': 1, 'Brasil': 1, 'India': 1, 'IN': 1, 'United States of America': 1})
- Mapped: 20
- Unmatched (preserved): 0
- Rows before: 20
- Rows after: 20

### Phone Normalization
- Time: 2026-11-25T14:49:37.827173
- Cleaned: 20 phone numbers to E.164-like format
- Rows before: 20
- Rows after: 20

### Status Cleanup
- Time: 2026-11-25T14:49:37.827363
- Standardized: Active/Inactive casing
- Rows before: 20
- Rows after: 20

### Verification
- Time: 2026-11-25T14:49:37.827837
- All checks passed: True
- Details: {'no_duplicate_ids': np.True_, 'spend_numeric': True, 'dates_parsed': np.True_, 'countries_mapped': np.True_, 'row_count_reasonable': True}
- Rows before: 20
- Rows after: 20
