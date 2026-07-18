# Troubleshooting

## Missing Converter

Install the extra associated with the input type. Use `[all]` only when the
larger dependency set is acceptable:

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

## Empty or Incomplete Output

1. Confirm the source file opens normally.
2. Check whether a PDF contains selectable text.
3. Install the OCR plugin for scanned or image-heavy documents.
4. Retry one file directly before running a batch.

## Remote Fetch Failure

Fetch the resource yourself with an allowlisted client, timeout, redirect
policy, and size limit. Then call `convert_response()`. Do not repeatedly retry
authentication or authorization failures.

## Permission Failure

Check that the process can read the input and create the output directory.
Never respond by widening permissions for unrelated paths.

## Batch Failure

The batch utility reports each failed file and exits nonzero when any conversion
fails. Fix the first reported dependency or input problem, then rerun with the
same file bound.

