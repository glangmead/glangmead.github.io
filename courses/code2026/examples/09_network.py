"""
CLASS 4 - NETWORK
================================================================================

THE PROMPT
----------
My students can read a file off disk. Now teach them to read one off the
internet, and make the point that it's almost the same act.

Use only the standard library so nobody has to install anything - a class
where ten people are pip-installing is a class where nothing gets taught.
But show the `requests` version side by side in a comment, because that's
what they'll see in every tutorial and in most AI output.

Cover:
1. What a URL is made of, taken apart.
2. One request. Show the STATUS CODE and a few response headers before
   touching the body, because those are the things they'll be asked about
   when something breaks.
3. Query parameters built with urlencode, never by gluing strings - and
   connect that explicitly to the SQL placeholder lesson, it's the same
   principle.
4. JSON in, nested dictionaries and lists out - the same shape they met in
   the dictionaries lesson.
5. Digging into a response safely when fields might be missing.
6. What goes wrong: 404, a bad hostname, a timeout. Catch each one and say
   what it means in English.
7. Manners: identify yourself, set a timeout, don't hammer, and read the
   terms.
8. A second, completely different API, to show the shape doesn't change.

Use Open Library (openlibrary.org) and Open-Meteo - both free, neither needs
an API key. If the network is down, say so clearly and carry on with a saved
copy of a response rather than crashing, because classroom wifi.

================================================================================
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request


# ============================================================ 1. What a URL is
print("=== 1. A URL, taken apart ===")

url = "https://openlibrary.org/search.json?q=piranesi&limit=2"
parts = urllib.parse.urlparse(url)

print(f"scheme (how):     {parts.scheme}   <- https means encrypted")
print(f"host (which machine): {parts.netloc}")
print(f"path (which thing):   {parts.path}")
print(f"query (the details):  {parts.query}")
print(f"query, parsed:        {urllib.parse.parse_qs(parts.query)}")

# Every web address you've ever typed has this shape. The browser does
# exactly what this program is about to do.


# =============================================================== the helper
def fetch(url, timeout=10):
    """Fetch a URL. Returns (status, headers, body-as-text).

    A request has to say who's asking. Many servers reject the default
    Python user-agent outright; an honest one that names the project is both
    politer and more reliable. Never lie about being a browser.
    """
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "code2026-class-example/1.0 (teaching example)"},
    )
    # timeout is not optional in real code. Without it, a server that never
    # answers hangs your program forever.
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, dict(response.headers), response.read().decode("utf-8")


# The same thing with the `requests` library, which you'll see everywhere:
#
#     import requests
#     r = requests.get(url, params={"q": "piranesi"}, timeout=10,
#                      headers={"User-Agent": "..."})
#     r.raise_for_status()
#     data = r.json()
#
# Shorter and nicer, and worth installing for real work. We're using the
# standard library here so this file runs on any Python, anywhere, with
# nothing installed.


# ======================================================== 2. One request
print("\n=== 2. The response, before the content ===")

online = True
try:
    status, headers, body = fetch("https://openlibrary.org/search.json?q=piranesi&limit=2")
    print(f"status code:  {status}      <- 200 means OK")
    print(f"content-type: {headers.get('Content-Type')}")
    print(f"body length:  {len(body):,} characters")
    print(f"first 80 chars: {body[:80]}...")
except urllib.error.URLError as error:
    online = False
    print(f"no network right now ({error.reason}) - carrying on with a saved copy")

# Status codes worth knowing by heart:
#   200 OK            it worked
#   301/302           moved; your client follows it automatically
#   400 Bad Request   you sent something malformed
#   401 / 403         you're not logged in / you're not allowed
#   404 Not Found     no such thing here
#   429 Too Many      you're going too fast; slow down (this one is on you)
#   500               the server broke; not your fault
# The first digit is the whole story: 2 fine, 3 elsewhere, 4 your fault,
# 5 their fault.


# ================================================= 3. Building the query safely
print("\n=== 3. Building a URL with someone else's text in it ===")

search_for = "Bridget Jones's Diary"      # apostrophe, spaces

# WRONG - the spaces and the apostrophe are not legal in a URL, and if this
# text came from a user it's a hole in your program.
print(f"glued together:  https://openlibrary.org/search.json?q={search_for}")

# RIGHT - urlencode escapes everything that needs escaping.
query = urllib.parse.urlencode({
    "q": search_for,
    "limit": 2,
    "fields": "title,author_name,first_publish_year",
})
safe_url = f"https://openlibrary.org/search.json?{query}"
print(f"urlencoded:      {safe_url}")

# This is the same rule as the ? placeholders in SQL, and the same rule as
# using the csv module instead of gluing commas. Any time text from
# somewhere else gets dropped into a language - SQL, a URL, HTML, a shell
# command - use the tool that escapes it. Never build it with an f-string.
# One idea, four places. If you learn nothing else this term, learn this one.


# =========================================== 4. JSON in, dictionaries out
print("\n=== 4. What comes back ===")

# A saved response, so this lesson works with the wifi off. This is exactly
# what the server sends, trimmed down.
SAVED = """
{"numFound": 27, "start": 0, "docs": [
  {"title": "Piranesi", "author_name": ["Susanna Clarke"], "first_publish_year": 2020},
  {"title": "Piranesi: The Complete Etchings", "author_name": ["Giovanni Battista Piranesi"], "first_publish_year": 1994}
]}
"""

if online:
    _, _, body = fetch("https://openlibrary.org/search.json?q=piranesi&limit=2"
                       "&fields=title,author_name,first_publish_year")
else:
    body = SAVED

# json.loads turns the text into ordinary Python values. This is the same
# json module that read your file in the storage lesson - JSON doesn't care
# whether the text came from a disk or a wire.
data = json.loads(body)

print(f"the top level is a {type(data).__name__} with keys: {list(data.keys())}")
print(f"data['docs'] is a {type(data['docs']).__name__} of {len(data['docs'])} items")
print(f"each item is a {type(data['docs'][0]).__name__}")
print("\nfirst result, in full:")
print(json.dumps(data["docs"][0], indent=2))

# Dictionaries inside lists inside dictionaries - exactly section 7 of the
# dictionaries lesson. Every web API you will ever touch looks like this.


# ==================================================== 5. Digging in safely
print("\n=== 5. Reading the parts you actually want ===")

for doc in data["docs"]:
    # Any field can be missing from any record. Real data is full of holes,
    # and doc["author_name"] would crash on the first book with no author.
    title = doc.get("title", "(untitled)")
    authors = doc.get("author_name", ["unknown"])
    year = doc.get("first_publish_year", "?")
    print(f"  {title} - {', '.join(authors)} ({year})")

# A rule worth adopting: index with [] into data YOU created, use .get() for
# data that arrived from outside. You control the first. You control nothing
# about the second.


# ================================================== 6. When it goes wrong
print("\n=== 6. Three ways it fails ===")

if online:
    # (a) The server answers, but says no.
    try:
        fetch("https://openlibrary.org/this-page-does-not-exist.json")
    except urllib.error.HTTPError as error:
        print(f"  404: HTTPError {error.code} - the server replied, and its reply was 'no'")

    # (b) There is no such machine.
    try:
        fetch("https://this-host-does-not-exist-2026.example/")
    except urllib.error.URLError as error:
        print(f"  bad host: URLError - never got as far as a server. ({error.reason})")

    # (c) The machine is there but too slow (0.001s is impossibly short, on purpose).
    try:
        fetch("https://openlibrary.org/search.json?q=slow", timeout=0.001)
    except Exception as error:
        print(f"  timeout: {type(error).__name__} - gave up waiting. This is why you set one.")
else:
    print("  (skipped - no network)")

# HTTPError means you reached the server and it refused you: read the code.
# URLError means you never got there: DNS, wifi, firewall, VPN, typo.
# Knowing which of the two you have cuts the debugging in half.


# ===================================================== 7. A different API
print("\n=== 7. A completely different API, the same five steps ===")

if online:
    weather_url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": 40.7128,      # New York
        "longitude": -74.0060,
        "current": "temperature_2m,wind_speed_10m",
        "temperature_unit": "fahrenheit",
    })
    try:
        # Pause between calls to a different service. One request is fine;
        # a loop making hundreds is how you get your address blocked.
        time.sleep(0.5)
        _, _, weather_body = fetch(weather_url)
        weather = json.loads(weather_body)
        now = weather["current"]
        units = weather["current_units"]
        print(f"  New York right now: {now['temperature_2m']}{units['temperature_2m']}, "
              f"wind {now['wind_speed_10m']} {units['wind_speed_10m']}")
        print(f"  (reading taken at {now['time']})")
    except Exception as error:
        print(f"  weather lookup failed: {type(error).__name__}: {error}")
else:
    print("  (skipped - no network)")

# Different company, different data, identical procedure: build a URL,
# fetch it, parse the JSON, dig out what you need, handle the failures. Once
# you can do it once you can do it for anything. The only thing that changes
# from API to API is the documentation you have to read.


# ==============================================================================
# MANNERS, AND THE RULES
# ------------------------------------------------------------------------------
# 1. Identify yourself in the User-Agent. Never impersonate a browser.
# 2. Always set a timeout.
# 3. Pause between requests. Back off when you see a 429.
# 4. Read the terms of service before you build anything on someone's API.
# 5. When an API needs a key, the key is a password. It NEVER goes in your
#    code, and it never gets pasted into a chat window. Put it in an
#    environment variable and read it with os.environ. If you commit a key to
#    GitHub, assume it is compromised within minutes - bots watch for it.
# 6. Assume every request will fail sometimes, because it will.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Put the safe_url from section 3 in your browser. It's the same request.
#   The browser is a fetch() with a nice interface.
# - Change the latitude and longitude to where you live.
# - Turn off your wifi and run the whole file. It should tell you what
#   happened rather than dumping a traceback. That difference is most of
#   what "production code" means.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Rewrite this using requests, and tell me exactly what requests is doing
#    for me that urllib isn't."
# - "This API call fails one time in fifty. Add retries with exponential
#    backoff, and explain why exponential."
# - "I need an API key for this service. Where should I put it, and what
#    should I never do with it?"
# ==============================================================================
