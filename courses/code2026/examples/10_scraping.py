"""
CLASS 4 - SCRAPING
================================================================================

THE PROMPT
----------
Teach web scraping to beginners, and put the ethics FIRST rather than in a
footnote, because this is the topic where an AI will cheerfully write them
something that gets their IP banned or gets them sued.

Structure:
1. The decision tree BEFORE any code: is there an API? is there a download?
   does robots.txt allow it? what do the terms say? is there personal data
   involved? Only then, scrape.
2. Actually check robots.txt in code, with urllib.robotparser, and explain
   what a 404 for robots.txt does and does not mean.
3. Fetch one page and look at the raw HTML, so they see it's just text.
4. Parse it with BeautifulSoup. Explain that a page is a TREE, the same way
   a folder is a tree, and that CSS selectors are paths through it.
5. Pull out a whole page of records into a list of dictionaries - the same
   shape they've had since the dictionaries lesson - and save it as CSV.
6. Follow the "next page" link, politely, with a pause. Cap it at two pages.
7. Be honest about why scrapers break: no contract, HTML changes, JavaScript
   pages that don't work this way at all.

Scrape books.toscrape.com, which exists specifically to be scraped for
practice. Make that clear so nobody thinks any site is fair game.

Standard library plus beautifulsoup4. If bs4 isn't installed, say how to
install it and stop cleanly instead of crashing.

================================================================================
"""

import csv
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("This lesson needs BeautifulSoup. Install it with:")
    print("    pip install beautifulsoup4")
    print("(In Google Colab it's already there.)")
    raise SystemExit(0)


SITE = "http://books.toscrape.com/"
HEADERS = {"User-Agent": "code2026-class-example/1.0 (teaching example)"}


# ==============================================================================
# 1. BEFORE YOU WRITE ANY CODE
# ------------------------------------------------------------------------------
# Work down this list. Stop at the first yes.
#
#   Is there an official API?            -> use it. Always. It's a promise
#                                           that the shape won't change.
#   Is there a bulk download or export?  -> use it. Wikipedia, data.gov, most
#                                           governments and many companies
#                                           publish dumps.
#   Does robots.txt disallow this path?  -> don't. Checked in code below.
#   Do the terms of service forbid it?   -> don't. Read them. Yes, really.
#   Is there personal data on the page?  -> stop and think hard. Names,
#                                           emails, photos, profiles. Legal
#                                           obligations attach to those in
#                                           most of the world, and "it was
#                                           public" is not a defence.
#   Would your traffic hurt the site?    -> slow down. One request every
#                                           second or two. You are a guest.
#
# Only after all of that: scrape. And even then, cache what you fetch so you
# don't re-download the same page every time you fix a bug in your parser.
#
# We're using books.toscrape.com, a fake bookshop published by the Scrapinghub
# team for exactly this purpose. Nothing here is a licence to point the same
# code at a real shop.
# ==============================================================================

print("=== 1-2. Asking permission ===")

def may_we_fetch(url):
    """Check robots.txt for `url`, honestly.

    The obvious version of this - and the version an AI will write for you -
    is three lines:

        robots = urllib.robotparser.RobotFileParser()
        robots.set_url(...)
        robots.read()

    It is wrong in two ways that never announce themselves, and the whole
    reason this function is longer is to avoid them. See the note below.
    """
    robots_url = urllib.parse.urljoin(url, "/robots.txt")
    parser = urllib.robotparser.RobotFileParser()

    # Fetch robots.txt ourselves, with the SAME User-Agent we'll scrape with.
    request = urllib.request.Request(robots_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            # No robots.txt at all. RFC 9309: nothing is disallowed.
            print(f"  no robots.txt (HTTP 404) - nothing is disallowed")
            return True
        # Anything else - 403, 500 - means we genuinely don't know. RFC 9309
        # says treat a 5xx as "disallow everything". Not knowing is a no.
        print(f"  couldn't read robots.txt (HTTP {error.code}) - assuming no")
        return False

    parser.parse(text.splitlines())
    return parser.can_fetch(HEADERS["User-Agent"], url)


allowed = may_we_fetch(SITE)
print(f"robots.txt says we may fetch {SITE}: {allowed}")

# ---------------------------------------------------------------------------
# WHY THE THREE-LINE VERSION IS WRONG - and this is the best example in the
# whole course of why you read the code an assistant hands you.
#
# 1. RobotFileParser.read() fetches robots.txt with urllib's OWN default
#    User-Agent, ignoring yours. So the permission check and the actual
#    scrape go out under two different identities - the exact thing this
#    lesson tells you not to do.
#
# 2. read() does not raise on an HTTP error. It swallows it. On a 403 it
#    quietly sets disallow_all = True, and from then on can_fetch() returns
#    False for every URL you ask about. Your `except` block never fires,
#    because nothing was ever raised.
#
# Together those produce a confident lie. Wikipedia now returns 403 to
# Python's default User-Agent, so the three-line version reports:
#
#     can_fetch("https://en.wikipedia.org/wiki/Python_(programming_language)")
#         -> False        # every page on Wikipedia is forbidden to you
#
# which is simply not true - Wikipedia's robots.txt allows that page. The
# program doesn't crash, doesn't warn, and gives you the opposite of the
# right answer. If you'd been checking permission before a scrape, you'd have
# concluded you weren't allowed. If the check had gone the other way, you'd
# have concluded you were.
#
# Nothing about the three-line version LOOKS wrong. That is the point.
# ---------------------------------------------------------------------------

# Note what a missing robots.txt does and doesn't mean. It means the site has
# stated no restrictions. It does not mean the site has given you permission,
# and it says nothing at all about the terms of service. robots.txt is
# standardised - RFC 9309, an actual IETF standard since 2022 - and that
# standard is explicit that it is NOT a form of access authorisation.
# It is a request, not a lock. Honouring it is the floor, not the bar.

if not allowed:
    print("robots.txt says no. Stopping, which is the entire point.")
    raise SystemExit(0)


# ============================================================ 3. The raw page
print("\n=== 3. A web page is just text ===")


def get(url):
    """Fetch a page as text. Same fetch() idea as the network lesson."""
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8")


try:
    html = get(SITE)
except Exception as error:
    print(f"couldn't reach the site ({type(error).__name__}: {error}).")
    print("Scraping lessons need the network. Try again later.")
    raise SystemExit(0)

print(f"downloaded {len(html):,} characters of HTML")
start = html.index("<article")
print("here's one book, exactly as the server sent it:\n")
print(html[start:start + 620])

# That is what your browser receives too. "View Source" in any browser shows
# you the same thing. Scraping is: download this text, find the parts you
# want. The hard part is entirely the second half.


# ========================================================= 4. The page is a tree
print("\n\n=== 4. Parsing: text in, tree out ===")

soup = BeautifulSoup(html, "html.parser")

print(f"page title: {soup.title.string.strip()}")

# HTML nests: <html> holds <body> holds <section> holds <article> holds <h3>
# holds <a>. It is a tree, exactly like folders inside folders. A CSS
# selector is a path through that tree.
#
#   "article.product_pod"     every <article> with class product_pod
#   "h3 a"                    an <a> anywhere inside an <h3>
#   "p.price_color"           a <p> with class price_color
#
# You do NOT guess these. You right-click the thing you want in your browser,
# choose Inspect, and read them off the Elements panel. That is the actual
# workflow, and it's the same one a professional uses.

pods = soup.select("article.product_pod")
print(f"found {len(pods)} book listings on this page")

first = pods[0]
print("\ndigging into the first one:")
print(f'  select_one("h3 a")           -> {first.select_one("h3 a")}')
print(f'  ...its ["title"] attribute   -> {first.select_one("h3 a")["title"]}')
print(f'  select_one("p.price_color")  -> {first.select_one("p.price_color").get_text(strip=True)}')
print(f'  the star rating is in a CLASS -> {first.select_one("p.star-rating")["class"]}')

# Notice the last one. The rating isn't text on the page at all - it's the
# word "Three" in a class name, which the site's stylesheet turns into
# pictures of stars. Scraping is full of this: the thing a human sees and the
# thing in the HTML are often not the same thing.


# ================================================ 5. A page of records, to CSV
print("\n=== 5. The whole page, as records ===")

WORD_TO_NUMBER = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_book(pod):
    """One <article> in, one dictionary out."""
    link = pod.select_one("h3 a")
    price_text = pod.select_one("p.price_color").get_text(strip=True)
    rating_classes = pod.select_one("p.star-rating")["class"]   # e.g. ['star-rating', 'Three']

    return {
        "title": link["title"],                     # the full title; the visible text is truncated
        # Strip the currency symbol and convert. Everything scraped is a
        # string - the same lesson as reading a CSV. Note the £ has to go
        # before float() will look at it.
        "price": float(price_text.lstrip("£")),
        "rating": WORD_TO_NUMBER.get(rating_classes[-1], 0),
        "in_stock": "In stock" in pod.get_text(),
        "url": urllib.parse.urljoin(SITE, link["href"]),   # relative -> absolute
    }


books = [parse_book(pod) for pod in pods]

for book in books[:5]:
    print(f"  {book['rating']}*  £{book['price']:>6.2f}  {book['title']}")
print(f"  ... and {len(books) - 5} more")

data_dir = Path(__file__).resolve().parent / "data"
data_dir.mkdir(exist_ok=True)
out = data_dir / "scraped_books.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(books[0].keys()))
    writer.writeheader()
    writer.writerows(books)
print(f"\nsaved to {out.name}")


# ============================================================= 6. Politely, page 2
print("\n=== 6. Following the next link ===")

next_link = soup.select_one("li.next a")
if next_link:
    next_url = urllib.parse.urljoin(SITE, next_link["href"])
    print(f"next page: {next_url}")

    # One second between requests. Not because anything enforces it - because
    # you are using someone else's computer and they didn't have to let you.
    # A loop with no sleep in it is how a scraper becomes an attack.
    time.sleep(1)

    page2 = BeautifulSoup(get(next_url), "html.parser")
    more = [parse_book(pod) for pod in page2.select("article.product_pod")]
    print(f"got {len(more)} more books; first is {more[0]['title']!r}")

    all_books = books + more
    print(f"{len(all_books)} books total, average price £{sum(b['price'] for b in all_books) / len(all_books):.2f}")

# The site has 50 pages. Scraping all of them would be 50 requests over about
# a minute, which is fine here and would be rude somewhere real. Stopping at
# two is deliberate.


# ==============================================================================
# 7. WHY SCRAPERS BREAK
# ------------------------------------------------------------------------------
# An API is a promise: "this field will be called `title` and if that changes
# we'll tell you." A scraper has no promise. You are reading a document meant
# for human eyes, and the moment a designer renames a CSS class - something
# they'll do without a thought - your program stops working. Usually it won't
# even crash. It will quietly find zero books and save an empty file.
#
# So: check that you got a sensible NUMBER of results, not just that nothing
# raised an error. `if len(pods) == 0: raise` is the most valuable line in
# any scraper.
#
# And the other big one: this technique only sees what the server sent. If a
# page builds itself in your browser with JavaScript after loading - most
# modern web apps - the HTML you download will be nearly empty and none of
# your selectors will match. Signs you've hit this: View Source shows almost
# nothing, but Inspect shows a full page. Then you need a real browser driven
# by code (Playwright, Selenium), or - better - the Network tab in DevTools,
# where you can often find the JSON API the page itself is calling and use
# that instead. Doing that is usually less work AND less fragile.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Change "article.product_pod" to "article.product_pods". Nothing crashes.
#   You get an empty list and a header-only CSV. Now add a check that catches it.
# - Open books.toscrape.com in your browser, right-click a price, Inspect,
#   and find `p.price_color` yourself. That's the whole skill.
# - Scrape the rating and price of the most expensive book on page 1.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - Paste the HTML of ONE record and ask: "write the BeautifulSoup selectors
#   to pull out the title, price and rating." Pasting one record beats
#   describing the page, every time.
# - "Add a check that fails loudly if this scraper finds fewer than 10 books."
# - "This page is empty when I download it but full in my browser. Why?"
# - Careful: ask an AI to scrape a site and it will usually just do it,
#   without checking robots.txt or the terms and without a sleep() anywhere.
#   That judgement is yours, and it is the part of this lesson that matters.
# ==============================================================================
