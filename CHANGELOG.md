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
* Add an option to support creating a compute session by manually typing the name of an image. ([#37](https://github.com/lablup/backend.ai-webserver/issues/37))
* Add ping API to to check webserver health. ([#38](https://github.com/lablup/backend.ai-webserver/issues/38))
* Send X-Forwarded-For header from token login handler for token authentication. ([#40](https://github.com/lablup/backend.ai-webserver/issues/40))
* Add webui_debug option to enable debug mode in Web-UI. ([#41](https://github.com/lablup/backend.ai-webserver/issues/41))
* General image allowlist support on configuration file ([#44](https://github.com/lablup/backend.ai-webserver/issues/44))

### Fixes
* Send cookies for an api request. This is required to cookie-based authentication for each request. ([#35](https://github.com/lablup/backend.ai-webserver/issues/35))
* Add max_memory_per_container in configuration file to limit memory allocation for each container. ([#39](https://github.com/lablup/backend.ai-webserver/issues/39))
* Deliver the client IP by referencing request.remote  when X-Forwarded-For is empty. ([#43](https://github.com/lablup/backend.ai-webserver/issues/43))


## Older Changelogs
* [21.03](https://github.com/lablup/backend.ai-webserver/blob/21.03/CHANGELOG.md)
* [20.09](https://github.com/lablup/backend.ai-webserver/blob/20.09/CHANGELOG.md)
