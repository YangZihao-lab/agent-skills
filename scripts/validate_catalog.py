#!/usr/bin/env python3
"""Validate the unified Agent Skills catalog with no third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.json"
UPSTREAM_PATH = ROOT / "upstream-skills.json"
SKILLS_ROOT = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing required file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path.relative_to(ROOT)}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def frontmatter_name(skill_md: Path) -> str | None:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("'\"")
    return None


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_named_objects(
    errors: list[str],
    values: object,
    label: str,
) -> tuple[list[dict[str, object]], set[str]]:
    if not isinstance(values, list):
        fail(errors, f"catalog {label} must be a list")
        return [], set()

    objects: list[dict[str, object]] = []
    identifiers: set[str] = set()
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            fail(errors, f"{label[:-1]} #{index + 1} must be an object")
            continue
        identifier = value.get("id")
        if not isinstance(identifier, str) or not NAME_RE.fullmatch(identifier):
            fail(errors, f"invalid {label[:-1]} id at index {index}: {identifier!r}")
            continue
        if identifier in identifiers:
            fail(errors, f"duplicate {label[:-1]} id: {identifier}")
        identifiers.add(identifier)
        objects.append(value)
    return objects, identifiers


def main() -> int:
    errors: list[str] = []
    catalog = load_json(CATALOG_PATH)
    upstream = load_json(UPSTREAM_PATH)

    if not isinstance(catalog, dict):
        raise ValueError("catalog/skills.json must contain a JSON object")
    if catalog.get("schema_version") != 2:
        fail(errors, "catalog schema_version must be 2")

    domains, domain_ids = validate_named_objects(errors, catalog.get("domains"), "domains")
    subcategories, subcategory_ids = validate_named_objects(
        errors, catalog.get("subcategories"), "subcategories"
    )

    subcategory_domains: dict[str, str] = {}
    for subcategory in subcategories:
        subcategory_id = subcategory.get("id")
        domain = subcategory.get("domain")
        if not isinstance(subcategory_id, str):
            continue
        if domain not in domain_ids:
            fail(errors, f"subcategory {subcategory_id}: unknown domain {domain!r}")
            continue
        subcategory_domains[subcategory_id] = domain

    skills = catalog.get("skills")
    if not isinstance(skills, list):
        fail(errors, "catalog skills must be a list")
        skills = []

    upstream_entries = upstream.get("skills", []) if isinstance(upstream, dict) else []
    upstream_names = {
        item.get("name")
        for item in upstream_entries
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }

    catalog_names: set[str] = set()
    for index, item in enumerate(skills):
        if not isinstance(item, dict):
            fail(errors, f"skill #{index + 1} must be an object")
            continue

        name = item.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            fail(errors, f"invalid skill name at index {index}: {name!r}")
            continue
        if name in catalog_names:
            fail(errors, f"duplicate skill name: {name}")
        catalog_names.add(name)

        domain = item.get("domain")
        if domain not in domain_ids:
            fail(errors, f"{name}: unknown domain {domain!r}")

        subcategory = item.get("subcategory")
        if subcategory not in subcategory_ids:
            fail(errors, f"{name}: unknown subcategory {subcategory!r}")
        elif subcategory_domains.get(str(subcategory)) != domain:
            fail(
                errors,
                f"{name}: subcategory {subcategory!r} does not belong to domain {domain!r}",
            )

        rel_path = item.get("path")
        expected_path = f"skills/{name}"
        if rel_path != expected_path:
            fail(errors, f"{name}: path must be {expected_path!r}, got {rel_path!r}")
        skill_dir = ROOT / expected_path
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            fail(errors, f"{name}: missing {expected_path}/SKILL.md")
            continue

        declared_name = frontmatter_name(skill_md)
        if declared_name != name:
            fail(errors, f"{name}: SKILL.md frontmatter name is {declared_name!r}")

        ownership = item.get("ownership")
        upstream_record = skill_dir / "_UPSTREAM.json"
        if ownership == "first-party":
            if upstream_record.exists():
                fail(errors, f"{name}: first-party skill must not contain _UPSTREAM.json")
        elif ownership == "mirrored-upstream":
            if not upstream_record.is_file():
                fail(errors, f"{name}: mirrored skill is missing _UPSTREAM.json")
            if name not in upstream_names:
                fail(errors, f"{name}: mirrored skill is not listed in upstream-skills.json")
        else:
            fail(errors, f"{name}: ownership must be first-party or mirrored-upstream")

        contains_scripts = (skill_dir / "scripts").is_dir()
        if item.get("contains_scripts") is not contains_scripts:
            fail(
                errors,
                f"{name}: contains_scripts={item.get('contains_scripts')!r} but filesystem is {contains_scripts}",
            )

        if item.get("invocation") not in {"explicit", "implicit-eligible"}:
            fail(errors, f"{name}: invalid invocation policy")

        platforms = item.get("platforms")
        if not isinstance(platforms, list) or not platforms or not all(
            isinstance(platform, str) and platform for platform in platforms
        ):
            fail(errors, f"{name}: platforms must be a non-empty string list")

    discovered = {
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    missing_catalog = discovered - catalog_names
    missing_directory = catalog_names - discovered
    for name in sorted(missing_catalog):
        fail(errors, f"skills/{name}: missing catalog entry")
    for name in sorted(missing_directory):
        fail(errors, f"catalog entry {name}: skill directory is missing")

    mirrored_catalog = {
        item.get("name")
        for item in skills
        if isinstance(item, dict) and item.get("ownership") == "mirrored-upstream"
    }
    for name in sorted(upstream_names - mirrored_catalog):
        fail(errors, f"upstream skill {name}: missing mirrored catalog entry")

    explainer_policy = ROOT / "skills" / "project-explainer" / "agents" / "openai.yaml"
    if explainer_policy.is_file():
        policy_text = explainer_policy.read_text(encoding="utf-8")
        if "allow_implicit_invocation: false" not in policy_text:
            fail(errors, "project-explainer: Codex implicit invocation must remain disabled")
    else:
        fail(errors, "project-explainer: missing agents/openai.yaml")

    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "skills": len(catalog_names),
                "domains": len(domain_ids),
                "subcategories": len(subcategory_ids),
                "first_party": sum(
                    1 for item in skills if isinstance(item, dict) and item.get("ownership") == "first-party"
                ),
                "mirrored_upstream": sum(
                    1
                    for item in skills
                    if isinstance(item, dict) and item.get("ownership") == "mirrored-upstream"
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"Catalog validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
