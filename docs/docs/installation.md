---
layout: default
title: Installation
nav_order: 2
---

# Installation
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Requirements

- **Python 3.8 or higher**
- **pip** (use `pip3` if `pip` points to Python 2)

Windows users: run these commands in PowerShell or Terminal.

---

## Install from PyPI (recommended)

```bash
pip install deemon-redux
```

Install a specific version:

```bash
pip install deemon-redux==2.25
```

Upgrade an existing install:

```bash
pip install --upgrade deemon-redux
```

---

## First run

```bash
deemon -V
deemon --init
deemon monitor
```

`deemon --init` creates the config, database, and logs under:

- **Linux:** `~/.config/deemon-redux`
- **macOS:** `~/Library/Application Support/deemon-redux`
- **Windows:** `%appdata%\deemon-redux`

Next step: [configuration](configuration.md).

---

## Docker

Images are published on each release to GitHub Container Registry.

```bash
docker pull ghcr.io/mon5termatt/deemon-redux:latest
```

First-time setup and one-shot refresh:

```bash
docker run --rm -it \
  -v deemon-redux-config:/config \
  -v ~/Music:/downloads \
  ghcr.io/mon5termatt/deemon-redux:latest --init

docker run --rm -it \
  -v deemon-redux-config:/config \
  -v ~/Music:/downloads \
  ghcr.io/mon5termatt/deemon-redux:latest refresh
```

### Scheduled refresh (`RUN_TIME`)

Set `RUN_TIME` (or `run_time`) to `HH:MM` (24-hour) to keep the container running and run `deemon refresh` once per day at that time. Use `TZ` for the timezone:

```bash
docker run -d --name deemon \
  -e RUN_TIME=06:00 \
  -e TZ=America/Chicago \
  -v deemon-redux-config:/config \
  -v ~/Music:/downloads \
  ghcr.io/mon5termatt/deemon-redux:latest
```

Without `RUN_TIME`, the image behaves like a normal CLI (`deemon <command>`).

Configuration is stored in the `/config` volume (`~/.config/deemon-redux` inside the container).

---

## Install from source

For development or contributing:

```bash
git clone https://github.com/mon5termatt/deemon-redux.git
cd deemon-redux
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
deemon --help
```

Without activating the virtualenv, use the repo wrapper:

```bash
./bin/deemon monitor
```

Install directly from GitHub without cloning:

```bash
pip install git+https://github.com/mon5termatt/deemon-redux.git
```

---

## About this fork

Deemon Redux is a continuation of the archived [deemon](https://github.com/digitalec/deemon) project, maintained at [mon5termatt/deemon-redux](https://github.com/mon5termatt/deemon-redux).

The `deemon` command is unchanged for compatibility with existing scripts and workflows.
