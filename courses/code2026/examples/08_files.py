"""
CLASS 4 - FILES
================================================================================

THE PROMPT
----------
My students have a list of book records in memory. Every time the program
ends, it's gone. Teach files as the answer to that.

Write ONE program that:
1. Explains what a path is - folders, relative vs absolute - using pathlib,
   and works no matter what folder the program is run from.
2. Writes a text file and reads it back.
3. Reads it line by line, and shows the trailing newline problem that bites
   everyone.
4. Appends to a file instead of overwriting, and shows that "w" DESTROYS
   what was there. I want them a little scared of "w".
5. Does the same job with the `with` statement and explains what it buys.
6. Writes and reads a CSV of my book records with the csv module, using
   DictReader so the rows come back as dictionaries they already understand.
7. Shows that everything read from a text file is a STRING, including
   numbers, and converts them.
8. Checks whether a file exists before reading it, and catches the error
   when it doesn't.

Rules: single file. It should create its own scratch folder next to itself
and leave the files behind so students can open them in a text editor. Say
`encoding="utf-8"` every time and explain once why.

================================================================================
"""

import csv
from pathlib import Path


# ============================================================ 1. What is a path
print("=== 1. Paths ===")

# __file__ is this program's own filename. .resolve() turns it into a full
# absolute path, and .parent is the folder containing it. Building paths this
# way means the program works no matter where you run it from - a very common
# source of "it worked on my machine".
here = Path(__file__).resolve().parent
data_dir = here / "data"          # the / operator joins path pieces
data_dir.mkdir(exist_ok=True)     # make it; don't complain if it's there

print(f"this program lives in: {here}")
print(f"scratch folder:        {data_dir}")
print(f"is it a folder?        {data_dir.is_dir()}")

notes_file = data_dir / "reading_notes.txt"
print(f"file we'll write:      {notes_file.name}")
print(f"its extension:         {notes_file.suffix}")


# ================================================== 2. Write it, read it back
print("\n=== 2. Write and read ===")

# encoding="utf-8" says how letters become bytes. Always say it. Leave it out
# and your program may work on your laptop and mangle every accent, curly
# quote and emoji on someone else's.
notes_file.write_text("Piranesi - finished in three sittings.\n", encoding="utf-8")

contents = notes_file.read_text(encoding="utf-8")
print(f"read back: {contents!r}")     # !r shows the quotes and the \n

# Note the \n at the end. A "line" in a text file is text followed by a
# newline character. That character is really there.


# ==================================================== 3. Line by line
print("\n=== 3. Line by line ===")

notes_file.write_text(
    "Piranesi - 5 stars\n"
    "The Overstory - 4 stars\n"
    "Educated - 5 stars\n",
    encoding="utf-8",
)

for line in notes_file.read_text(encoding="utf-8").splitlines():
    # .splitlines() strips the newlines for you. If you use .split("\n")
    # instead you get an empty string on the end - the classic off-by-one.
    print(f"  line: {line!r}")

print("with .split(chr(10)) instead, notice the ghost at the end:")
print(f"  {notes_file.read_text(encoding='utf-8').split(chr(10))}")


# ====================================================== 4. "w" destroys. "a" adds.
print("\n=== 4. The two ways to open for writing ===")

log = data_dir / "log.txt"

# "w" = write. It empties the file first. There is no undo and no warning.
with open(log, "w", encoding="utf-8") as f:
    f.write("first line\n")

with open(log, "w", encoding="utf-8") as f:      # the first line is GONE now
    f.write("second line\n")

print(f'after two opens with "w": {log.read_text(encoding="utf-8")!r}')

# "a" = append. It adds to the end.
with open(log, "a", encoding="utf-8") as f:
    f.write("third line\n")

print(f'after one open with "a":  {log.read_text(encoding="utf-8")!r}')

# Be suspicious of "w" in code you didn't write. Ask: what was in that file
# before? If an AI hands you a script that opens your file with "w", check
# it before you run it.


# =============================================================== 5. `with`
print("\n=== 5. What `with` is for ===")

# An open file is a resource the operating system is holding for you. It has
# to be closed, or your writes may sit in a buffer and never land on disk.
# You could do it by hand:
f = open(log, "a", encoding="utf-8")
f.write("fourth line\n")
f.close()                       # easy to forget; skipped entirely if the
                                # lines above raise an error

# ...but `with` closes it for you when the block ends, even if the code
# inside crashes. Use `with`. Always.
with open(log, "a", encoding="utf-8") as f:
    f.write("fifth line\n")

print(f"log now has {len(log.read_text(encoding='utf-8').splitlines())} lines")


# ==================================================================== 6. CSV
print("\n=== 6. CSV: a spreadsheet as a text file ===")

library = [
    {"title": "The Overstory", "author": "Richard Powers", "pages": 502},
    {"title": "Piranesi", "author": "Susanna Clarke", "pages": 245},
    {"title": "Educated", "author": "Tara Westover", "pages": 352},
    # A comma inside a value is exactly why you use the csv module instead of
    # gluing strings together with commas yourself:
    {"title": "Tomorrow, and Tomorrow, and Tomorrow", "author": "Gabrielle Zevin", "pages": 416},
]

books_csv = data_dir / "library.csv"

# newline="" is required by the csv module on Windows. Nobody remembers why.
# Copy it, and don't lose sleep.
with open(books_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "author", "pages"])
    writer.writeheader()
    writer.writerows(library)

print("the raw file, exactly as it sits on disk:")
for line in books_csv.read_text(encoding="utf-8").splitlines():
    print(f"  {line}")
# Look at the last row: csv put quotes around the title with commas in it,
# and will strip them again on the way back in.

print("\nread back with DictReader - each row is a dictionary:")
with open(books_csv, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    print(f"  {row}")


# =========================================== 7. Everything on disk is a string
print("\n=== 7. Files have no idea what a number is ===")

pages_field = rows[0]["pages"]
print(f"rows[0]['pages'] is {pages_field!r}, type {type(pages_field).__name__}")

try:
    print(sum(row["pages"] for row in rows))
except TypeError as error:
    print(f"so this fails: TypeError: {error}")

# int() converts. This step - taking text off disk or off the network and
# turning it into real values - is called parsing, and it is where a large
# share of all real-world bugs live.
total = sum(int(row["pages"]) for row in rows)
print(f"after int(): {total} pages")


# =========================================== 8. Files that aren't there
print("\n=== 8. When the file isn't there ===")

missing = data_dir / "does_not_exist.txt"

# Ask first...
if missing.exists():
    print(missing.read_text(encoding="utf-8"))
else:
    print(f"{missing.name} isn't there, so I won't try to read it")

# ...or just try, and handle the failure. Both are fine. The second is better
# when the file could vanish between the check and the read.
try:
    missing.read_text(encoding="utf-8")
except FileNotFoundError as error:
    print(f"caught it: FileNotFoundError: {error.strerror}")

print(f"\nGo look in {data_dir} with Finder or a text editor.")
print("Everything this program wrote is sitting there as plain text.")


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# 1. Build paths with pathlib and __file__, never by pasting in "/Users/you/...".
# 2. Always pass encoding="utf-8".
# 3. "w" destroys, "a" adds. Read the mode before you run someone else's code.
# 4. Use `with`.
# 5. Text files hold text. Numbers come back as strings until you convert them.
# 6. Use the csv module for CSV. Do not split on commas by hand.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Open library.csv in Excel or Numbers. It's the same file you just printed.
# - Add a book whose title contains a double quote and see what csv does.
# - Change encoding="utf-8" to encoding="ascii" and write a title with an
#   accent in it. Read the error - you've now met the encoding bug on purpose
#   instead of at 2am.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "This script opens my file with mode 'w'. What happens to what's already
#    in it?"  (Ask this EVERY time. It is the cheapest insurance there is.)
# - "Rewrite the CSV part using pandas, and tell me what I gain and what I
#    give up."
# ==============================================================================
