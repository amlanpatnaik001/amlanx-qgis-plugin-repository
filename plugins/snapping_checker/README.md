# Snapping Checker

**QGIS plugin · Version 3.2.5**  
**Author:** Amlan Patnaik  
**Copyright:** Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.

Snapping Checker provides telecom/fiber-network snapping quality checks, custom layer-to-layer workflows, and a dedicated **Line Alignment Offset (`LINE_OFFSET`)** tool.

## What's new in 3.2.5

The first toolbar action is now **Line Alignment Offset (`LINE_OFFSET`)**. It opens a focused One-to-Many dialog instead of the generic two-layer snapping dialog.

- Choose one source line layer and one or more target line layers.
- Optionally check selected features only on the source and/or target.
- Set the maximum offset distance and minimum offset precision.
- Create only `LINE_OFFSET` point findings and their matching **Gap connectors**.
- Gap connectors are styled as a red line with endpoint markers where supported by the active QGIS symbology API.

The original two-layer Processing algorithm remains available from the **Snapping QC** Processing provider. The other toolbar workflows remain available.

## Features

### 1. Line Alignment Offset (`LINE_OFFSET`)

The first toolbar button checks whether a source line path is consistently separated from nearby target linework along its length. The tool samples points along the source geometry between its stored vertices, finds the nearest target position, and records the maximum qualifying separation for each source/target feature pair.

A finding is reported when multiple interior samples are farther apart than the configured precision and no farther apart than the configured maximum offset distance. This is intended to identify line-path misalignment, not just endpoint gaps.

The dedicated tool:

- Accepts line geometry layers only.
- Uses One-to-Many selection: one source layer against one or more target layers.
- Supports selected-features-only filtering for both sides.
- Transforms target geometries into the source layer CRS before measuring.
- Creates point findings with `status=LINE_OFFSET` and matching connector features.
- Adds results to a separate QGIS project group; it does not edit source features.

**Distance units:** The maximum offset distance and precision use the source layer CRS map units. For a geographic CRS, map units are degrees. Choose a suitable projected CRS when you need distances in linear units.

### 2. Other snapping workflows

The plugin also retains these actions:

- **Check All Layers (fiber network):** the original telecom/fiber rule-set check.
- **Custom Check (One-to-Many):** one source layer against multiple target layers.
- **Custom Check (Many-to-Many):** multiple source layers against multiple target layers.
- **Original two-layer Processing algorithm:** available in the **Snapping QC** Processing provider.

The custom One-to-Many and Many-to-Many workflows run the original two-layer checker for each selected source/target pair. They can also include the optional `LINE_OFFSET` detection. Empty outputs and successful `SNAPPED` records are suppressed from the custom error results.

## Output fields

The dedicated `Line Alignment Offset points` and `Gap connectors` layers include these fields:

| Field | Meaning |
|---|---|
| `rule` | Detection rule; `LINE_ALIGNMENT` for this check |
| `status` | Finding status; `LINE_OFFSET` |
| `src_layer`, `src_fid` | Source layer name and feature ID |
| `tgt_layer`, `tgt_fid` | Target layer name and feature ID |
| `vtx_role` | `SEGMENT` for an interior line-path sample |
| `vtx_index` | `-1` for the sampled segment finding |
| `distance` | Maximum qualifying separation in source CRS map units |
| `near_x`, `near_y` | Coordinates of the nearest target position in the source CRS |
| `note` | Human-readable description of the detected offset |

The point marks the sampled source location with the maximum qualifying separation. Its connector joins that location to the nearest target location.

## Requirements and compatibility

- QGIS metadata declares `qgisMinimumVersion=3.28` and `qgisMaximumVersion=4.99`.
- The wrapper includes Qt5/Qt6 and legacy/scoped geometry-enum compatibility handling.
- The supplied original compiled snapping and licence engines are available for **Python 3.9, 3.10, 3.11, 3.12 and 3.13**.
- QGIS must be using one of those Python minor versions to load the compiled engines. The Python installed separately on Windows does not determine this; the relevant version is the Python bundled with QGIS.
- A valid product key is required to run the tools. Use **Snapping Checker → Enter / Update License…** to enter a key or load a `.lic` file.

Although the metadata declares QGIS 3.28–4.99 and compatibility fallbacks are included, this release has **not been verified in a live QGIS session across every QGIS/Python combination**. In particular, a QGIS build bundled with Python 3.14 or later needs matching compiled engine builds before the plugin can load its original algorithms.

## Installation in QGIS

1. Download `snapping_checker_3.2.5_qgis_install.zip` from the GitHub release assets.
2. Open QGIS and go to **Plugins → Manage and Install Plugins…**.
3. Select **Install from ZIP**.
4. Browse to the downloaded ZIP and install it.
5. Enable **Snapping Checker** if QGIS does not enable it automatically.
6. Activate the plugin with your product key when prompted.
7. Use the first toolbar button for **Line Alignment Offset (`LINE_OFFSET`)**.

## Install from a Git checkout

The repository root contains the QGIS plugin files. Clone or copy the repository into a QGIS profile's `python/plugins/snapping_checker` directory, then restart QGIS and enable **Snapping Checker** in the Plugin Manager.

Keep the compiled `snap_core_py*.pyc` and `license_py*.pyc` files in the plugin directory. They are required runtime components and are intentionally included in version control and release packages.

## Repository contents

- `metadata.txt` — QGIS plugin metadata and Plugin Manager changelog.
- `__init__.py`, `plugin.py`, `compat.py` — plugin entry point and Python wrapper.
- `snap_core_py*.pyc`, `license_py*.pyc` — supplied compiled runtime modules for Python 3.9–3.13.
- `icon*.svg` — toolbar and provider icons.
- `CHANGELOG.md` — release history.
- `COPYRIGHT.txt` — copyright and component-preservation notes.

## Reporting issues

When reporting a problem, include:

- QGIS version (from **Help → About**).
- Python version used by that QGIS installation (`import sys; print(sys.version)` in the QGIS Python Console).
- Operating system.
- The workflow used and the exact steps to reproduce the issue.
- Any relevant messages from the Snapping Checker Log or QGIS Log Messages panel.

Do not attach private network data, credentials, product keys, or licence files to a public issue.

## Copyright and licensing

Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.

The supplied compiled snapping and licence components are retained from the provided source package and have not been modified or reconstructed in this release. Their original ownership and applicable terms remain in force. No open-source licence is granted by this repository; contact the copyright holder for permission to use, modify, or redistribute the plugin.
