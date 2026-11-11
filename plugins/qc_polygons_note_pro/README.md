QC Polygons Note Pro
Version: 1.0.7
Plugin ID: qc_polygons_note_pro
Author: Amlan Patnaik
Category: Vector
Overview
Generate future-reserve notes for selected QC Polygons using data from FDA Boundaries, Sites, Equipment, and Slack loop layers.
Data sources
- QC Polygons: selected polygons to process.
- FDA Boundaries: infinium_id supplies the H-number.
- Sites: house_number and street_name supply service addresses. Grouping uses the exact street_name value and preserves every Site record.
- Equipment: location, address, hh_address, or handhole_address supplies the HH address when an Equipment feature intersects the polygon.
- Slack loop: rsv_counts supplies the reserved fiber range.
Usage
1. Load the required layers.
2. Select one or more QC Polygons features.
3. Run Plugins → QC Polygons Note Pro → Generate QC Polygon Notes.
4. Review generated notes and warnings.
5. Copy notes or confirm optional write-back to the comments field.
Compatibility
- Declared QGIS range: 3.28–4.99.
- Uses the QGIS-provided qgis.PyQt abstraction.
- Includes QAction Qt5/Qt6 import handling.
- Uses scoped QGIS geometry enums with legacy fallbacks.
This is a compatibility target, not a claim of runtime testing on every historical or future QGIS build. Test in the exact QGIS version deployed in your environment.
Changelog
1.0.7
- Updated polygon geometry enum resolution for current QGIS 4 / PyQt6 APIs.
- Retained QGIS 3.28+ compatibility fallbacks.
- Added changelog metadata for QGIS Plugin Manager.
- Preserved all note-generation and data-processing logic.
- Added copyright and release documentation.
1.0.6
- Added Qt5 / Qt6 QAction import compatibility.
- Added QGIS 3 / QGIS 4 layer and geometry enum compatibility.
- Added toolbar icon.
Copyright
Copyright Amlan Patnaik @2077 All copyrights are reserved everywhere.
