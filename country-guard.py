import signal
import json
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from urllib2 import Request, urlopen, URLError
from gi.repository import Notify as notify
import threading

APPINDICATOR_ID = "county-guard"
UNKNOWN_COUNTRY_CODE = "?"

countryCode = UNKNOWN_COUNTRY_CODE

def main():
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID,
        "whatever",
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    set_interval(check_country, 2)
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    item_quit = gtk.MenuItem("Quit")
    item_quit.connect("activate", quit)
    menu.append(item_quit)

    # item_joke = gtk.MenuItem("Joke")
    # item_joke.connect("activate", joke)
    # menu.append(item_joke)

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
            notify_failure()

def fetch_ip_info():
    request = Request("http://ip-api.com/json/")
    response = urlopen(request)
    return json.loads(response.read())

def notify_country(country, ip):
    notify.Notification.new(
        "<b>You're now in %s</b>" % country,
        "Your IP: %s" % ip,
        None).show()

def notify_failure():
    notify.Notification.new(
        "Unable to get current IP information!", None, None).show()

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
