#!/usr/bin/env python3
"""Create a metadata-only inventory of an already extracted PS2 disc folder.

This script is read-only, never uploads data and never extracts an ISO.
Keep the output PRIVATE: filenames, hashes and boot IDs may identify a game.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def boot_target(root: Path) -> dict[str, str | bool | None]:
    config = next(
        (p for p in root.iterdir() if p.is_file() and not p.is_symlink() and p.name.upper() == "SYSTEM.CNF"),
        None,
    )
    if config is None:
        return {"config": None, "raw_value": None, "executable_path": None, "exists": False}
    text = config.read_bytes()[:64 * 1024].decode("ascii", errors="replace")
    match = re.search(r"(?im)^\s*BOOT2?\s*=\s*(.*?)\s*$", text)
    if not match:
        return {"config": config.name, "raw_value": None, "executable_path": None, "exists": False}
    value = match.group(1).strip()
    normalized = re.sub(r"(?i)^cdrom0:\s*", "", value)
    normalized = normalized.split(";", 1)[0].replace("\\", "/").lstrip("/")
    # Reject travel outside the extracted folder; no target is opened here.
    pieces = [part for part in normalized.split("/") if part]
    path = "/".join(pieces) if pieces and all(p not in (".", "..") for p in pieces) else None
    return {"config": config.name, "raw_value": value, "executable_path": path, "exists": False}


def classify_file(path: Path, magic: bytes) -> str:
    ext = path.suffix.lower()
    if ext == ".irx":
        return "candidate IOP module"
    if magic.startswith(b"\x7fELF"):
        return "ELF signature"
    if ext == ".pss":
        return "candidate video stream"
    if ext in (".vag", ".ads"):
        return "candidate game audio"
    return "unclassified"


def scan_folder(root: Path, calculate_hash: bool) -> dict:
    root = root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("The input must be an already-extracted disc DIRECTORY, not an ISO file.")
    boot = boot_target(root)
    entries = []
    warnings = []
    for directory, subdirs, filenames in os.walk(root, topdown=True, followlinks=False):
        subdirs[:] = sorted(d for d in subdirs if not (Path(directory) / d).is_symlink())
        for filename in sorted(filenames):
            path = Path(directory) / filename
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            try:
                with path.open("rb") as fh:
                    magic = fh.read(4)
                entry = {
                    "path": relative,
                    "size_bytes": path.stat().st_size,
                    "header_hex": magic.hex(),
                    "type_guess": classify_file(path, magic),
                }
                if calculate_hash:
                    entry["sha256"] = sha256_file(path)
                entries.append(entry)
            except OSError as exc:
                warnings.append(f"{relative}: {type(exc).__name__} (unreadable)")
    entries.sort(key=lambda obj: obj["path"].casefold())
    if boot["executable_path"]:
        expected = str(boot["executable_path"]).casefold()
        boot["exists"] = any(item["path"].casefold() == expected for item in entries)
    return {
        "notice": "Private metadata-only inventory; no disc data uploaded or extracted.",
        "root_name": root.name,
        "boot": boot,
        "file_count": len(entries),
        "files": entries,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disc_directory", type=Path, help="Directory of ALREADY extracted PS2 disc files")
    parser.add_argument("--sha256", action="store_true", help="Calculate SHA-256 for each file; may take time")
    parser.add_argument("--output", type=Path, help="Write UTF-8 JSON to a private file (otherwise stdout)")
    args = parser.parse_args()
    try:
        data = scan_folder(args.disc_directory, args.sha256)
        serialized = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(serialized, encoding="utf-8")
            print(f"Inventory written: {args.output} ({data['file_count']} files)")
        else:
            sys.stdout.write(serialized)
    except (OSError, ValueError) as exc:
        print(f"Inventory failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
