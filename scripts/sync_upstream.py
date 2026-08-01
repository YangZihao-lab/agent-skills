#!/usr/bin/env python3
"""Mirror pinned Agent Skills from GitHub into this repository.

The script executes no upstream code. It only fetches pinned Git commits and copies
files into skills/<name>/ while preserving source attribution.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


class SyncError(RuntimeError):
    pass


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        command = " ".join(args)
        raise SyncError(f"Command failed ({result.returncode}): {command}\n{result.stdout[-2000:]}")
    return result.stdout.strip()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Cannot read manifest: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("skills"), list):
        raise SyncError("Manifest must contain a skills array")
    return value


def safe_relative(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise SyncError(f"{label} must be a non-empty string")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise SyncError(f"{label} must be a safe relative path")
    return path


def copy_skill(repo_root: Path, spec: dict[str, Any], temp_root: Path) -> None:
    name = spec.get("name")
    source_repo = spec.get("source_repo")
    source_ref = spec.get("source_ref")
    if not all(isinstance(item, str) and item.strip() for item in (name, source_repo, source_ref)):
        raise SyncError("Each skill requires name, source_repo, and source_ref")

    destination_name = safe_relative(name, "name")
    if len(destination_name.parts) != 1:
        raise SyncError("Skill name must be a single directory name")
    source_path = safe_relative(spec.get("source_path", "."), "source_path")

    checkout = temp_root / destination_name
    checkout.mkdir(parents=True, exist_ok=False)
    run("git", "init", "--quiet", cwd=checkout)
    run("git", "remote", "add", "origin", f"https://github.com/{source_repo}.git", cwd=checkout)
    run("git", "fetch", "--quiet", "--depth", "1", "origin", source_ref, cwd=checkout)
    run("git", "checkout", "--quiet", "--detach", "FETCH_HEAD", cwd=checkout)
    resolved_commit = run("git", "rev-parse", "HEAD", cwd=checkout)

    source = (checkout / source_path).resolve()
    try:
        source.relative_to(checkout.resolve())
    except ValueError as exc:
        raise SyncError(f"Source path escaped checkout for {name}") from exc
    if not source.is_dir():
        raise SyncError(f"Source directory does not exist for {name}: {source_path}")
    if not (source / "SKILL.md").is_file():
        raise SyncError(f"Missing SKILL.md for {name}")

    destination = repo_root / "skills" / destination_name
    if destination.exists():
        shutil.rmtree(destination)

    excluded = {".git"}
    raw_exclude = spec.get("exclude", [])
    if not isinstance(raw_exclude, list) or not all(isinstance(item, str) for item in raw_exclude):
        raise SyncError(f"exclude must be a string array for {name}")
    excluded.update(raw_exclude)

    def ignore(_directory: str, entries: list[str]) -> set[str]:
        return {entry for entry in entries if entry in excluded}

    shutil.copytree(source, destination, ignore=ignore)

    license_value = spec.get("license_path")
    if isinstance(license_value, str) and license_value.strip():
        license_path = checkout / safe_relative(license_value, "license_path")
        if license_path.is_file() and not (destination / "LICENSE").exists():
            shutil.copy2(license_path, destination / "LICENSE.upstream")

    upstream = {
        "source_repo": source_repo,
        "source_ref": source_ref,
        "resolved_commit": resolved_commit,
        "source_path": source_path.as_posix(),
        "generated": True,
        "edit_policy": "Do not edit this mirrored directory directly; update upstream-skills.json and resync.",
    }
    (destination / "_UPSTREAM.json").write_text(
        json.dumps(upstream, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Synced {name} from {source_repo}@{resolved_commit}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync pinned upstream Agent Skills")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    manifest_path = (args.manifest or repo_root / "upstream-skills.json").resolve()
    manifest = load_manifest(manifest_path)
    (repo_root / "skills").mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="agent-skills-sync-") as temp:
        temp_root = Path(temp)
        for raw_spec in manifest["skills"]:
            if not isinstance(raw_spec, dict):
                raise SyncError("Each skills entry must be an object")
            copy_skill(repo_root, raw_spec, temp_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
