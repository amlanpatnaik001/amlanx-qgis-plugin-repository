#!/usr/bin/env python3
"""Build a QGIS plugins.xml index and JSON catalogue from plugin ZIP archives."""
from __future__ import annotations

import argparse
import configparser
import html
import json
import re
import sys
import zipfile
from pathlib import Path
from packaging.version import Version, InvalidVersion
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

def safe_text(value: str) -> str:
    return (value or "").strip()

def parse_metadata(zf: zipfile.ZipFile, plugin_id: str) -> tuple[dict, str]:
    candidates = [
        n for n in zf.namelist()
        if n.replace("\\", "/").endswith("/metadata.txt")
        and len(n.replace("\\", "/").split("/")) == 2
    ]
    if not candidates:
        raise ValueError("ZIP must contain <plugin_id>/metadata.txt at its root")
    meta_path = candidates[0]
    folder = meta_path.replace("\\", "/").split("/")[0]
    if folder != plugin_id:
        raise ValueError(f"top-level folder '{folder}' must match plugin ID '{plugin_id}'")
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(zf.read(meta_path).decode("utf-8-sig"))
    if not parser.has_section("general"):
        raise ValueError("metadata.txt has no [general] section")
    data = dict(parser.items("general"))
    required = ("name", "version", "description", "qgisminimumversion")
    missing = [k for k in required if not safe_text(data.get(k, ""))]
    if missing:
        raise ValueError("missing metadata fields: " + ", ".join(missing))
    try:
        Version(data["version"])
    except InvalidVersion as exc:
        raise ValueError(f"invalid plugin version: {data['version']}") from exc
    return data, folder

def add_text(parent, tag, value):
    child = SubElement(parent, tag)
    child.text = safe_text(value)
    return child

def build(root: Path, base_url: str):
    plugins_dir = root / "plugins"
    site_dir = root / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    base_url = base_url.rstrip("/")
    records, errors = [], []

    if plugins_dir.exists():
        for zip_path in sorted(plugins_dir.glob("*/*.zip")):
            plugin_id = zip_path.parent.name
            try:
                with zipfile.ZipFile(zip_path) as zf:
                    meta, folder = parse_metadata(zf, plugin_id)
                version = safe_text(meta["version"])
                records.append({
                    "id": plugin_id,
                    "name": safe_text(meta["name"]),
                    "version": version,
                    "description": safe_text(meta.get("description", "")),
                    "about": safe_text(meta.get("about", "")),
                    "author": safe_text(meta.get("author", "")),
                    "email": safe_text(meta.get("email", "")),
                    "qgis_minimum_version": safe_text(meta.get("qgisminimumversion", "")),
                    "qgis_maximum_version": safe_text(meta.get("qgismaximumversion", "")),
                    "category": safe_text(meta.get("category", "Plugins")),
                    "experimental": safe_text(meta.get("experimental", "False")).lower() == "true",
                    "deprecated": safe_text(meta.get("deprecated", "False")).lower() == "true",
                    "filename": zip_path.name,
                    "download_url": f"{base_url}/plugins/{plugin_id}/{zip_path.name}",
                    "homepage": safe_text(meta.get("homepage", base_url)),
                    "tracker": safe_text(meta.get("tracker", "")),
                    "repository": safe_text(meta.get("repository", "")),
                })
            except Exception as exc:
                errors.append(f"{zip_path}: {exc}")

    if errors:
        raise RuntimeError("Plugin package validation failed:\n- " + "\n- ".join(errors))

    latest = {}
    for item in records:
        key = item["id"]
        if key not in latest or Version(item["version"]) > Version(latest[key]["version"]):
            latest[key] = item
    current = sorted(latest.values(), key=lambda x: x["name"].lower())

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
    print(f"Indexed {len(current)} plugin(s); retained {len(records)} version archive(s).")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--base-url", required=True)
    args = ap.parse_args()
    try:
        build(Path(args.root).resolve(), args.base_url)
    except Exception as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
