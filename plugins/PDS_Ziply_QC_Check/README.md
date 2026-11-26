# PDS Ziply QC Check

**QGIS plugin | Version 1.0.7 | Category: Vector**  
**Author:** Amlan Patnaik  
**Copyright:** Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.

PDS Ziply QC Check validates Ziply telecom GIS data against the configured legacy checks and the current 36-row field rulebook. Version 1.0.7 adds a strict, additive rulebook pass while retaining the existing QC workflow and report exports.

- **Plugin ID:** `PDS_Ziply_QC_Check`
- **QGIS compatibility declaration:** 3.22–4.99
- **Release archive:** `PDS_Ziply_QC_Check.1.0.7.zip`
- **Repository folder:** `plugins/PDS_Ziply_QC_Check/`
- **Repository homepage:** https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository/tree/main/plugins/PDS_Ziply_QC_Check
- **Issue tracker:** https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository/issues

## Version 1.0.7 — strict 36-row rulebook execution

The current `PDS_Ziply_QC_Field_Rules_Template` contains 36 field rules across seven layer types. Version 1.0.7 evaluates every configured rule row through the separate `field_rulebook_checks.py` module. The existing QC engine remains in place; the rulebook pass is additive.

| Layer | Rule rows | Rule coverage |
|---|---:|---|
| Equipment | 6 | Location, Mount Type, Physical Status, Type, Size, Category |
| Fiber Cable | 2 | Placement Type, Physical Status |
| Labor Units | 3 | Type, Surface Type, Category |
| Slackloop | 5 | Cable Size, Cable Name, Cable Length, Category, Comments / RSV Counts dependency |
| Span | 8 | Install Method, Size, Physical Status, Install Type, Category, ROW/PUE, Conduit Name, Count |
| Splice Closure | 6 | Case Size, Splice Closure ID, Mount Type, Type, Physical Status, Category |
| Structures | 6 | Structure Name, Type, Size, Physical Status, ROW/PUE, Category |
| **Total** | **36** | **All configured rule rows** |

## Strict completion and result rules

- Every rulebook row is evaluated for every feature in its matching eligible layer.
- Fields resolve using the physical field name or the QGIS field alias.
- The workbook's `Field Type` is checked. The configured rows require String except Slackloop `cable_size` and `cable_length`, which require Integer. A schema-type mismatch is reported at that rule row's configured severity.
- A missing configured target layer produces a `WARNING`; the run cannot silently pass with incomplete layer coverage.
- A missing configured field is reported using the severity assigned to that rule row, and that rule is marked as not evaluated.
- A present target layer with no features produces a `WARNING`, because no feature values were checked.
- A rule-engine execution exception produces an `ERROR` and marks the run `FAILED`.
- The overall result is calculated after the legacy checks and all 36 rulebook rows have contributed findings: `FAILED` when errors exist, `REVIEW` when warnings remain, and `PASSED` only when no errors or warnings remain.

## Conditional rules

- **Equipment Type:** FDH is required when the equipment naming field is blank; DBT is required when naming is populated.
- **Equipment Size:** DBT expects Size `2`; FDH accepts `144`, `288`, or `432`.
- **Slackloop Comments:** when `rsv_counts` is populated, Comments must be populated; when `rsv_counts` is blank, Comments must be blank. If `rsv_counts` is absent, a warning explains that the dependency could not be evaluated.
- **Span / Structures ROW/PUE:** `Right of Way` passes. `Public Utility Easement` and other values generate a warning with `RE-VERIFY` guidance.
- **Splice Closure ID:** validates `SP01`, `SP02`, etc. Duplicate IDs and sequence gaps from SP01 through the highest observed ID are warnings.
- **Structures Type / Size:** Type is `Flower Pot` when Size is blank; Size `2x3` or `36x60x36` requires Type `Handhole`. For Flower Pot, Size must be blank.

## Fiber Cable scope

The rulebook includes two Fiber Cable attribute checks:

- `placementtype` (alias `Placement Type`) must be `Underground`.
- `physical_status` (alias `Physical Status`) must be `New Build`.

The rulebook does **not** require separate Low Count, High Count, TotalActiveCounts, Active Count, or Dead Count fields. Existing Fiber Cable Count string-format, embedded Hub Number, range-order, cable-series, and Size = 1 blank-count exception checks remain part of the legacy QC engine.

## Legacy QC checks retained

The plugin continues to run its existing global Infinium ID / Hub Number checks, excluded layer-group filtering, Fiber Cable Count validation, Equipment naming / DPI / terminal / range checks, cable-series validation, and the existing setup/results workflow. The field-rulebook module appends findings to the existing results; it does not replace the legacy QC engine.

## Reports

The existing **Export Reports…** action generates:

- A formatted Excel workbook with an Overview worksheet and one worksheet per scanned layer.
- A searchable, filterable HTML report with print / Save as PDF support.
- A CSV copy.

Report metadata includes the overall QC result and rulebook coverage counts, including configured rules, field values checked, field types checked / mismatches, missing fields, missing layers, and empty layers.

## Data handling

The plugin reads the current QGIS project layers and feature attributes for validation and reporting. The supplied plugin documentation states that it does not update source feature attributes or geometries. Review the report findings before making any separate data corrections.

## Compatibility

The package metadata declares **QGIS 3.22 through 4.99** and the source includes Qt 5 / Qt 6 compatibility handling. This is a declared compatibility target, not a guarantee that every QGIS build or future version has been runtime-tested. Validate the plugin in the actual QGIS deployment before production use.

## Installation

### Install from ZIP

1. Download `PDS_Ziply_QC_Check.1.0.7.zip`.
2. In QGIS, open **Plugins → Manage and Install Plugins… → Install from ZIP**.
3. Select the downloaded archive.
4. Enable **PDS Ziply QC Check** if QGIS does not enable it automatically.

### Install through AMLAN-X

Add this repository URL in QGIS Plugin Manager if it is not already configured:

`https://amlanpatnaik001.github.io/amlanx-qgis-plugin-repository/plugins.xml`

Then search for **PDS Ziply QC Check** and install the available release.

## Repository release layout

The AMLAN-X repository expects the directory name, archive filename prefix, and internal plugin folder to match the plugin ID:

```text
plugins/
└── PDS_Ziply_QC_Check/
    ├── PDS_Ziply_QC_Check.1.0.7.zip
    └── README.md
```

The ZIP must contain exactly one top-level `PDS_Ziply_QC_Check/` folder with `metadata.txt` directly inside it.

## Support and issue reporting

For plugin-specific issues, include the plugin version, QGIS version, affected layer name, exact QC check, and a sanitized error message or report excerpt. Do not attach confidential customer data, credentials, or private production datasets.

- **Repository:** https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository
- **Plugin folder:** https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository/tree/main/plugins/PDS_Ziply_QC_Check
- **Issues:** https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository/issues

---

**Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.**
