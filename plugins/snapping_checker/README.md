Snapping Checker
Version: 3.2.2
Plugin ID: snapping_checker
Category: Vector
Author: Amlan Patnaik

Snapping Checker provides two-layer, all-layer fibre-network, custom One-to-Many and custom Many-to-Many snapping quality checks for QGIS vector layers.
Release package
- ZIP filename: snapping_checker.3.2.2.zip
- GitHub folder: plugins/snapping_checker/
- Plugin archive destination: plugins/snapping_checker/snapping_checker.3.2.2.zip
Features and workflows
1. Check Snapping (two layers) — runs the original Processing algorithm for one source and one target layer.
2. Check All Layers (fibre network) — runs the original fibre-network rule-set algorithm.
3. Custom Check (One-to-Many) — chooses one source layer and multiple target layers; the original two-layer checker runs once for each selected target.
4. Custom Check (Many-to-Many) — chooses multiple source and target layers; every selected source is checked against every selected target.
The custom workflows support the original snapping options, including endpoint/all-vertex mode, target vertex/edge mode, tolerance, precision, overshoot, self-loop checks, crossing/overlap checks, selected-features-only processing, and optional NOT_CONNECTED / SNAPPED outputs.
Result handling and safety
- Custom checks create error-point and connector layers only when actual errors/connectors exist.
- Correctly snapped SNAPPED records are suppressed from custom error results.
- Empty result groups are removed when all selected pairs are clean.
- Results are organised in a timestamped QGIS layer-tree group.
- Source layers are read-only in the custom workflows; they are not edited.
- Source-target pairs run sequentially. If one pair fails, remaining pairs continue and the failed pair is reported.
- Existing output layers from completed pairs are retained if a later pair fails or processing is cancelled.
- Line-to-line checks can sample between stored vertices to identify path misalignment (LINE_OFFSET). Nearby parallel utilities may be flagged if they fall within the chosen tolerance, so select tolerance carefully.
Compatibility
The package declares QGIS 3.28 through QGIS 4.x compatibility (qgisMinimumVersion=3.28, qgisMaximumVersion=4.99) and uses QGIS's qgis.PyQt abstraction with scoped/legacy geometry-enum handling.

The original compiled snapping and licence modules are supplied for these Python minor versions:
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13
At runtime the plugin must load the compiled core and licence module matching the Python minor version bundled with QGIS. QGIS builds using Python 3.14 or later are not supported by this archive unless matching compiled modules are supplied. QGIS versions earlier than 3.28 and QGIS 2.x are not supported.

The metadata compatibility range is a declaration, not proof of successful execution on every QGIS build. Test the plugin in the actual QGIS version and operating system before production use.
Installation through QGIS Plugin Manager
1. Open Plugins → Manage and Install Plugins.
2. Add or enable the AMLAN-X repository:
   https://amlanpatnaik001.github.io/amlanx-qgis-plugin-repository/plugins.xml
3. Reload plugin repositories.
4. Search for Snapping Checker and install or upgrade to version 3.2.2.
Alternatively, use Install from ZIP and select snapping_checker.3.2.2.zip.
Changelog — 3.2.2
- Added scoped Qgis.GeometryType resolution for modern QGIS 3 and QGIS 4.
- Retained the legacy QgsWkbTypes geometry-enum fallback for older supported QGIS 3 builds.
- Preserved the original compiled snapping and licence modules byte-for-byte.
- Preserved the two-layer, all-layer, One-to-Many and Many-to-Many workflows.
- Preserved line-alignment checks, result filtering, and licensing behaviour.
- Updated release metadata and compatibility documentation.
For earlier changes, see CHANGELOG.txt included in the plugin ZIP.
Copyright
Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.

The copyright notice applies to the first-party wrapper code, compatibility helper, custom layer dialog and runner, metadata, SVG icons, documentation and packaging. The original compiled snapping and licence modules are preserved from the supplied prior release and are not modified by this compatibility update. Retain any applicable third-party notices and licence terms.
Support and issue reports
When reporting a problem, include the Snapping Checker version, QGIS version, operating system, Python version bundled with QGIS, exact error message, reproduction steps, and relevant QGIS Log Messages. Remove credentials, internal endpoints, or client information before sharing logs.
