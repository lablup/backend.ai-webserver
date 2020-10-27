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

20.03.1 (2020-10-27)
--------------------

### Features
* Add option to enable/disable open port to public checkbox. ([#22](https://github.com/lablup/backend.ai-console-server/issues/22))

### Fixes
* Update dependencies (aiohttp 3.7, client SDK 20.03.8, etc.) which enables use of `SameSite` cookies ([#23](https://github.com/lablup/backend.ai-console-server/issues/23))


20.03.0 (2020-07-28)
--------------------

#### Features
* Add option to expose `allow change signin mode` option by config.toml [(#12)](https://github.com/lablup/backend.ai-console-server/issues/12)
* Adopt towncrier for changelog management [(#13)](https://github.com/lablup/backend.ai-console-server/issues/13)
* Update the proxy implementation to work with the new client SDK (v20.03 series) [(#14)](https://github.com/lablup/backend.ai-console-server/issues/14)
* Add route for cloud plugin. [(#15)](https://github.com/lablup/backend.ai-console-server/issues/15)
* Add `allowAnonymousChangePassword` option for console [(#18)](https://github.com/lablup/backend.ai-console-server/issues/18)
