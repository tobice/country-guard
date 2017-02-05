# country-guard

A simple IP-based country indicator for Ubuntu.

[![Screenshot](./screenshot.png)](./screenshot.png)

Depending on your current IP-based location, the indicator shows a nice
country flag in your notification area. In case you find yourself in an
undesirable country, a customizable list of commands is executed. Perfect for
detecting unintentional VPN disconnects.

## How does this work

The script polls every few seconds [ip-api.com](http://ip-api.com) to obtain
the current IP and related meta-data including geographical information.

Unlike other approaches, this can detect VPN disconnects even when the VPN is
not running on your machine but perhaps on a router you're connected to. **This
script gives you an immediate visual feedback of where you are.**

You can also define a whitelist of *safe* countries and also a list of commands
that should be executed in the moment you find yourself in a country that is not
whitelisted. Typically, you might want to kill *certain programs* in such a
situation.

Note that these commands are executed continuously.

## Installation

First, clone or download this repository. Rename `config.sample.py` to
`config.py` and adjust the values. Then simply execute `country-guard.py`.

If you want this script to start automatically, create a file
`country-guard.desktop` in `~/.config/autostart` with the following content:

```
[Desktop Entry]
Type=Application
Exec=/home/user/path/to/country-guard.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Country Guard
Comment=
```

Don't forget to make both the `country-guard.py` file and the
`coungry-guard.desktop` file executable.
