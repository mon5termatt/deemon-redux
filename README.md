# Deemon Redux

<img src="deemon/assets/images/deemon.png" alt="Deemon Redux" width="300">

Deemon Redux is a continuation of the archived [deemon](https://github.com/digitalec/deemon) project — a monitoring utility for new artist releases with email alerts and automated downloading via the deemix library.

## Development setup

### Prerequisites

- Python `>= 3.8`

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Run without activating `.venv`

If you prefer not to `source .venv/bin/activate`, use the repo wrapper:

```bash
./bin/deemon --help
./bin/deemon monitor
```

### Initialize local app data

```bash
deemon --init
```

This creates the local configuration/database used by the CLI.

## Run locally

```bash
deemon --help
deemon monitor
```

For command-specific help:

```bash
deemon monitor -h
```

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
  ghcr.io/mon5termatt/deemon-redux:latest --help

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

## Testing / sanity checks

```bash
deemon test -h
deemon test -E '<URL regex pattern>'
deemon test -e
```

## Documentation

- Online docs: https://mon5termatt.github.io/deemon-redux/
- CLI help: `deemon <command> -h`
- Source docs in-repo under `docs/`

## Contributing

Open an issue for bugs/feature requests and submit PRs with a short test plan.
