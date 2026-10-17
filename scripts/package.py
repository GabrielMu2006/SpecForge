#!/usr/bin/env python3
"""Build a reproducible, self-contained skill archive and verify its payload."""

import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import check

from check import require


def build(output_dir=None):
    metadata = check.validate()
    version = metadata["metadata"]["version"]
    output_dir = (Path(output_dir) if output_dir else check.ROOT / "dist").resolve()
    require(output_dir != check.SKILL.resolve() and check.SKILL.resolve() not in output_dir.parents,
            "Build output must be outside the runtime skill directory")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"specforge-{version}.zip"
    entries = {}
    for name in sorted(check.RUNTIME_FILES):
        entries[f"specforge/{name}"] = (check.SKILL / name).read_bytes()
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content)
    with ZipFile(destination) as archive:
        require(archive.testzip() is None, "ZIP integrity check failed")
        require(set(archive.namelist()) == set(entries), "Archive manifest mismatch")
        for name, content in entries.items():
            require(archive.read(name) == content, f"Archive content mismatch: {name}")
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    checksum = destination.with_suffix(".zip.sha256")
    checksum.write_text(f"{digest}  {destination.name}\n", encoding="utf-8")
    print(f"Built {destination.name}: {len(entries)} files, {destination.stat().st_size} bytes")
    print(f"SHA-256: {digest}")
    return destination


if __name__ == "__main__":
    build()
