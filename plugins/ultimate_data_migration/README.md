# Ultimate Data Migration

**Version:** 1.0.0  
**Author:** Amlan Patnaik  
**Category:** Database  
**Minimum QGIS Version:** 3.34  
**Compatibility Target:** QGIS 3.34+ and QGIS 4.x

---

## 1. Overview

Ultimate Data Migration is an advanced QGIS plugin designed to migrate and synchronize features between multiple vector layers through a single batch-processing interface.

The plugin is particularly useful when transferring locally stored GIS data into PostgreSQL/PostGIS databases. Instead of migrating one layer at a time, users can configure multiple source-to-target layer pairs and execute them within one migration session.

For example, a telecom GIS project may contain several offline layers that need to be migrated to their corresponding online PostgreSQL layers.

### Example migration configuration

| Source Layer | Target Layer | Storage |
|---|---|---|
| Fiber_Cable_Offline | Fiber_Cable | OFFLINE → ONLINE |
| Equipment_Offline | Equipment | OFFLINE → ONLINE |
| Slackloop_Offline | Slackloop | OFFLINE → ONLINE |
| Splice_Closure_Offline | Splice_Closure | OFFLINE → ONLINE |
| Structures_Offline | Structures | OFFLINE → ONLINE |

Each migration pair has independent field mappings, storage information and processing options.

---

## 2. Core Features

### 2.1 Multiple Layer Migration

- Add multiple source-to-target migration pairs.
- Configure each pair independently.
- Enable or disable individual migration pairs.
- Remove unnecessary migration pairs.
- Automatically match similarly named source and target layers.
- Process multiple datasets in one batch.
- Prevent the same target layer from being used by multiple enabled pairs.

### 2.2 Automatic Storage Detection

The plugin identifies the storage/provider type of both source and target layers independently.

| Indicator | Description |
|---|---|
| OFFLINE | Local file-backed layers such as GeoPackage, Shapefile, SpatiaLite, GPX and delimited text. |
| ONLINE | PostgreSQL provider layers. |
| TEMPORARY | Temporary in-memory QGIS layers. |
| REMOTE | Other service or connection-based providers. |

The interface displays available file paths and connection information for both source and target layers.

Credential-like values are redacted from visible connection information.

**Important:** Storage classification identifies the provider type. It does not guarantee that a PostgreSQL server is reachable or that the current account has permission to write to it.

### 2.3 Advanced Field Mapping

Every migration pair has its own field mapping configuration.

Features include:

- Automatic mapping of fields with matching names.
- Manual source-to-target field selection.
- Ability to skip unnecessary fields.
- Default and constant values.
- Field type mismatch warnings.
- Independent field mapping for each layer pair.

### 2.4 Migration Modes

The plugin provides three migration modes.

**Insert Only**

Adds source features as new records in the target layer. This mode does not independently prevent duplicates.

**Upsert by Matching Key**

Checks whether a matching target record exists.

- Matching record found: update the existing record.
- No matching record found: insert a new record.
- Duplicate values in the target matching field: reject the migration during validation.

**Update Matching Features Only**

Updates records that have a matching key in the target layer. Unmatched source records are skipped rather than inserted.

For telecom datasets, UUID is generally preferable to mutable identifiers such as cable names when a stable unique identifier is available.

### 2.5 Geometry Management

- Transfer source geometries to target layers.
- Transform geometries when source and target CRS differ.
- Convert multipart geometries to singlepart in supported insert workflows.
- Remove Z and M dimensions where supported.
- Optionally update geometries of matched records.
- Preserve existing target values when mapped source attributes are NULL or empty, when the corresponding option is enabled.

### 2.6 UUID Management

The plugin supports automatic UUID generation for newly inserted features when the target layer contains a UUID field that has not been explicitly mapped.

For reliable synchronization, users should map existing source and target UUID fields when using key-based migration.

### 2.7 Batch Preview and Validation

Before processing, users can validate the configured migration pairs.

The preflight process reviews:

- Source and target layer selections.
- Field mapping configuration.
- Matching-field configuration.
- Duplicate target matching keys.
- Migration options.
- Selected-feature requirements.
- Other configuration errors.

A batch preview allows users to review the planned migration before starting the operation.

### 2.8 Progress and Reporting

- Migration progress display.
- Processing cancellation.
- Individual pair execution results.
- Migration report generation.
- Exportable execution reports.

### 2.9 Save and Load Configurations

Users can save migration configurations as JSON files and load them later.

Configurations preserve layer references, field mappings and processing options.

Layer IDs are project-specific. Always verify the selected layers after loading a configuration into a different QGIS project.

---

## 3. Typical Offline-to-Online Workflow

A common use case is transferring offline telecom edits to PostgreSQL.

1. Load the offline and PostgreSQL layers into QGIS.
2. Open Ultimate Data Migration.
3. Add the required migration pairs.
4. Verify the OFFLINE and ONLINE indicators.
5. Inspect the source and target paths.
6. Configure the individual field mappings.
7. Select the migration mode.
8. Configure UUID matching if using Upsert or Update.
9. Enable geometry updates when existing target geometries must be replaced.
10. Run Preview Batch.
11. Review validation results and resolve warnings or errors.
12. Run the migration.
13. Review the execution report.

The same batch can contain Fiber Cable, Equipment, Slackloop, Splice Closure, Structures and other supported vector layers.

---

## 4. Safety and Data Protection

The plugin includes several safeguards:

- Source features are retained. There is no automatic source-deletion option.
- Target layers already in edit mode are rejected to avoid committing someone else's pending target edits.
- Source-layer pending edits may be included in the migration and are identified through preview warnings.
- Preflight validation takes place before migration begins.
- Duplicate matching keys are checked during validation.
- Each target layer is committed separately.
- The plugin attempts to roll back a target layer when processing fails.

**Important limitations:**

A multi-layer batch is not one database-wide atomic transaction. Each target layer is committed separately.

Rollback behavior can vary by data provider. Always inspect the execution report and verify the destination data following an unsuccessful migration.

The plugin should initially be tested on copies of important datasets. Back up PostgreSQL tables and local data before using it in production.

---

## 5. QGIS Compatibility

The plugin declares:

- Minimum QGIS version: 3.34
- Maximum metadata version: 4.99
- QGIS 3.x compatibility target.
- QGIS 4.x compatibility target.
- Qt 5 / Qt 6 compatibility handling through QGIS Python abstractions.

Compatibility declarations do not guarantee that every QGIS build or provider combination has been runtime-tested.

Actual GUI and PostgreSQL acceptance testing should be performed on the QGIS versions used in the deployment environment.

---

## 6. Installation

1. Download the versioned plugin ZIP.
2. Open QGIS.
3. Navigate to **Plugins → Manage and Install Plugins**.
4. Select **Install from ZIP**.
5. Browse to the downloaded archive.
6. Install the plugin.
7. Enable Ultimate Data Migration in the Installed tab.
8. Open the plugin from the Plugins menu or toolbar.

---

## 7. Package Structure

```text
ultimate_data_migration/
│
├── __init__.py
├── metadata.txt
├── ultimate_data_migration.py
├── ultimate_data_migration_dialog.py
├── migration_engine.py
├── icon.svg
├── README.md
├── CHANGELOG.md
└── COPYRIGHT.txt
```

---

## 8. Release Information

**Current Version:** 1.0.0

See [CHANGELOG.md](CHANGELOG.md) for the version history and release changes.

---

## 9. Copyright

**Copyright © 2077 Amlan Patnaik. All rights reserved.**

Developed by Amlan Patnaik.

Unauthorized redistribution or modification is subject to the applicable software licence and copyright terms.

---

**Ultimate Data Migration | Amlan Patnaik**  
*Simplifying multi-layer GIS data migration.*
