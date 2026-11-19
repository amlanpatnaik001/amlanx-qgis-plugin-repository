High-Res Map Exporter
AMLAN-X QGIS Plugin Repository · Version 1.1.0
Plugin ID: map_exporter
Author: Amlan Patnaik
Copyright: Copyright © 2077 Amlan Patnaik. All rights reserved.

Export the current QGIS map canvas as a high-resolution image while retaining the visible layer stack, map extent, coordinate reference system, symbology, labels and canvas background.
Version 1.1.0 highlights
- Resolution-aware DPI scaling keeps millimetre-based labels, symbols and line widths proportionate in large exports.
- Full HD, 4K UHD, 8K UHD and custom output dimensions.
- JPEG, PNG and TIFF output, with configurable JPEG quality.
- Optional aspect-ratio fitting expands the geographic extent rather than cropping the visible map.
- Remembers the last output folder and supports custom filename prefixes.
- Progress indication and cancellation where supported by the installed QGIS API.
- Validates the rendered image dimensions before saving.
- Includes an in-dialog copyright notice and project copyright metadata.
Install from the AMLAN-X repository
1. Open QGIS → Plugins → Manage and Install Plugins.
2. Open the Settings tab and add the AMLAN-X repository using this repository URL:
   https://amlanpatnaik001.github.io/amlanx-qgis-plugin-repository/plugins.xml
3. Return to All or Not installed, search for High-Res Map Exporter, and install it.
4. Start the plugin from its toolbar icon or the Plugins menu.
Install from ZIP
1. Download the release archive: [`map_exporter.1.1.0.zip`](map_exporter.1.1.0.zip).
2. In QGIS, open Plugins → Manage and Install Plugins → Install from ZIP.
3. Select the downloaded ZIP and confirm installation.
4. Enable High-Res Map Exporter in the plugin manager.
The archive contains exactly one top-level plugin folder named map_exporter, with metadata.txt inside it.
GitHub release location
Upload the versioned ZIP to this path in the AMLAN-X repository:

plugins/map_exporter/map_exporter.1.1.0.zip

This plugin folder's README should be stored as plugins/map_exporter/README.md.
- Plugin folder on GitHub
- Repository issue tracker
- AMLAN-X plugin repository website
Export workflow
1. Pan and zoom the QGIS map canvas to the area you want to export.
2. Open High-Res Map Exporter.
3. Choose Full HD, 4K, 8K or custom width and height.
4. Choose JPEG, PNG or TIFF and set the destination folder.
5. Keep Scale labels, symbols and line widths with export resolution enabled for most high-resolution exports.
6. Keep Expand the map extent to fit the output aspect ratio enabled to avoid losing map content at the edges.
7. Start the export and monitor progress. You can cancel while rendering if the installed QGIS renderer exposes cancellation support.
Recommended settings for telecom and GIS plans
- Use 8K UHD for large, detailed plan sheets when sufficient memory is available.
- Use PNG for crisp vector linework and text, JPEG for imagery-heavy maps with smaller file sizes, and TIFF when required by downstream workflows.
- Check the requested output dimensions and final image size before delivering exported maps.
Important limitations
- The exporter renders the current visible map area; zoom to the intended area before exporting.
- Increasing output dimensions does not create new source detail in satellite imagery or raster tiles.
- Large renders consume substantial memory. An uncompressed 8K RGBA buffer alone is approximately 127 MiB, before QGIS layer and intermediate render buffers.
- Raster tile detail and availability remain dependent on the source service.
- The supplied metadata declares QGIS 3.0 as the minimum version. Actual GUI/rendering behaviour should be tested in the precise QGIS build deployed; this package is not claimed to have been runtime-tested across every QGIS release.
Copyright and licensing
Copyright © 2077 Amlan Patnaik. All rights reserved.

This notice applies to the original High-Res Map Exporter project materials distributed in this package. It does not replace or override the licenses, notices or attribution requirements of QGIS, PyQGIS, Qt, Python, or other third-party components. Do not remove applicable third-party notices.
