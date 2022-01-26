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

.. towncrier release notes start


## 21.09.4 (2022-01-26)

### Miscellaneous
* Update and pin the client SDK version to 21.09.3


## 21.09.3 (2022-01-13)

### Web UI
* Updated the webui version to 21.09.3

### Features
* Add allow_signup_without_confirmation in configuration file to disable token input and email confirmation ([#50](https://github.com/lablup/backend.ai-webserver/issues/50))


## 21.09.2 (2021-11-09)

### Web UI
* Updated the webui version to 21.09.2


## 21.09.1 (2021-10-21)

### Web UI
* Updated the webui version to 21.09.1


## 21.09.0 (2022-10-21)

### Web UI
* Updated the webui version to 21.09.0

### Features
* Adds configurations on maximum resources per session (cores, CUDA devices, shared memory, and upload size limit). ([#28](https://github.com/lablup/backend.ai-webserver/issues/28))
* Prevents too many login attempts, usually an indication of abuse and/or malicious robots. Block time and allowed fail count are configurable. ([#29](https://github.com/lablup/backend.ai-webserver/issues/29))
* Add an option to support creating a compute session by manually typing the name of an image. ([#37](https://github.com/lablup/backend.ai-webserver/issues/37))
* Add ping API to to check webserver health. ([#38](https://github.com/lablup/backend.ai-webserver/issues/38))
* Send X-Forwarded-For header from token login handler for token authentication. ([#40](https://github.com/lablup/backend.ai-webserver/issues/40))
* Add webui_debug option to enable debug mode in Web-UI. ([#41](https://github.com/lablup/backend.ai-webserver/issues/41))
* General image allowlist support on configuration file ([#44](https://github.com/lablup/backend.ai-webserver/issues/44))

### Fixes
* Use persistent manager endpoint for websocket streaming (app) per session and per app by storing the endpoint information in the browser session. ([#30](https://github.com/lablup/backend.ai-webserver/issues/30))
* Send cookies for an api request. This is required to cookie-based authentication for each request. ([#35](https://github.com/lablup/backend.ai-webserver/issues/35))
* Add max_memory_per_container in configuration file to limit memory allocation for each container. ([#39](https://github.com/lablup/backend.ai-webserver/issues/39))
* Deliver the client IP by referencing request.remote  when X-Forwarded-For is empty. ([#43](https://github.com/lablup/backend.ai-webserver/issues/43))

### Miscellaneous
* Improve GitHub Actions CI workflows to run as single pipeline and make the deployment to be triggered via tagged commits like other repositories ([#31](https://github.com/lablup/backend.ai-webserver/issues/31))
* Update the name of console-server to webserver ([#32](https://github.com/lablup/backend.ai-webserver/issues/32))


## 20.09.0b1 (2020-12-02)

* Updated the console version to 20.11.3


## 20.09.0a3 (2020-11-03)

* Updated the console version to 20.11.1

### Fixes
* Fix a 502 HTTP error returned when starting service ports via CLI in the session mode by excluding the `stream/session/{id}/apps` API from the websocket routes since it's a plain HTTP GET API. ([#27](https://github.com/lablup/backend.ai-console-server/issues/27))


## 20.09.0a2 (2020-10-28)

### Features
* Add option to enable/disable open port to public checkbox. ([#22](https://github.com/lablup/backend.ai-console-server/issues/22))

### Fixes
* Specify no-store only to disable cache for static files. ([#21](https://github.com/lablup/backend.ai-console-server/issues/21))
* Update dependencies (aiohttp 3.7, etc.) which enables use of `SameSite` cookies ([#23](https://github.com/lablup/backend.ai-console-server/issues/23))
* Update aiohttp to 3.7.2 to fix [an upstream issue](https://github.com/aio-libs/aiohttp/issue/5149) related to `sendfile()` fallback with uvloop ([#25](https://github.com/lablup/backend.ai-console-server/issues/25))

### Miscellaneous
* Update GitHub Actions workflows to handle tests, deployment and changelog linting with submodules ([#26](https://github.com/lablup/backend.ai-console-server/issues/26))
