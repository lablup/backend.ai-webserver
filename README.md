# backend.ai-console-server

A minimal webapp to convert web session requests to API requests


## Installation

Prepare a Python virtualenv (Python 3.7 or higher) and a Redis server.

```console
$ git clone https://github.com/lablup/backend.ai-console-server console-server
$ cd console-server
$ pip install -U -e .
$ cp console-server.sample.conf console-server.conf
```

Build **[backend.ai-console](https://github.com/lablup/backend.ai-console)** and copy all files under `build/bundle`
into the `src/ai/backend/console/static` directory.

You don't have to write `config.ini` for the console as this console server auto-generates it on-the-fly.

Edit `console-server.conf` to match with your environment.

## Usage

```console
$ python -m ai.backend.console.server
```
