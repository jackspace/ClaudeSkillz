# Structured Data

MarkItDown converts CSV, JSON, and XML sources into Markdown suited to text
analysis. Validate the source size and schema before conversion.

```python
from pathlib import Path
from markitdown import MarkItDown

source = Path("data/report.json")
if source.stat().st_size > 5_000_000:
    raise ValueError("Input exceeds 5 MB")

result = MarkItDown().convert_local(source)
Path("output/report.json.md").write_text(
    result.text_content,
    encoding="utf-8",
)
```

## Practical Checks

- Confirm the character encoding before converting CSV or XML.
- Reject unexpectedly large arrays, deeply nested objects, or oversized cells.
- Keep source identifiers beside converted Markdown for traceability.
- Treat formula-like spreadsheet cells and embedded text as untrusted content.
- Validate generated tables before using them in prompts or reports.

