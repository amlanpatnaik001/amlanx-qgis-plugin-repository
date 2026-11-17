#!/usr/bin/env python3
"""Validate AMLAN-X plugin ZIPs and build QGIS XML, web JSON and release stats."""
from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

try:
    from packaging.version import Version, InvalidVersion
except ImportError as exc:
    raise SystemExit("Missing dependency: run python -m pip install packaging") from exc

REQUIRED = ("name", "version", "description", "qgisminimumversion")
VERSION_FILE = re.compile(r"^[A-Za-z0-9_]+\\.(\\d+(?:\\.\\d+){1,3}(?:[a-zA-Z0-9.+-]*)?)\\.zip$")

def clean(value: str | None) -> str:
    return (value or "").strip()

def validate_public_url(value: str, field: str) -> str:
    value = clean(value)
    if not value:
        return ""
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f"{field} must be a public HTTPS URL")
    return value

def parse_metadata(zf: zipfile.ZipFile, plugin_id: str) -> dict:
    candidates = [
        n for n in zf.namelist()
        if n.replace("\\\\", "/").endswith("/metadata.txt")
        and len(n.replace("\\\\", "/").split("/")) == 2
    ]
    if len(candidates) != 1:
        raise ValueError("ZIP must contain exactly one root-level <plugin_id>/metadata.txt")
    meta_path = candidates[0]
    folder = meta_path.replace("\\\\", "/").split("/")[0]
    if folder != plugin_id:
        raise ValueError(f"internal folder '{folder}' must match plugin ID '{plugin_id}'")
    if any(info.filename.startswith("/") or ".." in Path(info.filename).parts for info in zf.infolist()):
        raise ValueError("ZIP contains an unsafe absolute or parent-traversal path")
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(zf.read(meta_path).decode("utf-8-sig"))
    if not parser.has_section("general"):
        raise ValueError("metadata.txt has no [general] section")
    data = dict(parser.items("general"))
    missing = [key for key in REQUIRED if not clean(data.get(key))]
    if missing:
        raise ValueError("missing metadata fields: " + ", ".join(missing))
    try:
        Version(data["version"])
    except InvalidVersion as exc:
        raise ValueError(f"invalid plugin version: {data['version']}") from exc
    if data.get("qgismaximumversion") and Version(data["qgismaximumversion"]) < Version(data["qgisminimumversion"]):
        raise ValueError("qgisMaximumVersion cannot be lower than qgisMinimumVersion")
    for key in ("homepage", "tracker", "repository"):
        data[key] = validate_public_url(data.get(key, ""), key)
    return data

def add_text(parent, tag, value):
    child = SubElement(parent, tag)
    child.text = clean(value)
    return child

def build(root: Path, base_url: str):
    plugins_dir, site_dir = root / "plugins", root / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    base_url = validate_public_url(base_url.rstrip("/"), "base URL")
    archives, errors = [], []
    if plugins_dir.exists():
        for zip_path in sorted(plugins_dir.glob("*/*.zip")):
            plugin_id = zip_path.parent.name
            try:
                match = VERSION_FILE.fullmatch(zip_path.name)
                if not match or not zip_path.name.startswith(plugin_id + "."):
                    raise ValueError("filename must be <plugin_id>.<version>.zip")
                with zipfile.ZipFile(zip_path) as zf:
                    meta = parse_metadata(zf, plugin_id)
                if Version(match.group(1)) != Version(meta["version"]):
                    raise ValueError("ZIP filename version does not match metadata.txt version")
                archives.append((zip_path, plugin_id, meta))
            except Exception as exc:
                errors.append(f"{zip_path}: {exc}")
    if errors:
        raise RuntimeError("Plugin package validation failed:\\n- " + "\\n- ".join(errors))

    latest = {}
    for zip_path, plugin_id, meta in archives:
        record = {
            "id": plugin_id, "name": clean(meta["name"]), "version": clean(meta["version"]),
            "description": clean(meta.get("description")), "about": clean(meta.get("about")),
            "author": clean(meta.get("author")) or "Amlan Patnaik",
            "email": clean(meta.get("email")), "qgis_minimum_version": clean(meta.get("qgisminimumversion")),
            "qgis_maximum_version": clean(meta.get("qgismaximumversion")),
            "category": clean(meta.get("category")) or "Plugins",
            "experimental": clean(meta.get("experimental", "False")).lower() == "true",
            "deprecated": clean(meta.get("deprecated", "False")).lower() == "true",
            "filename": zip_path.name,
            "download_url": f"{base_url}/plugins/{plugin_id}/{zip_path.name}",
            "homepage": clean(meta.get("homepage")) or base_url,
            "tracker": clean(meta.get("tracker")), "repository": clean(meta.get("repository")),
        }
        if plugin_id not in latest or Version(record["version"]) > Version(latest[plugin_id]["version"]):
            latest[plugin_id] = record
    current = sorted(latest.values(), key=lambda item: item["name"].lower())

    xml_root = Element("plugins")
    for p in current:
        node = SubElement(xml_root, "pyqgis_plugin", {
            "name": p["name"], "version": p["version"], "plugin_id": p["id"]
        })
        add_text(node, "description", p["description"])
        add_text(node, "about", p["about"])
        add_text(node, "version", p["version"])
        add_text(node, "qgis_minimum_version", p["qgis_minimum_version"])
        if p["qgis_maximum_version"]:
            add_text(node, "qgis_maximum_version", p["qgis_maximum_version"])
        add_text(node, "homepage", p["homepage"])
        add_text(node, "file_name", p["filename"])
        add_text(node, "author_name", p["author"])
        add_text(node, "download_url", p["download_url"])
        add_text(node, "experimental", "True" if p["experimental"] else "False")
        add_text(node, "deprecated", "True" if p["deprecated"] else "False")
        if p["tracker"]:
            add_text(node, "tracker", p["tracker"])
        if p["repository"]:
            add_text(node, "repository", p["repository"])

    indent(xml_root, space="  ")
    ElementTree(xml_root).write(site_dir / "plugins.xml", encoding="utf-8", xml_declaration=True)
    (site_dir / "catalog.json").write_text(json.dumps(current, indent=2), encoding="utf-8")
    stats = {
        "plugin_count": len(current),
        "archive_count": len(archives),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (site_dir / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(f"Validated {len(archives)} ZIP release(s); indexed {len(current)} latest plugin(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    try:
        build(Path(args.root).resolve(), args.base_url)
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
