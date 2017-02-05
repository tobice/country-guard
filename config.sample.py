# How often (in seconds) the current IP information should be refreshed. Note
# that the API we use to obtain this information, ip-api.com, allows at most
# 150 requests per minute (~ twice every second).
refresh_interval = 2

# List of "allowed" countries.
country_whitelist = ["CZ"]

# List of commands that are executed whenever the user finds themselves outside
# of whitelisted countries. Note that these commands are executed periodically.
guard_commands = [
    "killall -9 ktorrent",
    "killall -9 transmission-gtk"]
