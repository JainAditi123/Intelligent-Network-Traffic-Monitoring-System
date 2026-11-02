"""
make_zip.py
-----------
Creates DDoS_Monitoring_Final.zip one level above the project folder.
Preserves subfolder structure. Excludes venv/, __pycache__/, and this script itself.
Safe to run multiple times (overwrites existing ZIP).
"""

import os
import zipfile
import pathlib

project_root = pathlib.Path(__file__).parent.resolve()
dest_zip     = project_root.parent / "DDoS_Monitoring_Final.zip"

EXCLUDE_DIRS  = {"venv", "__pycache__", ".git"}
EXCLUDE_FILES = {"make_zip.py", "make_submission_zip.ps1"}

print(f"Source : {project_root}")
print(f"Output : {dest_zip}")
print()

added = 0
skipped = 0

with zipfile.ZipFile(dest_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for fpath in sorted(project_root.rglob("*")):
        if not fpath.is_file():
            continue

        # Skip excluded directories anywhere in path
        parts = set(fpath.relative_to(project_root).parts)
        if parts & EXCLUDE_DIRS:
            skipped += 1
            continue

        # Skip excluded filenames
        if fpath.name in EXCLUDE_FILES:
            skipped += 1
            continue

        # Archive name: DDoS_Monitoring/subpath/file.ext
        arcname = "DDoS_Monitoring" / fpath.relative_to(project_root)
        size_kb = fpath.stat().st_size / 1000
        print(f"  Adding ({size_kb:>10.1f} KB)  {arcname}")
        zf.write(fpath, arcname)
        added += 1

zip_mb = dest_zip.stat().st_size / 1_000_000
print()
print(f"Done. {added} files added, {skipped} skipped.")
print(f"ZIP size : {zip_mb:.2f} MB")
print(f"Location : {dest_zip}")
