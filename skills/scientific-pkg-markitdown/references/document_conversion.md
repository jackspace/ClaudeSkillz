# Document Conversion

Use a virtual environment and install only the extras required by the input
formats:

```bash
python -m venv .venv
source .venv/bin/activate
pip install 'markitdown[pdf,docx,pptx,xlsx,xls]'
```

## Format Matrix

| Input | Extra | Notes |
| --- | --- | --- |
| PDF | `pdf` | Text PDFs work locally. Scanned PDFs may require OCR. |
| DOCX | `docx` | Preserves headings, lists, links, and tables when available. |
| PPTX | `pptx` | Extracts slide text and can describe images with an LLM. |
| XLSX | `xlsx` | Converts sheets and cells into Markdown tables. |
| XLS | `xls` | Enables older Excel workbooks. |

## Local-Only Conversion

Prefer the narrow local-file method when the input should never trigger a
network request:

```python
from pathlib import Path
from markitdown import MarkItDown

source = Path("documents/report.pdf").resolve(strict=True)
allowed_root = Path("documents").resolve(strict=True)
if not source.is_relative_to(allowed_root):
    raise ValueError("Input must stay inside documents/")

result = MarkItDown().convert_local(source)
Path("output/report.pdf.md").write_text(result.text_content, encoding="utf-8")
```

Validate file paths before conversion. MarkItDown performs I/O with the
permissions of the current process.

