
#!/usr/bin/env python3
"""
AMLAN-X QGIS Plugin Repository Builder

Validates plugin ZIP archives and generates:
    - site/plugins.xml
    - site/catalog.json
    - site/stats.json

Maintained by Amlan Patnaik.
"""

from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
import zipfile

from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from xml.etree.ElementTree import (
    Element,
    SubElement,
    ElementTree,
    indent,
)

from packaging.version import Version, InvalidVersion


# ============================================================
# CONFIGURATION
# ============================================================

REQUIRED_FIELDS = (
    "name",
    "version",
    "description",
    "qgisminimumversion",
)

DEFAULT_AUTHOR = "Amlan Patnaik"


# ============================================================
# GENERAL HELPERS
# ============================================================

def safe_text(value: str | None) -> str:
    """Return stripped text without None values."""
    return (value or "").strip()


def validate_base_url(url: str) -> str:
    """Validate repository base URL."""

    url = safe_text(url).rstrip("/")

    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or parsed.username
        or parsed.password
    ):
        raise ValueError(
            "Repository base URL must be a valid HTTPS URL."
        )

    return url


def safe_archive_path(filename: str) -> bool:
    """Prevent unsafe ZIP paths."""

    normalized = filename.replace("\\", "/")
    path = PurePosixPath(normalized)

    if path.is_absolute():
        return False

    if ".." in path.parts:
        return False

    return True


# ============================================================
# VERSION AND FILENAME VALIDATION
# ============================================================

def validate_filename(zip_path: Path, plugin_id: str) -> Version:
    """
    Expected filename:

        plugin_id.MAJOR.MINOR.PATCH.zip

    Examples:

        CRS_Guardian.2.5.1.zip
        TelecomSQLGenerator.1.1.0.zip
        save_all_layer_edits.2.0.0.zip
    """

    pattern = (
        rf"{re.escape(plugin_id)}"
        rf"\.(\d+(?:\.\d+){{1,3}}(?:[a-zA-Z0-9.+-]*)?)"
        rf"\.zip"
    )

    match = re.fullmatch(
        pattern,
        zip_path.name,
        flags=re.IGNORECASE,
    )

    if not match:
        raise ValueError(
            f"Invalid ZIP filename: {zip_path.name}. "
            f"Expected {plugin_id}.MAJOR.MINOR.PATCH.zip"
        )

    filename_version = match.group(1)

    try:
        return Version(filename_version)

    except InvalidVersion as exc:
        raise ValueError(
            f"Invalid version in ZIP filename: {filename_version}"
        ) from exc


# ============================================================
# METADATA EXTRACTION
# ============================================================

def parse_metadata(
    zf: zipfile.ZipFile,
    plugin_id: str,
) -> dict:
    """
    Extract and validate plugin metadata.

    Required structure:

        plugin_id/
            metadata.txt
    """

    # Check unsafe archive paths.
    for info in zf.infolist():

        if not safe_archive_path(info.filename):
            raise ValueError(
                f"Unsafe ZIP path detected: {info.filename}"
            )

    # Find root-level metadata.txt.
    candidates = []

    for filename in zf.namelist():

        normalized = filename.replace("\\", "/")

        parts = normalized.split("/")

        if (
            len(parts) == 2
            and parts[1].lower() == "metadata.txt"
        ):
            candidates.append(normalized)

    if len(candidates) != 1:
        raise ValueError(
            "ZIP must contain exactly one "
            "plugin_id/metadata.txt at its root."
        )

    meta_path = candidates[0]

    # Validate internal folder.
    folder = meta_path.split("/")[0]

    if folder != plugin_id:
        raise ValueError(
            f"Internal folder '{folder}' does not match "
            f"plugin folder '{plugin_id}'."
        )

    # Read metadata.
    parser = configparser.ConfigParser(
        interpolation=None
    )

    try:

        metadata_content = zf.read(meta_path).decode(
            "utf-8-sig"
        )

        parser.read_string(metadata_content)

    except Exception as exc:

        raise ValueError(
            f"Unable to read metadata.txt: {exc}"
        ) from exc

    if not parser.has_section("general"):
        raise ValueError(
            "metadata.txt does not contain [general]."
        )

    data = dict(parser.items("general"))

    # Validate required fields.
    missing = [
        field
        for field in REQUIRED_FIELDS
        if not safe_text(data.get(field))
    ]

    if missing:
        raise ValueError(
            "Missing required metadata fields: "
            + ", ".join(missing)
        )

    # Validate version.
    try:

        Version(data["version"])

    except InvalidVersion as exc:

        raise ValueError(
            f"Invalid metadata version: {data['version']}"
        ) from exc

    # Validate QGIS version compatibility.
    maximum = safe_text(
        data.get("qgismaximumversion")
    )

    if maximum:

        try:

            if Version(maximum) < Version(
                data["qgisminimumversion"]
            ):
                raise ValueError(
                    "QGIS maximum version cannot be "
                    "lower than minimum version."
                )

        except InvalidVersion as exc:

            raise ValueError(
                "Invalid QGIS compatibility version."
            ) from exc

    return data


# ============================================================
# XML HELPER
# ============================================================

def add_text(parent, tag: str, value: str):
    """Add XML element safely."""

    child = SubElement(parent, tag)
    child.text = safe_text(value)

    return child


# ============================================================
# MAIN REPOSITORY BUILDER
# ============================================================

def build(root: Path, base_url: str):

    plugins_dir = root / "plugins"
    site_dir = root / "site"

    site_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    base_url = validate_base_url(base_url)

    records = []
    errors = []

    # ========================================================
    # SCAN ALL PLUGIN ZIP ARCHIVES
    # ========================================================

    if plugins_dir.exists():

        zip_files = sorted(
            plugins_dir.glob("*/*.zip")
        )

        print(
            f"\nAMLAN-X: Found {len(zip_files)} ZIP archive(s)."
        )

        for zip_path in zip_files:

            plugin_id = zip_path.parent.name

            print(
                f"\nChecking: {zip_path.name}"
            )

            try:

                # 1. Validate filename.
                filename_version = validate_filename(
                    zip_path,
                    plugin_id,
                )

                # 2. Read and validate ZIP metadata.
                with zipfile.ZipFile(zip_path, "r") as zf:

                    meta = parse_metadata(
                        zf,
                        plugin_id,
                    )

                # 3. Compare filename and metadata versions.
                metadata_version = Version(
                    safe_text(meta["version"])
                )

                if filename_version != metadata_version:

                    raise ValueError(
                        f"Version mismatch: filename contains "
                        f"{filename_version}, but metadata.txt "
                        f"contains {metadata_version}."
                    )

                # 4. Build plugin record.
                record = {

                    "id": plugin_id,

                    "name": safe_text(
                        meta.get("name")
                    ),

                    "version": safe_text(
                        meta.get("version")
                    ),

                    "description": safe_text(
                        meta.get("description")
                    ),

                    "about": safe_text(
                        meta.get("about")
                    ),

                    "author": (
                        safe_text(meta.get("author"))
                        or DEFAULT_AUTHOR
                    ),

                    "email": safe_text(
                        meta.get("email")
                    ),

                    "qgis_minimum_version": safe_text(
                        meta.get("qgisminimumversion")
                    ),

                    "qgis_maximum_version": safe_text(
                        meta.get("qgismaximumversion")
                    ),

                    "category": (
                        safe_text(meta.get("category"))
                        or "Plugins"
                    ),

                    "experimental": (
                        safe_text(
                            meta.get("experimental", "False")
                        ).lower() == "true"
                    ),

                    "deprecated": (
                        safe_text(
                            meta.get("deprecated", "False")
                        ).lower() == "true"
                    ),

                    "filename": zip_path.name,

                    "download_url": (
                        f"{base_url}/plugins/"
                        f"{plugin_id}/{zip_path.name}"
                    ),

                    # No incorrect homepage fallback.
                    "homepage": safe_text(
                        meta.get("homepage", "")
                    ),

                    "tracker": safe_text(
                        meta.get("tracker", "")
                    ),

                    "repository": safe_text(
                        meta.get("repository", "")
                    ),
                }

                records.append(record)

                print(
                    f"  PASS: {plugin_id} "
                    f"v{metadata_version}"
                )

            except Exception as exc:

                error_message = (
                    f"{zip_path}: {exc}"
                )

                errors.append(error_message)

                print(
                    f"  FAIL: {error_message}",
                    file=sys.stderr,
                )

    else:

        print(
            "WARNING: plugins directory not found."
        )

    # ========================================================
    # STOP IF ANY ARCHIVE IS INVALID
    # ========================================================

    if errors:

        print(
            "\n========================================",
            file=sys.stderr,
        )

        print(
            "AMLAN-X PLUGIN VALIDATION FAILED",
            file=sys.stderr,
        )

        print(
            "========================================",
            file=sys.stderr,
        )

        for error in errors:

            print(
                f"- {error}",
                file=sys.stderr,
            )

        raise RuntimeError(
            f"{len(errors)} plugin archive(s) failed validation."
        )

    # ========================================================
    # SELECT LATEST VERSION PER PLUGIN
    # ========================================================

    latest = {}

    for item in records:

        plugin_id = item["id"]

        current_version = Version(
            item["version"]
        )

        if plugin_id not in latest:

            latest[plugin_id] = item

        else:

            existing_version = Version(
                latest[plugin_id]["version"]
            )

            if current_version > existing_version:

                latest[plugin_id] = item

    current = sorted(
        latest.values(),
        key=lambda x: x["name"].lower(),
    )

    # ========================================================
    # GENERATE QGIS plugins.xml
    # ========================================================

    xml_root = Element("plugins")

    for plugin in current:

        node = SubElement(
            xml_root,
            "pyqgis_plugin",
            {
                "name": plugin["name"],
                "version": plugin["version"],
                "plugin_id": plugin["id"],
            },
        )

        add_text(
            node,
            "description",
            plugin["description"],
        )

        add_text(
            node,
            "about",
            plugin["about"],
        )

        add_text(
            node,
            "version",
            plugin["version"],
        )

        add_text(
            node,
            "qgis_minimum_version",
            plugin["qgis_minimum_version"],
        )

        if plugin["qgis_maximum_version"]:

            add_text(
                node,
                "qgis_maximum_version",
                plugin["qgis_maximum_version"],
            )

        # Only add homepage if supplied in metadata.
        if plugin["homepage"]:

            add_text(
                node,
                "homepage",
                plugin["homepage"],
            )

        add_text(
            node,
            "file_name",
            plugin["filename"],
        )

        add_text(
            node,
            "author_name",
            plugin["author"],
        )

        add_text(
            node,
            "download_url",
            plugin["download_url"],
        )

        add_text(
            node,
            "experimental",
            "True" if plugin["experimental"] else "False",
        )

        add_text(
            node,
            "deprecated",
            "True" if plugin["deprecated"] else "False",
        )

        if plugin["tracker"]:

            add_text(
                node,
                "tracker",
                plugin["tracker"],
            )

        if plugin["repository"]:

            add_text(
                node,
                "repository",
                plugin["repository"],
            )

    indent(
        xml_root,
        space="  ",
    )

    ElementTree(xml_root).write(
        site_dir / "plugins.xml",
        encoding="utf-8",
        xml_declaration=True,
    )

    # ========================================================
    # GENERATE WEB CATALOGUE JSON
    # ========================================================

    catalog_path = site_dir / "catalog.json"

    catalog_path.write_text(
        json.dumps(
            current,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # ========================================================
    # GENERATE REPOSITORY STATISTICS
    # ========================================================

    stats = {

        "repository": "AMLAN-X",

        "maintainer": DEFAULT_AUTHOR,

        "plugin_count": len(current),

        "archive_count": len(records),

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(timespec="seconds"),

        "status": "success",
    }

    stats_path = site_dir / "stats.json"

    stats_path.write_text(
        json.dumps(
            stats,
            indent=2,
        ),
        encoding="utf-8",
    )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n========================================")
    print("AMLAN-X REPOSITORY BUILD SUCCESSFUL")
    print("========================================")

    print(
        f"Plugin archives validated : {len(records)}"
    )

    print(
        f"Unique plugins published : {len(current)}"
    )

    print(
        f"XML generated             : {site_dir / 'plugins.xml'}"
    )

    print(
        f"JSON generated            : {catalog_path}"
    )

    print(
        f"Statistics generated      : {stats_path}"
    )

    print("========================================\n")


# ============================================================
# COMMAND LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "AMLAN-X QGIS Plugin Repository Builder"
        )
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Repository root directory",
    )

    parser.add_argument(
        "--base-url",
        required=True,
        help="GitHub Pages repository URL",
    )

    args = parser.parse_args()

    try:

        build(
            Path(args.root).resolve(),
            args.base_url,
        )

    except Exception as exc:

        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )

        raise SystemExit(1)
