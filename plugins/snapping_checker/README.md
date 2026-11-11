# AMLAN-X Snapping Checker

**Plugin:** Snapping Checker  
**Version:** 3.2.1  
**Plugin ID:** `snapping_checker`  
**Category:** Vector  
**Author:** Amlan Patnaik

---

## 1. Overview

Snapping Checker is a QGIS quality-control plugin designed to identify snapping errors, connectivity problems, geometry misalignment, overshoots, crossings and other potential issues in vector network data.

It provides four checking workflows:

1. Two-Layer Snapping Check
2. All-Layer Fibre Network Check
3. Custom One-to-Many Check
4. Custom Many-to-Many Check

The plugin preserves the original compiled snapping algorithms and licence system while providing additional custom layer-selection workflows and improved result handling.

## 2. Main Features

### A. Two-Layer Snapping Check

Run the original snapping validation algorithm against one source layer and one target layer.

Available checks and parameters are inherited from the original snapping algorithm.

### B. All-Layer Fibre Network Check

Run the original fibre-network quality-control algorithm across the supported network layers.

The original telecom-specific validation logic is retained.

### C. Custom One-to-Many Check

Select one source layer and multiple target layers.

The plugin runs the original two-layer checker sequentially for every selected source-target pair.

**Example:**

- Source: Fibre Cable
- Targets: Equipment, Slackloop, Splice Closure, Structures and Span

### D. Custom Many-to-Many Check

Select multiple source layers and multiple target layers.

Every selected source is checked against every selected target.

For example, three source layers and four target layers produce twelve source-target checks.

The dialog provides:

- Multiple layer selection.
- Select All.
- Clear Selection.
- One-to-Many / Many-to-Many selection.
- Original snapping parameter controls.
- Sequential processing.
- Progress reporting.
- Cancellation.
- Per-pair error reporting.

## 3. Snapping Validation Options

The original snapping controls are retained, including:

- Endpoint-only or all-vertex checking.
- Target vertex or edge checking.
- Snapping tolerance.
- Precision.
- Overshoot detection.
- Self-loop checking.
- Crossing and overlap checking.
- Selected-features-only processing.
- Optional `NOT_CONNECTED` and `SNAPPED` outputs.

The exact available parameters depend on the selected workflow and original processing algorithm.

## 4. Line-to-Line Path Alignment

Version 3.2.1 includes additional line-path alignment checking between existing vertices.

### LINE_OFFSET detection

The checker samples line geometry between stored vertices and identifies potential path misalignment.

A `LINE_OFFSET` finding indicates that interior samples exceed the configured precision while remaining within the configured search tolerance.

The result can include:

- Offset identification.
- A nearest-point connector.
- Maximum sampled separation.

**Important:** This check assumes that the selected line features are intended to follow the same path. Nearby parallel utilities may be flagged when they fall within the selected tolerance. Review these results before correcting network geometry.

## 5. Result Management

Version 3.2.1 improves how custom-check results are presented.

- Empty error layers are not added.
- Empty connector layers are suppressed.
- Correctly snapped `SNAPPED` records are excluded from custom error results.
- Empty result groups are removed when every selected pair is clean.
- Results are organised into timestamped QGIS layer-tree groups.
- Existing results are retained if a subsequent pair fails or processing is cancelled.
- Custom workflows do not edit source geometries or attributes.

Each failed source-target pair is reported separately, allowing other pairs to continue processing.

## 6. Original Engine and Licence Integrity

The following original components are preserved:

- Original two-layer snapping algorithm.
- Original all-layer fibre-network algorithm.
- Original compiled snapping engine modules.
- Original compiled licence and activation modules.
- Original algorithm logic and licence verification.

The custom workflows reuse the original two-layer checker rather than replacing its underlying snapping implementation.

No external Python dependencies are introduced by the custom workflow.

## 7. Compatibility

**Declared QGIS compatibility range:**

- QGIS 3.28 and later QGIS 3 releases.
- QGIS 4.x, subject to compatible runtime dependencies.
- Qt5 / PyQt5 builds where matching compiled modules are available.
- Qt6 / PyQt6 builds where matching compiled modules are available.

**Python compiled-module requirements:**

The supplied compiled snapping and licence modules are available for these Python minor versions:

- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

Actual compatibility depends on the Python version bundled with the QGIS installation and the availability of the matching compiled module.

QGIS 4 compatibility must be verified against the specific QGIS and Python runtime. A successful installation or ZIP validation does not guarantee that every compiled component will load.

## 8. Installation

### Install through AMLAN-X Repository

1. Open QGIS.
2. Navigate to **Plugins → Manage and Install Plugins**.
3. Open the **Settings** tab.
4. Ensure the AMLAN-X repository is enabled.
5. Reload all plugin repositories.
6. Search for **Snapping Checker**.
7. Select the available version and click Install.

### Install from ZIP

1. Open **Plugins → Manage and Install Plugins**.
2. Select **Install from ZIP**.
3. Choose the Snapping Checker ZIP package.
4. Complete installation.
5. Restart QGIS if an older version is already loaded.

### Repository URL

`https://amlanpatnaik001.github.io/amlanx-qgis-plugin-repository/plugins.xml`

## 9. Changelog

### Version 3.2.1 — Focused Line QC and Clean Results

- Suppressed empty error and connector layers in custom workflows.
- Excluded correctly snapped `SNAPPED` records from custom results.
- Removed empty result groups when all selected pairs are clean.
- Added line-path alignment sampling between existing vertices.
- Added `LINE_OFFSET` findings.
- Added nearest-point connectors and maximum sampled separation.
- Improved temporary output resolution to prevent accidental reuse of another pair's result layer.
- Preserved original compiled snapping and licence modules.

### Version 3.2.0 — Custom Layer Edition

- Added Custom Check (One-to-Many).
- Added Custom Check (Many-to-Many).
- Added multi-layer selection.
- Added Select All and Clear controls.
- Added sequential execution.
- Added progress display and cancellation.
- Added per-pair error handling.
- Added timestamped result groups.
- Preserved original snapping algorithms and licence system.
- Added coordinated toolbar and menu icons.

## 10. Troubleshooting

### Plugin does not appear in QGIS

- Check whether the AMLAN-X repository is enabled.
- Reload all plugin repositories.
- Check the QGIS and Python versions.
- Verify that a matching compiled module is available.
- Review the QGIS Log Messages panel.

### Compiled module import failure

The original compiled modules require a matching Python minor version. A mismatch between the module build and the Python runtime can prevent the plugin from loading.

### Unexpected snapping results

- Verify source and target layer selection.
- Review snapping tolerance and precision.
- Confirm the coordinate reference systems.
- Check whether the selected lines are intended to follow the same path.
- Review `LINE_OFFSET` findings before making geometry corrections.

### Missing or empty output groups

Custom workflows suppress empty result layers. If all selected source-target pairs are clean, the temporary result group is removed.

## 11. Support

Report issues through the AMLAN-X GitHub repository:

https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository/issues

When reporting an issue, include:

- Snapping Checker version.
- QGIS version.
- Python runtime version.
- Source and target geometry types.
- Selected checking workflow.
- Exact error message.
- Relevant QGIS Log Messages output.

Remove confidential project information and database credentials before sharing diagnostic logs.

---

## Copyright

**Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.**

All original compiled engines, licence components and third-party notices retain their respective existing ownership and licence terms.

**AMLAN-X / GIS TOOLS**  
Maintained by Amlan Patnaik.
