# backend.ai-console-server

A minimal webapp to convert web session requests to API requests


## Installation

Prepare a Python virtualenv (Python 3.7 or higher) and a Redis server (5.0 or higher).

```console
$ git clone https://github.com/lablup/backend.ai-console-server console-server
$ cd console-server
$ pip install -U -e .
$ cp console-server.sample.conf console-server.conf
```

## Mode

If `service.mode` is set "webconsole" (the default), the console server handles
PWA-style fallbacks (e.g., serving `index.html` when there are no matching
files for the requested URL path).
The PWA must exclude `/server` and `/func` URL prefixes from its own routing
to work with the console server's web sessions and the API proxy.

If it is set "static", the console server serves the static files as-is,
without any fallbacks or hooking, while preserving the `/server` and `/func`
prefixed URLs and their functionalities.

If you want to serve console in console-server with "webconsole" mode, prepare static console source by choosing one of the followings.

### Option 1: Build console from source

Build **[backend.ai-console](https://github.com/lablup/backend.ai-console)** and copy all files under `build/bundle`
into the `src/ai/backend/console/static` directory.

### Option 2: Use pre-built console

To download and deploy console from pre-built source, do the following:

```console
git submodule init
git submodule update
cd src/ai/backend/console/static
git checkout main  # or target branch
git fetch
git pull
```
### Setup configuration for console-server

You don't have to write `config.toml` for the console as this console server auto-generates it on-the-fly.

Edit `console-server.conf` to match with your environment.


## Usage

```console
$ python -m ai.backend.console.server
```
