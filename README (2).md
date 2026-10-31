# AMLAN-X QGIS Plugin Repository

A public QGIS plugin repository hosted with GitHub Pages. It includes:
- `plugins.xml` generated from ZIPs in `plugins/`
- a public web catalogue at `/`
- QGIS Plugin Manager compatibility
- GitHub Actions validation and index generation

> **Public means public:** anyone can browse, download and install every plugin ZIP in this repository. Do not publish client data, credentials, internal endpoints, proprietary code, or plugins you are not authorized to distribute.

## 1. Create the GitHub repository

Create a **public** repository named `amlanx-qgis-plugin-repository` under your GitHub account.
Upload the contents of this starter kit to the repository root (not the containing folder).

## 2. Enable GitHub Pages

In GitHub:
1. Open **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Save.

The included workflow deploys the web catalogue and plugin repository to Pages after each push to `main`.

## 3. Add a plugin

For each QGIS plugin, create a folder under `plugins/` named exactly as the plugin's import folder / plugin ID:

```text
plugins/
  your_plugin_id/
    your_plugin_id/
      __init__.py
      metadata.txt
      ...
```

The folder directly inside the ZIP must be the plugin folder. For example, the ZIP should contain `your_plugin_id/metadata.txt`, not an extra outer folder.

Then create a ZIP named `your_plugin_id-1.0.0.zip` and upload it to:

```text
plugins/your_plugin_id/your_plugin_id-1.0.0.zip
```

The generator scans `plugins/<plugin_id>/*.zip`, reads `metadata.txt`, validates the package, and emits `plugins.xml`. Keep previous versions if you want release history; the index advertises the highest version for each plugin ID.

## 4. Required metadata.txt fields

At minimum, include:

```ini
[general]
name=Your Plugin Name
qgisMinimumVersion=3.28
description=Short description of what the plugin does.
version=1.0.0
author=Your Name
email=you@example.com
about=More detailed plugin information.
tracker=https://github.com/YOUR_GITHUB_USERNAME/amlanx-qgis-plugin-repository/issues
repository=https://github.com/YOUR_GITHUB_USERNAME/amlanx-qgis-plugin-repository
homepage=https://YOUR_GITHUB_USERNAME.github.io/amlanx-qgis-plugin-repository/
category=Plugins
experimental=False
deprecated=False
```

Use a unique plugin folder / plugin ID. Confirm each plugin's license and permission to publish before making it public.

## 5. Install in QGIS

After the first successful Pages deployment, add this repository in QGIS:

**Plugins → Manage and Install Plugins → Settings → Add**

Name:
`AMLAN-X Public QGIS Repository`

URL:
`https://YOUR_GITHUB_USERNAME.github.io/amlanx-qgis-plugin-repository/plugins.xml`

Replace `YOUR_GITHUB_USERNAME` with your GitHub username. QGIS will then list plugins and offer upgrades when a higher version is published.

## 6. Publish an update

1. Increase `version=` in the plugin's `metadata.txt`.
2. Build a new ZIP with the correct top-level plugin folder.
3. Upload the ZIP under `plugins/<plugin_id>/`.
4. Commit and push to `main`.
5. GitHub Actions validates packages, rebuilds `plugins.xml`, and deploys Pages.

The admin dashboard is a public catalogue / release overview. Publishing is intentionally done through authenticated GitHub commits, not by embedding a GitHub token in browser JavaScript.

## 7. Local validation

Run from the repository root:

```powershell
py -3 -m pip install packaging
py -3 scripts/build_repository.py --root . --base-url https://YOUR_GITHUB_USERNAME.github.io/amlanx-qgis-plugin-repository
```

This writes `site/plugins.xml` and `site/catalog.json`.

## Security and release policy

- Never put a Personal Access Token (PAT) in `index.html`, JavaScript, or a public workflow file.
- Treat every plugin ZIP as public and downloadable.
- Review plugin source, licenses, third-party dependencies, and metadata before publishing.
- GitHub Pages is static hosting; it does not provide private access control.
- This is a public distribution repository, not a private/internal repository.
