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
