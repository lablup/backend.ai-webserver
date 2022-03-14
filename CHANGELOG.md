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

## 22.03.0a1 (2022-03-14)

### Breaking Changes
* Now it requires Python 3.10 or higher to run. ([#52](https://github.com/lablup/backend.ai-webserver/issues/52))

### Features
* Adds configurations on maximum resources per session (cores, CUDA devices, shared memory, and upload size limit). ([#28](https://github.com/lablup/backend.ai-webserver/issues/28))
* Prevents too many login attempts, usually an indication of abuse and/or malicious robots. Block time and allowed fail count are configurable. ([#29](https://github.com/lablup/backend.ai-webserver/issues/29))
* Add an option to support creating a compute session by manually typing the name of an image. ([#37](https://github.com/lablup/backend.ai-webserver/issues/37))
* Add ping API to to check webserver health. ([#38](https://github.com/lablup/backend.ai-webserver/issues/38))
* Send X-Forwarded-For header from token login handler for token authentication. ([#40](https://github.com/lablup/backend.ai-webserver/issues/40))
* Add webui_debug option to enable debug mode in Web-UI. ([#41](https://github.com/lablup/backend.ai-webserver/issues/41))
* General image allowlist support on configuration file ([#44](https://github.com/lablup/backend.ai-webserver/issues/44))
* Add allow_signup_without_confirmation in configuration file to disable token input and email confirmation ([#50](https://github.com/lablup/backend.ai-webserver/issues/50))
* Add mask_user_info in configuration file to hiding user information ([#51](https://github.com/lablup/backend.ai-webserver/issues/51))

### Fixes
* Use persistent manager endpoint for websocket streaming (app) per session and per app by storing the endpoint information in the browser session. ([#30](https://github.com/lablup/backend.ai-webserver/issues/30))
* Send cookies for an api request. This is required to cookie-based authentication for each request. ([#35](https://github.com/lablup/backend.ai-webserver/issues/35))
* Add max_memory_per_container in configuration file to limit memory allocation for each container. ([#39](https://github.com/lablup/backend.ai-webserver/issues/39))
* Deliver the client IP by referencing request.remote  when X-Forwarded-For is empty. ([#43](https://github.com/lablup/backend.ai-webserver/issues/43))
* Update dependencies for 21.09 release ([#45](https://github.com/lablup/backend.ai-webserver/issues/45))
* Update dependencies for Backend.AI common 21.9, aiohttp 3.8, and aioredis 2.0 ([#47](https://github.com/lablup/backend.ai-webserver/issues/47))
* Upgrade aiohttp-session to a pre-release version compatible with aioredis v2 ([#48](https://github.com/lablup/backend.ai-webserver/issues/48))
* Update Jinja2 package from 2.11.x to 3.0.x ([#49](https://github.com/lablup/backend.ai-webserver/issues/49))

### Miscellaneous
* Improve GitHub Actions CI workflows to run as single pipeline and make the deployment to be triggered via tagged commits like other repositories ([#31](https://github.com/lablup/backend.ai-webserver/issues/31))
* Update the name of console-server to webserver ([#32](https://github.com/lablup/backend.ai-webserver/issues/32))


## Older changelogs

* [21.09](https://github.com/lablup/backend.ai-webserver/blob/21.09/CHANGELOG.md)
* [21.03](https://github.com/lablup/backend.ai-webserver/blob/21.03/CHANGELOG.md)
* [20.09](https://github.com/lablup/backend.ai-webserver/blob/20.09/CHANGELOG.md)
* [20.03](https://github.com/lablup/backend.ai-webserver/blob/20.03/CHANGELOG.md)
