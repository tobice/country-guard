#!/usr/bin/env python

################################################################################
#
# country-guard - A simple Ubuntu IP-based country indicator.
#
# Depending on your current IP-based location, the indicator shows a nice
# country flag in your notification area. In case you find yourself in an
# undesirable country, a customizable list of commands is executed. Perfect for
# detecting unintentional VPN disconnects.
#
# Author: Tobias Potocek <tobiaspotocek@gmail.com>
#
################################################################################

import signal
import json
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from urllib2 import Request, urlopen, URLError
from gi.repository import Notify as notify
import threading
import os
import config

APPINDICATOR_ID = "county-guard"
UNKNOWN_COUNTRY_CODE = "?"

# Current country code
countryCode = UNKNOWN_COUNTRY_CODE

# Reference to the GTK indicator
indicator = None

def main():
    global indicator
    indicator = build_indicator()
    notify.init(APPINDICATOR_ID)
    set_interval(check_country, config.refresh_interval)
    gtk.main()

def build_indicator():
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID,
        gtk.STOCK_REFRESH,
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    return indicator

def build_menu():
    menu = gtk.Menu()

    item_quit = gtk.MenuItem("Quit")
    item_quit.connect("activate", quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def check_country():
    """ The core function that is repeatedly called to check the country """
    global countryCode
    try:
        ip_info = fetch_ip_info()

        if ip_info["countryCode"] != countryCode:
            countryCode = ip_info["countryCode"]
            notify_country(ip_info["country"], ip_info["query"])

    except Exception:
        if countryCode != UNKNOWN_COUNTRY_CODE:
            countryCode = UNKNOWN_COUNTRY_CODE

    # Note that the gaurd commands are executed in every cycle.
    if countryCode not in config.country_whitelist:
        execute_guard_commands()

    update_icon()

def fetch_ip_info():
    request = Request("http://ip-api.com/json/")
    response = urlopen(request)
    return json.loads(response.read())

def notify_country(country, ip):
    notify.Notification.new(
        "<b>You're now in %s</b>" % country,
        "Your IP: %s" % ip,
        None).show()

def execute_guard_commands():
    for command in config.guard_commands:
        os.system(command)

def update_icon():
    global indicator, countryCode
    indicator.set_icon(
        gtk.STOCK_STOP if countryCode == UNKNOWN_COUNTRY_CODE
        else get_icon_file(countryCode))

def get_icon_file(countryCode):
    icon = get_abs_script_dir() + "/flags/" + countryCode.lower() + ".svg"
    return icon if os.path.isfile(icon) else gtk.STOCK_DIALOG_QUESTION

def get_abs_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def quit(source):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
