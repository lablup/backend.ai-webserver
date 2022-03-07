Changes
=======

<!--
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.

    To add a new change log entry, please refer
    https://pip.pypa.io/en/latest/development/contributing/#news-entries

    We named the news folder "changes".

    WARNING: Don't drop the last line!
-->

<!-- towncrier release notes start -->

21.03.14 (2022-01-26)
---------------------

### Miscellaneous
* Update and pin the client SDK version to 21.03.10


21.03.13 (2021-11.09)
---------------------

### Web UI
* Updated the webui version to 21.09.2


21.03.12 (2021-10-21)
---------------------

### Web UI
* Updated the webui version to 21.09.1


21.03.11 (2021-10-21)
---------------------

### Web UI
* Updated the webui version to 21.09.0


21.03.10 (2021-09-14)
---------------------

### Web UI
* Updated the webui version to 21.03.11


21.03.9 (2021-09-02)
--------------------

### Web UI
* Updated the webui version to 21.03.9


21.03.8 (2021-08-09)
--------------------

### Web UI
* Updated the webui version to 21.03.9

### Features
* General image allowlist support on configuration file ([#44](https://github.com/lablup/backend.ai-webserver/issues/44))

### Fixes
* Deliver the client IP by referencing request.remote  when X-Forwarded-For is empty. ([#43](https://github.com/lablup/backend.ai-webserver/issues/43))


21.03.7 (2021-07-22)
--------------------

### Web UI
* Updated the webui version to 21.03.8


21.03.6 (2021-07-19)
--------------------

### Web UI
* Updated the webui version to 21.03.7

### Features
* Send X-Forwarded-For header from token login handler for token authentication. ([#40](https://github.com/lablup/backend.ai-webserver/issues/40))
* Add webui_debug option to enable debug mode in Web-UI. ([#41](https://github.com/lablup/backend.ai-webserver/issues/41))


21.03.5 (2021-07-14)
--------------------

### Web UI
* Updated the webui version to 21.03.6

### Features
* Add an option to support creating a compute session by manually typing the name of an image. ([#37](https://github.com/lablup/backend.ai-webserver/issues/37))
* Add ping API to to check webserver health. ([#38](https://github.com/lablup/backend.ai-webserver/issues/38))

### Fixes
* Add max_memory_per_container in configuration file to limit memory allocation for each container. ([#39](https://github.com/lablup/backend.ai-webserver/issues/39))


21.03.4 (2021-06-07)
--------------------

### Web UI
* Updated the webui version to 21.03.5


21.03.3 (2021-05-17)
--------------------

### Web UI
* Updated the webui version to 21.03.4

### Fixes
* Send cookies for an api request. This is required to cookie-based authentication for each request. ([#35](https://github.com/lablup/backend.ai-webserver/issues/35))

21.03.2 (2021-04-30)
--------------------

### Web UI
* Updated the webui version to 21.03.3


21.03.1 (2021-04-04)
--------------------

### Web UI
* Updated the webui version to 21.03.2


21.03.0 (2021-03-29)
--------------------

### Web UI
* Updated the webui version to 21.03.0

### Miscellaneous
* Improve GitHub Actions CI workflows to run as single pipeline and make the deployment to be triggered via tagged commits like other repositories ([#31](https://github.com/lablup/backend.ai-webserver/issues/31))
* Update the name of console-server to webserver ([#32](https://github.com/lablup/backend.ai-webserver/issues/32))


20.09.2 (2021-01-04)
--------------------

### Web UI
* Updated the console version to 21.01.0


20.09.1 (2020-12-30)
--------------------

### Web UI
* Updated the console version to 20.12.6


20.09.0 (2020-12-29)
--------------------

### Web UI
* Updated the console version to 20.12.5

### Features
* Adds configurations on maximum resources per session (cores, CUDA devices, shared memory, and upload size limit). ([#28](https://github.com/lablup/backend.ai-webserver/issues/28))
* Prevents too many login attempts, usually an indication of abuse and/or malicious robots. Block time and allowed fail count are configurable. ([#29](https://github.com/lablup/backend.ai-webserver/issues/29))

### Fixes
* Use persistent manager endpoint for websocket streaming (app) per session and per app by storing the endpoint information in the browser session. ([#30](https://github.com/lablup/backend.ai-webserver/issues/30))


20.09.0b1 (2020-12-02)
----------------------

* Updated the console version to 20.11.3


20.09.0a3 (2020-11-03)
----------------------

* Updated the console version to 20.11.1

### Fixes
* Fix a 502 HTTP error returned when starting service ports via CLI in the session mode by excluding the `stream/session/{id}/apps` API from the websocket routes since it's a plain HTTP GET API. ([#27](https://github.com/lablup/backend.ai-console-server/issues/27))


20.09.0a2 (2020-10-28)
----------------------

### Features
* Add option to enable/disable open port to public checkbox. ([#22](https://github.com/lablup/backend.ai-console-server/issues/22))

### Fixes
* Specify no-store only to disable cache for static files. ([#21](https://github.com/lablup/backend.ai-console-server/issues/21))
* Update dependencies (aiohttp 3.7, etc.) which enables use of `SameSite` cookies ([#23](https://github.com/lablup/backend.ai-console-server/issues/23))
* Update aiohttp to 3.7.2 to fix [an upstream issue](https://github.com/aio-libs/aiohttp/issue/5149) related to `sendfile()` fallback with uvloop ([#25](https://github.com/lablup/backend.ai-console-server/issues/25))

### Miscellaneous
* Update GitHub Actions workflows to handle tests, deployment and changelog linting with submodules ([#26](https://github.com/lablup/backend.ai-console-server/issues/26))


20.03.0 (2020-07-28)
--------------------

#### Features
* Add option to expose `allow change signin mode` option by config.toml [(#12)](https://github.com/lablup/backend.ai-console-server/issues/12)
* Adopt towncrier for changelog management [(#13)](https://github.com/lablup/backend.ai-console-server/issues/13)
* Update the proxy implementation to work with the new client SDK (v20.03 series) [(#14)](https://github.com/lablup/backend.ai-console-server/issues/14)
* Add route for cloud plugin. [(#15)](https://github.com/lablup/backend.ai-console-server/issues/15)
* Add `allowAnonymousChangePassword` option for console [(#18)](https://github.com/lablup/backend.ai-console-server/issues/18)
