---
layout: default
title: Home
nav_order: 1
description: "Deemon Redux is a monitoring utility for new artist releases that can provide email alerts and automate downloading via the deemix library"
permalink: /
---

# Deemon Redux Documentation
{: .fs-9 }

Monitor new artist releases with email alerts and automated downloading via deemix.
{: .fs-6 .fw-300 }

[Install now]({{ site.baseurl }}{% link docs/installation.md %}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [Configure]({{ site.baseurl }}{% link docs/configuration.md %}){: .btn .fs-5 .mb-4 .mb-md-0 .mr-2 } [GitHub](https://github.com/mon5termatt/deemon-redux){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Quick install

Requires **Python 3.8+**.

```bash
pip install deemon-redux
deemon -V
deemon --init
deemon monitor
```

Use `pip3` on systems where `pip` is Python 2. See the [installation guide]({{ site.baseurl }}{% link docs/installation.md %}) for Docker, upgrades, and development setup.

---

## Quick start

| Task | Command |
|------|---------|
| Initialize config/database | `deemon --init` |
| Add artists to monitor | `deemon monitor` |
| Check for new releases | `deemon refresh` |
| Download music | `deemon download --help` |
| Command help | `deemon <command> -h` |

Config location:

- **Linux:** `~/.config/deemon-redux`
- **macOS:** `~/Library/Application Support/deemon-redux`
- **Windows:** `%appdata%\deemon-redux`

---

## Disclaimer

Deemon Redux does not download anything by itself. It requires [deemix](https://pypi.org/project/deemix/), which is installed automatically with `pip install deemon-redux`.

Deemix development has been discontinued. Deemon Redux will attempt to stay updated with the latest deemix releases when possible.

The maintained fork [bambanah/deemix](https://github.com/bambanah/deemix) is not compatible with Deemon Redux.

---

## About

Deemon Redux (**dee**zer **mon**itor) is a continuation of the archived [deemon](https://github.com/digitalec/deemon) project.

Licensed under [GPL-3.0](https://github.com/mon5termatt/deemon-redux/blob/main/LICENSE).
