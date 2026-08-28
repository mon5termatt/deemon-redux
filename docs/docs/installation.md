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

## Step 1 - Required Dependencies

To install and run Deemon Redux, you need **Python 3.8 or higher** and the `pip` package manager.

Please refer to [python.org](https://www.python.org/downloads/) for more information.

On some distributions, the `pip` command is for Python 2. In that case, substitute `pip` for `pip3` in the commands below.

**Windows users**: Run these commands in Command Prompt, Windows Terminal, or PowerShell.

## Step 2 - Installing Deemon Redux

Deemon Redux is a continuation of the archived [deemon](https://github.com/digitalec/deemon) project. This fork is maintained at [mon5termatt/deemon-redux](https://github.com/mon5termatt/deemon-redux).

### Install from GitHub (recommended)

Install the latest `main` branch directly with pip:

```bash
pip install git+https://github.com/mon5termatt/deemon-redux.git
```

To install a specific release tag:

```bash
pip install git+https://github.com/mon5termatt/deemon-redux.git@v2.25
```

### Install from a local clone

If you plan to contribute or run from source:

```bash
git clone https://github.com/mon5termatt/deemon-redux.git
cd deemon-redux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

If you prefer not to activate the virtual environment each time, use the repo wrapper:

```bash
./bin/deemon --help
```

You can also symlink it for system-wide use:

```bash
ln -sf "$(pwd)/bin/deemon" /usr/local/bin/deemon
```

## Step 3 - Verify installation

Once installation completes, confirm Deemon Redux is available:

```bash
deemon -V
Deemon Redux 2.25
```

## Step 4 - Initialize application data

Before first use, initialize the local config and database:

```bash
deemon --init
```

This creates the application data directory used by Deemon Redux (config, database, logs).

## Docker

Pre-built images are published to GitHub Container Registry on each release:

```bash
docker pull ghcr.io/mon5termatt/deemon-redux:latest
```

Example usage:

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

Configuration is stored in the `/config` volume (mapped to `~/.config/deemon-redux` inside the container).

## Configuration & First Use

Congrats! If you've made it this far, you have successfully installed Deemon Redux.
There are a few things you should configure before using Deemon Redux. Head on over
to the [configuration](configuration.md) page to learn more.
