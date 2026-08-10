import csv
from collections import Counter


def audit_csv(path):
    """Read-only CSV audit: returns machine-readable quality findings."""
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    headers = list(rows[0].keys()) if rows else []
    normalized = [tuple((r.get(h) or '').strip() for h in headers) for r in rows]
    duplicate_rows = sum(n - 1 for n in Counter(normalized).values() if n > 1)
    columns = {}
    for h in headers:
        vals = [r.get(h) or '' for r in rows]
        columns[h] = {
            'missing': sum(not v.strip() for v in vals),
            'whitespace_issues': sum(v != v.strip() for v in vals),
            'unique_nonblank': len({v.strip() for v in vals if v.strip()}),
        }
    return {
        'row_count': len(rows),
        'column_count': len(headers),
        'duplicate_rows': duplicate_rows,
        'columns': columns,
    }
