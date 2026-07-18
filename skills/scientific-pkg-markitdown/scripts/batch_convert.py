#!/usr/bin/env python3
"""Convert a bounded local directory tree to Markdown."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert local files to Markdown with MarkItDown.",
    )
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--max-files",
        type=int,
        default=1000,
        help="Maximum number of files to convert (default: 1000).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing Markdown outputs.",
    )
    return parser.parse_args()


def discover_files(input_dir: Path, output_dir: Path, max_files: int) -> list[Path]:
    if max_files < 1:
        raise ValueError("--max-files must be at least 1")
    if output_dir.is_relative_to(input_dir):
        raise ValueError("Output directory must be outside the input directory")

    files = [
        path
        for path in sorted(input_dir.rglob("*"))
        if path.is_file() and not path.is_symlink()
    ]
    if len(files) > max_files:
        raise ValueError(
            f"Found {len(files)} files, exceeding --max-files={max_files}",
        )
    return files


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve(strict=True)
    if not input_dir.is_dir():
        raise ValueError("Input path must be a directory")
    output_dir = args.output_dir.resolve()
    files = discover_files(input_dir, output_dir, args.max_files)

    from markitdown import MarkItDown

    converter = MarkItDown()
    failures = 0
    for source in files:
        relative = source.relative_to(input_dir)
        destination = output_dir / relative.parent / f"{relative.name}.md"
        if destination.exists() and not args.overwrite:
            print(f"skip existing: {destination}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(source, "r", encoding="utf-8", errors="ignore") as stream:
                stream.read(1)
            result = converter.convert_local(source)
            destination.write_text(result.text_content, encoding="utf-8")
            print(f"converted: {source} -> {destination}")
        except Exception as error:
            failures += 1
            print(f"failed: {source}: {error}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
