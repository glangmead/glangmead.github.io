"""
CLASS 3 - DICTIONARIES
================================================================================

THE PROMPT
----------
In an earlier lesson my students kept a list of book titles and a separate
list of page counts, lined up by hand, and I made them feel how fragile that
is. Dictionaries are the payoff. Write the lesson that pays it off.

Cover, in this order:
1. A dictionary as a LOOKUP TABLE: title -> pages. Show that the lookup is
   by key, not by position, and that order of insertion doesn't matter.
2. Missing keys: the crash, and .get() with a fallback.
3. A dictionary as a RECORD: one book, several named fields. Contrast it
   with the lookup-table use - same syntax, completely different intent.
4. A list of records, which is what the two parallel lists should have been.
   Loop over it. Sort it.
5. Looping with .items(), .keys(), .values().
6. Counting things with a dictionary - the single most useful pattern there
   is. Use a real paragraph of text. Then show Counter doing it in one line.
7. Nested dictionaries, briefly, and how to reach into them safely.

Rules: single file, only `collections` imported, prints as it goes,
f-strings. Somewhere in the file, spell out when a list is the right choice
and when a dictionary is.

================================================================================
"""

from collections import Counter


# ================================================== 1. Dictionary as lookup table
print("=== 1. Look things up by name, not by position ===")

# Curly braces, and each entry is  key: value.
pages = {
    "The Overstory": 502,
    "Piranesi": 245,
    "Educated": 352,
    "Klara and the Sun": 303,
    "The Warmth of Other Suns": 622,
}

# Square brackets again, but now what goes inside is the KEY, not a position.
print(f'pages["Piranesi"] = {pages["Piranesi"]}')
print(f"how many entries: {len(pages)}")
print(f"is Educated in here? {'Educated' in pages}")

# Adding is just assigning to a key that isn't there yet.
pages["Project Hail Mary"] = 476
print(f"after adding one: {len(pages)} entries")

# The titles and page counts can no longer drift apart, because they aren't
# two things any more. That was the whole problem with the parallel lists.


# ==================================================== 2. Keys that aren't there
print("\n=== 2. When the key isn't there ===")
try:
    print(pages["Moby-Dick"])
except KeyError as error:
    print(f"crash: KeyError: {error}  (the key it couldn't find)")

# .get() asks politely: give me the value, or this fallback if it's missing.
print(f'pages.get("Moby-Dick") = {pages.get("Moby-Dick")}')
print(f'pages.get("Moby-Dick", 0) = {pages.get("Moby-Dick", 0)}')

# Use [] when a missing key means your program has a bug and should stop.
# Use .get() when a missing key is a normal thing that happens.


# ======================================================= 3. Dictionary as record
print("\n=== 3. The other job: one thing, several named fields ===")

book = {
    "title": "Piranesi",
    "author": "Susanna Clarke",
    "pages": 245,
    "year": 2020,
    "finished": True,
}

print(f"{book['title']} by {book['author']}, {book['year']}")

# Same syntax as the lookup table, but notice how different the INTENT is:
#   - lookup table: many entries, all the same kind, keys are data
#     ("what did the user type in?"), and it grows and shrinks.
#   - record: a fixed handful of entries, keys are field names you typed
#     yourself, and the shape stays the same.
# Class 3's other half - objects - is the better tool for the second job.


# ============================================ 4. A list of records (the real fix)
print("\n=== 4. What the two parallel lists should have been ===")

library = [
    {"title": "The Overstory", "author": "Richard Powers", "pages": 502, "price": 18.99},
    {"title": "Piranesi", "author": "Susanna Clarke", "pages": 245, "price": 16.00},
    {"title": "Educated", "author": "Tara Westover", "pages": 352, "price": 13.49},
    {"title": "Klara and the Sun", "author": "Kazuo Ishiguro", "pages": 303, "price": 17.00},
]

for entry in library:
    # :.2f because $16.0 is not how anyone writes money (see the arithmetic lesson)
    print(f"{entry['title']:<20} {entry['pages']:>4} pages  ${entry['price']:.2f}")

# Now sorting is safe. Nothing can drift, because each book is one object and
# the fields travel together.
print("\nSorted by length, longest first:")
longest_first = sorted(library, key=lambda entry: entry["pages"], reverse=True)
for entry in longest_first:
    print(f"  {entry['pages']:>4}  {entry['title']}")

# `key=lambda entry: entry["pages"]` reads as: "to sort these, look at each
# one's 'pages' field." A lambda is just a one-line function with no name.
# Sorting the old parallel lists would have silently corrupted the data.


# ================================================================ 5. Looping
print("\n=== 5. Three ways to loop over a dictionary ===")

print("keys only:")
for title in pages:                       # looping a dict gives you its KEYS
    print(f"  {title}")

print("values only:")
print(f"  total pages across all: {sum(pages.values())}")

print("both at once - use .items():")
for title, count in pages.items():
    if count > 500:
        print(f"  {title} is long: {count} pages")


# ============================================== 6. Counting: the killer pattern
print("\n=== 6. Counting things ===")

blurb = """Piranesi's house is infinite, its rooms endless, its corridors
lined with statues. He has explored the halls for years and has met only
one other person, whom he calls the Other, and the Other visits twice a
week to ask him questions about the house."""

# The pattern: for each thing, add one to its running count. .get(word, 0)
# handles the first time you see a word, when there's nothing to add to yet.
counts = {}
for word in blurb.lower().replace(",", "").replace(".", "").split():
    counts[word] = counts.get(word, 0) + 1

# Sort the (word, count) pairs by count, biggest first, take the top five.
top = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:5]
print("most common words, by hand:")
for word, count in top:
    print(f"  {word:<10} {count}")

# Counter is a dictionary that already knows how to do all of that.
print("\nmost common words, with Counter:")
for word, count in Counter(blurb.lower().split()).most_common(3):
    print(f"  {word:<10} {count}")


# ========================================================= 7. Nesting, briefly
print("\n=== 7. Dictionaries inside dictionaries ===")

authors = {
    "Susanna Clarke": {
        "born": 1959,
        "books": {"Piranesi": 2020, "Jonathan Strange & Mr Norrell": 2004},
    },
    "Richard Powers": {
        "born": 1957,
        "books": {"The Overstory": 2018, "Bewilderment": 2021},
    },
}

# Read the chain left to right, one hop at a time.
print(f'Piranesi came out in {authors["Susanna Clarke"]["books"]["Piranesi"]}')

# Chained [] means chained chances to crash. Chained .get() with {} fallbacks
# survives a missing name at any level.
missing = authors.get("Ursula K. Le Guin", {}).get("books", {}).get("The Dispossessed", "unknown")
print(f"The Dispossessed: {missing}")

# Any JSON you get back from the internet (Class 4) looks exactly like this:
# dictionaries and lists nested inside each other. This is the shape of data
# on the web.


# ==============================================================================
# LIST OR DICTIONARY?
# ------------------------------------------------------------------------------
#   Use a LIST when order matters, or when you'll walk through everything:
#       the books I read, in order; the lines of a file; steps in a recipe.
#   Use a DICTIONARY when you'll look one thing up by a name you already know:
#       pages by title; a user by their id; settings by their name.
#   The give-away question: "will I ever ask for the 3rd one?" -> list.
#                          "will I ever ask for the one called X?" -> dict.
#
#   Speed matters too, at scale: `"x" in a_list` checks every item one by one;
#   `"x" in a_dict` jumps straight there. With ten items you'll never notice.
#   With ten million, it's the difference between instant and lunch.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - In section 6, remove `.lower()` and see "Piranesi" and "piranesi" counted
#   as two different words. Cleaning data is most of real programming.
# - Change `counts.get(word, 0)` to `counts[word]` and read the crash.
# - Add a duplicate key to the `pages` dictionary. No error - the second one
#   silently wins. Keys are unique.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Rewrite my two parallel lists as a list of dictionaries, and show me one
#    bug that the rewrite makes impossible."
# - "Explain what key=lambda entry: entry['pages'] means, word by word."
# ==============================================================================
