# backend.ai-webserver

A minimal webapp to convert web session requests to API requests.


## Installation

Prepare a Python virtualenv (Python 3.7 or higher) and a Redis server (5.0 or higher).

```webserver
$ git clone https://github.com/lablup/backend.ai-webserver webserver
$ cd webserver
$ pip install -U -e .
$ cp webserver.sample.conf webserver.conf
```

## Mode

If `service.mode` is set "webui" (the default), the webserver handles
PWA-style fallbacks (e.g., serving `index.html` when there are no matching
files for the requested URL path).
The PWA must exclude `/server` and `/func` URL prefixes from its own routing
to work with the webserver's web sessions and the API proxy.

If it is set "static", the webserver serves the static files as-is,
without any fallbacks or hooking, while preserving the `/server` and `/func`
prefixed URLs and their functionalities.

If you want to serve web UI in webserver with "webui" mode, prepare static web UI source by choosing one of the followings.

### Option 1: Build web UI from source

Build **[backend.ai-webui](https://github.com/lablup/backend.ai-webui)** and copy all files under `build/bundle`
into the `src/ai/backend/web/static` directory.

### Option 2: Use pre-built web UI

To download and deploy web UI from pre-built source, do the following:

```web UI
git submodule init
git submodule update
cd src/ai/backend/web/static
git checkout main  # or target branch
git fetch
git pull
```
### Setup configuration for webserver

You don't have to write `config.toml` for the web UI as this webserver auto-generates it on-the-fly.

Edit `webserver.conf` to match with your environment.


## Usage

```console
$ python -m ai.backend.console.server
```
