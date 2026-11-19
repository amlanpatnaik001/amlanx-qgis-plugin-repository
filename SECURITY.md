# Security Policy

## About AMLAN-X Security

AMLAN-X is a QGIS plugin repository maintained by Amlan Patnaik. Security is important for the plugins, release archives, repository website, build scripts and GitHub Actions workflows distributed through this project.

**Copyright © 2077 Amlan Patnaik. All rights reserved.**

## Supported Versions

Because AMLAN-X contains multiple independently versioned QGIS plugins, security support is managed separately for each plugin.

| Component | Security Support |
|---|---|
| Latest published version of each plugin | Eligible for security fixes |
| Older archived plugin versions | Not guaranteed |
| Third-party libraries and dependencies | Subject to their respective maintainers' security policies |

Users are encouraged to install the latest available release of each plugin.

QGIS compatibility is defined separately in each plugin's `metadata.txt`. Compatibility declarations do not necessarily mean every QGIS version has been runtime-tested.

## Reporting a Security Vulnerability

**Please do not report exploitable security vulnerabilities through public GitHub Issues, Discussions or Pull Requests.**

Preferred reporting method:

1. Open the AMLAN-X repository on GitHub.
2. Navigate to **Security and quality → Advisories**.
3. Select **Report a vulnerability**.
4. Submit the vulnerability privately.

This reporting option must be enabled by the repository maintainer.

If private vulnerability reporting is unavailable, contact the maintainer through:

https://github.com/amlanpatnaik001

Request a private reporting channel without publishing sensitive vulnerability details.

## Information to Include

Please provide as much of the following information as safely possible:

- Affected plugin name and version.
- QGIS version and operating system.
- Description of the suspected vulnerability.
- Steps required to reproduce the issue.
- Potential security impact.
- A minimal proof of concept, where appropriate.
- Relevant sanitized logs or screenshots.

Do not include passwords, authentication tokens, private database credentials, customer information or confidential project datasets.

## Response and Disclosure Process

Reports will be reviewed by the maintainer as soon as reasonably practical.

The review process may include:

1. Initial assessment and validation.
2. Determining affected plugin releases and severity.
3. Preparing a fix or mitigation where appropriate.
4. Publishing a corrected release.
5. Coordinating public disclosure when appropriate.

Response and remediation timelines are not guaranteed and depend on the severity, complexity and reproducibility of the reported issue.

Please allow the maintainer a reasonable opportunity to investigate and address a confirmed vulnerability before publicly disclosing technical details.

## Responsible Security Testing

Security researchers are requested to:

- Test only systems and environments they own or are explicitly authorized to assess.
- Avoid accessing, modifying or disclosing other users' data.
- Avoid service disruption, destructive testing or denial-of-service attacks.
- Avoid publicly disclosing unpatched vulnerabilities.
- Report findings privately and cooperate during investigation.

Thank you for helping make AMLAN-X safer.

---

**Maintained by:** Amlan Patnaik  
**Project:** AMLAN-X QGIS Plugin Repository  
**Repository:** https://github.com/amlanpatnaik001/amlanx-qgis-plugin-repository

Copyright © 2077 Amlan Patnaik. All rights reserved.
