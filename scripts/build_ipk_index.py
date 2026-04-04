#!/usr/bin/env python3

from __future__ import annotations

import gzip
import hashlib
import subprocess
from pathlib import Path


def run(*args: str, input_bytes: bytes | None = None) -> bytes:
    proc = subprocess.run(
        args,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"{' '.join(args)} failed: {stderr}")
    return proc.stdout


def list_members(path: Path) -> list[str]:
    output = run("bsdtar", "-tf", str(path)).decode("utf-8", "replace")
    return [line.strip() for line in output.splitlines() if line.strip()]


def extract_member(path: Path, member: str) -> bytes:
    return run("bsdtar", "-xOf", str(path), member)


def extract_control_text(path: Path) -> str:
    members = list_members(path)

    direct = [name for name in members if name.split("/")[-1] == "control"]
    for member in direct:
        try:
            return extract_member(path, member).decode("utf-8")
        except Exception:
            continue

    nested_archives = [name for name in members if name.split("/")[-1].startswith("control.tar")]
    for member in nested_archives:
        payload = extract_member(path, member)
        inner_list = run("bsdtar", "-tf", "-", input_bytes=payload).decode("utf-8", "replace")
        inner_members = [line.strip() for line in inner_list.splitlines() if line.strip()]
        for inner_member in inner_members:
            if inner_member.split("/")[-1] != "control":
                continue
            try:
                return run("bsdtar", "-xOf", "-", inner_member, input_bytes=payload).decode("utf-8")
            except Exception:
                continue

    preview = ", ".join(members[:20]) or "(none)"
    raise RuntimeError(f"control file not found in {path.name}; members={preview}")


def build_entry(path: Path) -> str:
    control = extract_control_text(path).strip()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    size = path.stat().st_size
    return (
        f"{control}\n"
        f"Filename: ./{path.name}\n"
        f"Size: {size}\n"
        f"SHA256sum: {digest}\n"
    )


def main() -> int:
    root = Path.cwd()
    packages = sorted(root.glob("*.ipk"))
    if not packages:
        raise SystemExit("No .ipk packages found")

    manifest = "\n".join(build_entry(path) for path in packages) + "\n"
    (root / "Packages").write_text(manifest, encoding="utf-8")
    with (root / "Packages.gz").open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as fh:
            fh.write(manifest.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
