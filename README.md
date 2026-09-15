# Deemon Redux

<img src="deemon/assets/images/deemon.png" alt="Deemon Redux" width="300">

Deemon Redux is a continuation of the archived [deemon](https://github.com/digitalec/deemon) project — a monitoring utility for new artist releases with email alerts and automated downloading via the deemix library.

## Quick install

Requires **Python 3.8+**.

```bash
pip install deemon-redux
deemon -V
deemon --init
deemon monitor
```

On Linux/macOS, use `pip3` if `pip` points to Python 2. On Windows, run these in PowerShell or Terminal.

## Quick start

```bash
deemon --init          # create config and database (first run only)
deemon monitor         # add artists to watch
deemon refresh         # check for new releases
deemon download --help
```

Config is stored at `~/.config/deemon-redux` (Linux), `~/Library/Application Support/deemon-redux` (macOS), or `%appdata%\deemon-redux` (Windows).

More setup options: [installation docs](https://mon5termatt.github.io/deemon-redux/docs/installation/) · [configuration](https://mon5termatt.github.io/deemon-redux/docs/configuration/)

## Docker

```bash
docker pull ghcr.io/mon5termatt/deemon-redux:latest

docker run --rm -it \
  -v deemon-redux-config:/config \
  -v ~/Music:/downloads \
  ghcr.io/mon5termatt/deemon-redux:latest --init

docker run --rm -it \
  -v deemon-redux-config:/config \
  -v ~/Music:/downloads \
  ghcr.io/mon5termatt/deemon-redux:latest refresh
```

Schedule a daily refresh with `RUN_TIME` (and optional `TZ`):

```bash
docker run -d --name deemon \
  -e RUN_TIME=06:00 \
  -e TZ=America/Chicago \
  -v deemon-redux-config:/config \
  -v ~/Music:/downloads \
  ghcr.io/mon5termatt/deemon-redux:latest
```

## Development

Clone and install from source:

```bash
git clone https://github.com/mon5termatt/deemon-redux.git
cd deemon-redux
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
deemon --help
```

Or use the repo wrapper without activating the venv:

```bash
./bin/deemon monitor
```

## Documentation

- Online docs: https://mon5termatt.github.io/deemon-redux/
- CLI help: `deemon <command> -h`

## Contributing

Open an issue for bugs/feature requests and submit PRs with a short test plan.
