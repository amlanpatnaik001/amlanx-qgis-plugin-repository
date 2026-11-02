# Slackloop Auto Naming

**Version:** 1.0.4  
**Category:** Vector  
**Author:** Amlan Patnaik

## Description

Automatically populates Slackloop cable names and sizes
from eligible Fiber Cable features.

## Features

- Automatically identifies eligible F2 cables.
- Copies Fiber Cable.naming to Slackloop.cable_name.
- Copies Fiber Cable.size to Slackloop.cable_size.
- Supports cable_category and categoy fallback.
- Uses natural ascending cable naming order.
- Configurable spatial tolerance.
- Progress reporting and cancellation.
- Detailed error reporting and diagnostics.
- PyQt5 and PyQt6 compatibility improvements.

## Compatibility

- QGIS 3.28–3.99
- QGIS 4.x compatibility target
- Qt5 / PyQt5
- Qt6 / PyQt6

## Changelog – v1.0.4

- Improved QGIS 3 and QGIS 4 compatibility.
- Added Qt5 and Qt6 compatibility handling.
- Improved geometry and CRS handling.
- Improved spatial matching performance.
- Added safer cancellation and error handling.
- Preserved existing telecom naming logic.

Copyright © Amlan Patnaik @2077.
All rights reserved.
