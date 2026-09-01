"""
CLASS 1 - LOOPS
================================================================================

THE PROMPT
----------
Follow-up to the list lesson for my absolute beginners. Same data - my
reading list - but now add a second list of page counts, lined up with the
titles so that pages[0] goes with books[0].

Write ONE program that shows every kind of loop a beginner needs, in this
order:
1. Doing something once per item ("for each book...").
2. The same, but when you also need the position number.
3. Walking two lined-up lists at the same time.
4. Counting up with range().
5. A running total (the "accumulator" pattern).
6. A while loop, for when you don't know in advance how many times.
7. Stopping early with break, and skipping one with continue.

Rules:
- Single file, no imports, prints as it goes, output reads like a transcript.
- Before each loop, put a one-line comment saying WHEN a person would reach
  for that shape of loop. That's the part I actually want them to learn.
- Use f-strings for the printing.
- No functions or dictionaries yet.
- At the end, add a comment honestly describing what's annoying about
  keeping two lists lined up by hand.

================================================================================
"""

# Two lists that have to stay lined up by hand: books[0] was 502 pages,
# books[1] was 245 pages, and so on. Keep reading - this gets annoying.
books = [
    "The Overstory",
    "Piranesi",
    "Educated",
    "Klara and the Sun",
    "The Warmth of Other Suns",
    "Project Hail Mary",
]
pages = [502, 245, 352, 303, 622, 476]


# 1. The everyday loop: "do this once for each thing in the list."
#    `title` is a name that gets handed each book in turn.
print("--- Every book I read ---")
for title in books:
    print(f"I read {title}")


# 2. Reach for enumerate() when you also need the position - a numbered list,
#    "the 3rd one", that kind of thing.
print("\n--- Numbered, in the order I read them ---")
for position, title in enumerate(books):
    # enumerate starts at 0, so add 1 to make it read like a human list.
    print(f"{position + 1}. {title}")


# 3. Reach for zip() when two lists are lined up and you need both at once.
#    zip walks them in lockstep: first with first, second with second.
print("\n--- With page counts ---")
for title, page_count in zip(books, pages):
    print(f"{title} - {page_count} pages")


# 4. Reach for range() when you want to count, and there's no list involved.
#    range(1, 4) gives 1, 2, 3 - it stops one short, exactly like a slice.
print("\n--- Counting ---")
for n in range(1, 4):
    print(f"This is pass number {n}")


# 5. The accumulator: start a total at zero OUTSIDE the loop, add to it
#    INSIDE. If you start it inside, it resets every time - a classic bug.
print("\n--- Total pages ---")
total = 0
for page_count in pages:
    total = total + page_count  # could also be written: total += page_count
    print(f"running total: {total}")
print(f"All together: {total} pages")


# 6. Reach for while when you don't know how many rounds it will take, only
#    when to stop. Here: how many books until I've passed 1000 pages?
print("\n--- Reading until I hit 1000 pages ---")
pages_so_far = 0
how_many_books = 0
while pages_so_far < 1000:
    pages_so_far = pages_so_far + pages[how_many_books]
    how_many_books = how_many_books + 1
    print(f"after {how_many_books} book(s): {pages_so_far} pages")
print(f"It took {how_many_books} books to pass 1000 pages.")


# 7. break leaves the loop entirely; continue skips just this one round.
print("\n--- The first book over 500 pages ---")
for title, page_count in zip(books, pages):
    if page_count <= 500:
        continue  # not what I'm looking for - go straight to the next book
    print(f"Found it: {title}, {page_count} pages")
    break  # stop looking; don't check the rest


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# Every loop above is the same idea - "do this again" - wearing different
# clothes. The choice between them is really the question "what do I have?":
#     a list                  -> for x in things
#     a list, and I need #s   -> for i, x in enumerate(things)
#     two lists side by side  -> for a, b in zip(one, two)
#     just a count            -> for n in range(...)
#     a stopping condition    -> while ...
#
# THE ANNOYING PART (this is on purpose)
# ------------------------------------------------------------------------------
# `books` and `pages` are held together by nothing but discipline. If I sort
# `books`, the page counts silently stop matching and every number in this
# program becomes a lie - with no error message. If I append to one and forget
# the other, zip quietly drops the extra. Nothing in Python is checking.
#
# Hold onto that feeling. Dictionaries (Class 3) exist to fix exactly this.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Move `total = 0` to INSIDE the loop and watch the answer become garbage.
# - Delete the `break` in the last loop. What do you get instead, and why?
# - Add a seventh title to `books` but not to `pages`. Run it. Notice that
#   nothing crashes - which is worse than crashing.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Trace this while loop for me one round at a time, showing the value of
#    every variable, without rewriting the code."
# - "What happens if the while loop's condition never becomes false?"
# ==============================================================================
