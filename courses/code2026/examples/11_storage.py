"""
CLASS 5 - STORAGE
================================================================================

THE PROMPT
----------
My students can already write a CSV. Now I want them to understand the
LADDER of ways to keep data, and to be able to pick a rung.

Write ONE program that walks up it:
  rung 0: variables - gone the moment the program ends;
  rung 1: JSON - a whole nested structure saved and reloaded in one line;
  rung 2: CSV - flat rows, opens in Excel, loses all type information;
  rung 3: SQLite - a real database, one file, no server, built into Python.

For JSON: show a round trip, and show honestly what does NOT survive it -
tuples come back as lists, sets and objects and dates don't go in at all.

For SQLite: CREATE TABLE, INSERT with ? placeholders, SELECT with WHERE and
ORDER BY, one aggregate, and an UPDATE. Explain what committing means. Make
the ? placeholder point emphatic - show what f-string SQL does when a title
contains an apostrophe, and name the attack it enables.

Finish with a table telling them which rung to pick and why.

Rules: single file, stdlib only, writes into a scratch folder next to itself
and leaves the files behind, deletes any database from a previous run so it
can be run twice.

================================================================================
"""

import csv
import json
import sqlite3
from pathlib import Path

data_dir = Path(__file__).resolve().parent / "data"
data_dir.mkdir(exist_ok=True)

library = [
    {"title": "The Overstory", "author": "Richard Powers", "pages": 502, "year": 2018, "read": True},
    {"title": "Piranesi", "author": "Susanna Clarke", "pages": 245, "year": 2020, "read": True},
    {"title": "Educated", "author": "Tara Westover", "pages": 352, "year": 2018, "read": True},
    {"title": "Klara and the Sun", "author": "Kazuo Ishiguro", "pages": 303, "year": 2021, "read": False},
    {"title": "Bewilderment", "author": "Richard Powers", "pages": 288, "year": 2021, "read": False},
    # An apostrophe in the title. Harmless here; it matters a lot further down.
    {"title": "Bridget Jones's Diary", "author": "Helen Fielding", "pages": 288, "year": 1996, "read": True},
]


# ================================================== RUNG 0: nothing at all
print("=== Rung 0: in memory ===")
print(f"{len(library)} books in a Python list.")
print("Close the program and every one of them is gone. That's the problem.")


# ============================================================== RUNG 1: JSON
print("\n=== Rung 1: JSON ===")

books_json = data_dir / "library.json"

# indent=2 makes it human-readable. Leave it out and you get one long line -
# smaller, but nobody can read it in a text editor.
books_json.write_text(json.dumps(library, indent=2), encoding="utf-8")

print("the first few lines on disk:")
for line in books_json.read_text(encoding="utf-8").splitlines()[:8]:
    print(f"  {line}")

# ...and straight back into real Python values.
reloaded = json.loads(books_json.read_text(encoding="utf-8"))
print(f"\nreloaded {len(reloaded)} books")
print(f"and pages came back as a real number: {reloaded[0]['pages']!r}")
print(f"and read came back as a real True/False: {reloaded[0]['read']!r}")
print(f"identical to what we saved? {reloaded == library}")

print("\nWhat JSON does NOT survive:")
awkward = {
    "a_tuple": ("X", "O"),
    "a_number": 3,
}
back = json.loads(json.dumps(awkward))
print(f"  in:  {awkward}")
print(f"  out: {back}")
print(f"  the tuple came back as a {type(back['a_tuple']).__name__}")

for value, why in [({1, 2}, "a set"), (library[0].get, "a function")]:
    try:
        json.dumps(value)
    except TypeError as error:
        print(f"  {why} can't go in at all: TypeError: {error}")

# JSON has six types: string, number, true/false, null, list, object. Anything
# else - a set, a date, a Book object - you have to convert yourself on the
# way out and rebuild on the way in. Dates are almost always stored as
# strings, in the "2026-08-31" format, because it sorts correctly as text.


# =============================================================== RUNG 2: CSV
print("\n=== Rung 2: CSV ===")

books_csv = data_dir / "storage_library.csv"
with open(books_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(library[0].keys()))
    writer.writeheader()
    writer.writerows(library)

with open(books_csv, newline="", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

print(f"first row back from CSV: {csv_rows[0]}")
print("Everything is a string. `read` came back as the TEXT 'True', and")
print(f"bool('False') is {bool('False')} - a non-empty string is always truthy.")
print("CSV is a good exchange format and a bad storage format. Use it when a")
print("human is going to open it in a spreadsheet, and not otherwise.")


# ============================================================ RUNG 3: SQLite
print("\n=== Rung 3: SQLite ===")

db_path = data_dir / "library.db"
db_path.unlink(missing_ok=True)      # start fresh so this can be run twice

# SQLite is a whole relational database that lives in one ordinary file. No
# server, no install, no configuration - it ships inside Python. It is the
# most widely deployed database in the world: it's in your phone, your
# browser, and most of the apps on your laptop.
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE books (
        id     INTEGER PRIMARY KEY,   -- fills itself in, 1, 2, 3...
        title  TEXT NOT NULL,         -- refuses to store a row with no title
        author TEXT NOT NULL,
        pages  INTEGER,               -- a real number, not text
        year   INTEGER,
        read   INTEGER                -- SQLite has no boolean; 0 or 1
    )
""")

# The ? marks are placeholders. NEVER build SQL by pasting values into a
# string - see the demonstration below.
for book in library:
    cursor.execute(
        "INSERT INTO books (title, author, pages, year, read) VALUES (?, ?, ?, ?, ?)",
        (book["title"], book["author"], book["pages"], book["year"], int(book["read"])),
    )

# Nothing is permanent until you commit. Until then your changes exist only
# for this connection; a crash loses them. That all-or-nothing bundle is
# called a transaction, and it's a large part of why databases exist.
connection.commit()
cursor.execute("SELECT COUNT(*) FROM books")
print(f"the database now holds {cursor.fetchone()[0]} books")

# ---------------------------------------------------------------- asking questions
print("\nSELECT with a condition, sorted:")
cursor.execute("SELECT title, pages FROM books WHERE pages > ? ORDER BY pages DESC", (300,))
for title, pages in cursor.fetchall():
    print(f"  {pages:>4}  {title}")

print("\nLetting the database do the arithmetic:")
cursor.execute("SELECT author, COUNT(*), SUM(pages) FROM books GROUP BY author ORDER BY 2 DESC")
for author, how_many, total in cursor.fetchall():
    print(f"  {author}: {how_many} book(s), {total} pages")

# This is the real reason to climb to this rung. With JSON you must load the
# entire file into memory and write the loop yourself. With SQL you describe
# WHAT you want and the database works out how. At five books that's showing
# off. At five million it's the only option.

print("\nChanging one row:")
cursor.execute("UPDATE books SET read = 1 WHERE title = ?", ("Klara and the Sun",))
connection.commit()
cursor.execute("SELECT COUNT(*) FROM books WHERE read = 1")
print(f"  books marked read: {cursor.fetchone()[0]}")

# ------------------------------------------------- rows as dictionaries
# By default rows come back as tuples and you index them by position - the
# parallel-list problem all over again. row_factory fixes it.
connection.row_factory = sqlite3.Row
nicer = connection.cursor()
nicer.execute("SELECT * FROM books WHERE author LIKE ?", ("Richard%",))
for row in nicer.fetchall():
    print(f"  {dict(row)}")


# ================================================== why the ? actually matters
print("\n=== Why the ? placeholders matter ===")

# An apostrophe in the data ends the string early and the rest becomes SQL.
title = "Bridget Jones's Diary"

bad_sql = f"SELECT * FROM books WHERE title = '{title}'"
print(f"built with an f-string: {bad_sql}")
try:
    cursor.execute(bad_sql)
except sqlite3.OperationalError as error:
    print(f"  -> crashes: {error}")

cursor.execute("SELECT * FROM books WHERE title = ?", (title,))
print(f"with a placeholder: no drama, {len(cursor.fetchall())} row found")

# A crash is the harmless version. The dangerous version is when the text
# comes from a stranger and is chosen deliberately:
#
#     title = "x'; DROP TABLE books; --"
#
# Pasted into an f-string, that stops being a title and starts being a
# command. This is SQL injection - still, decades on, one of the most
# common serious vulnerabilities on the web. The fix is one character:
# pass values as parameters, never as text. AI assistants usually get this
# right, but not always - so check every SELECT you're handed for an
# f-string, and push back when you find one.

connection.close()


# ====================================================================== summary
print(f"""
=== Which rung? ===

  in memory   nothing to keep; it's a calculation, not a record
  JSON        settings, saved games, one program's own data, API responses;
              nested structure; small enough to load all at once
  CSV         a human will open it in a spreadsheet, or another tool demands it
  SQLite      more data than fits comfortably in memory, or you need to ask
              questions of it, or two things write to it at once, or you care
              that a half-finished change never lands
  a server    (Postgres, MySQL) many machines talking to one database at once;
              everything above still applies, plus operations work

  Default to JSON while you're learning. Move to SQLite the first time you
  find yourself writing a loop to search a JSON file.

All of it is in {data_dir}
  library.json  - open it, it's readable
  library.db    - open it with the DB Browser for SQLite app, it's not
""")


# ==============================================================================
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Delete the connection.commit() after the INSERTs and run it twice. The
#   second run finds no books. That is what "uncommitted" means.
# - Add a book with no title through the database. NOT NULL stops you. Try
#   the same in the JSON file - nothing stops you. That's what a schema is.
# - Change ORDER BY pages DESC to ORDER BY title.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Here's my JSON file. Write the CREATE TABLE that matches it, and the
#    script to load it in."
# - "Is this query safe from SQL injection?" - about any SQL you're given.
# - "I have 200,000 records and my JSON approach got slow. Walk me through
#    moving to SQLite without losing anything."
# ==============================================================================
