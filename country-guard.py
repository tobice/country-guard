import signal
import json
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from urllib2 import Request, urlopen, URLError
from gi.repository import Notify as notify
import threading
import os

COUNTRY_WHITELIST = ["CZ"]
GUARD_COMMANDS = [
    "killall -9 ktorrent",
    "killall -9 transmission-gtk"]

APPINDICATOR_ID = "county-guard"
UNKNOWN_COUNTRY_CODE = "?"

countryCode = UNKNOWN_COUNTRY_CODE
indicator = None

def main():
    global indicator
    indicator = build_indicator()
    notify.init(APPINDICATOR_ID)
    set_interval(check_country, 2)
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
    global countryCode
    try:
        ip_info = fetch_ip_info()

        if ip_info["countryCode"] != countryCode:
            countryCode = ip_info["countryCode"]
            notify_country(ip_info["country"], ip_info["query"])

    except Exception:
        if countryCode != UNKNOWN_COUNTRY_CODE:
            countryCode = UNKNOWN_COUNTRY_CODE

    if countryCode not in COUNTRY_WHITELIST:
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
    for command in GUARD_COMMANDS:
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
