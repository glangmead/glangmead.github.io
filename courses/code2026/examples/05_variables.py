"""
CLASS 2 - VARIABLES (values versus references)
================================================================================

THE PROMPT
----------
I deliberately saved variables until AFTER lists and functions, because I
want to teach the thing that actually matters: a variable is a NAME STUCK ON
a value, not a box holding a copy of it.

Write ONE program that makes that visible. Build it in this order, and make
each step a surprise that the next step explains:

1. Two names for the same list. Change it through one name; show it changed
   "through" the other. Prove they are the same object with id().
2. Do the same with numbers and strings and show that the surprise does NOT
   happen. Explain what mutable/immutable means using what just happened.
3. `is` versus `==`.
4. Hand a list to a function; the function changes it; the caller's list is
   changed. Hand a number to a function; it isn't.
5. How to actually make a copy, and the trap where the copy isn't deep
   enough because the list contains lists.
6. The mutable-default-argument trap, with the fix.

Rules: single file, only `copy` imported, prints as it goes, no cleverness.
Print id() values so they can see the identity, but tell them the exact
numbers are meaningless and change every run.

================================================================================
"""

import copy


# =========================================================== 1. Two names, one list
print("=== 1. Two names for one list ===")
my_shelf = ["The Overstory", "Piranesi"]
your_shelf = my_shelf          # this does NOT make a second list

your_shelf.append("Educated")  # I only touched `your_shelf`...

print(f"your_shelf: {your_shelf}")
print(f"my_shelf:   {my_shelf}   <-- changed too!")

# id() is the object's address in memory - "which thing is this, exactly".
# The numbers are meaningless and different every run. Only "same or
# different" matters.
print(f"id(my_shelf)   = {id(my_shelf)}")
print(f"id(your_shelf) = {id(your_shelf)}")
print(f"Same object?     {my_shelf is your_shelf}")

# The picture to hold in your head:
#
#     my_shelf   ----\
#                     >----> [ "The Overstory", "Piranesi", "Educated" ]
#     your_shelf ----/
#
# NOT this:
#
#     my_shelf   ---> [ ... ]        your_shelf ---> [ ... a copy ... ]
#
# `=` never copies anything. It points a name at a value.


# ======================================================== 2. Why numbers feel safe
print("\n=== 2. The same move with a number ===")
my_count = 2
your_count = my_count
your_count = your_count + 1

print(f"your_count: {your_count}")
print(f"my_count:   {my_count}   <-- NOT changed")

# Why the difference? Not because numbers are "copied". Because `+` cannot
# change a 2 into a 3 - there is no such operation. 2 is 2 forever. So
# `your_count + 1` had to make a NEW number, and `=` re-pointed the name at
# it. `my_count` still points at the old 2.
#
# Values that cannot be changed:  numbers, strings, True/False, None, tuples.
# Values that CAN be changed:     lists, dictionaries, sets, most objects.
# The jargon: immutable and mutable.

print("\nStrings are immutable too:")
title = "piranesi"
shouted = title.upper()
print(f"title:   {title}    <-- .upper() did not change it")
print(f"shouted: {shouted}   <-- it made a new string")
# There is no title.append(). You can only build a new string from the old.
# Lists have .append() precisely BECAUSE they are mutable.


# ================================================================ 3. is vs ==
print("\n=== 3. `is` vs `==` ===")
left = ["a", "b"]
right = ["a", "b"]
same = left

print(f"left == right : {left == right}    (same CONTENTS?)")
print(f"left is right : {left is right}    (same OBJECT?)")
print(f"left is same  : {left is same}")

right.append("c")
print(f"after right.append('c'):  left={left}  right={right}")
same.append("c")
print(f"after same.append('c'):   left={left}  same={same}")

# Use == essentially always. Use `is` only for None: `if x is None:`.


# ================================================= 4. What functions can do to you
print("\n=== 4. Handing values to functions ===")


def add_a_book(shelf, title):
    """Adds to the shelf it was given. Returns nothing - on purpose."""
    shelf.append(title)  # mutates the caller's list


def add_one(number):
    """Tries to change the caller's number. Cannot."""
    number = number + 1  # only re-points the local name `number`
    return number


shelf = ["Piranesi"]
count = 1

add_a_book(shelf, "Educated")
add_one(count)

print(f"shelf after add_a_book:  {shelf}   <-- the function changed MY list")
print(f"count after add_one:     {count}     <-- unchanged")
print(f"add_one's return value:  {add_one(count)}  <-- the answer was in the return")

# Same rule as before, no exception: the function got a NAME pointing at the
# caller's value. If the value is mutable, the function can change it out
# from under you. If it's immutable, it can't.
#
# This is why "the AI's function wrecked my data" happens. When you get code
# back, ask: does this function change what I gave it, or hand back something
# new? A function should do one or the other and say which in its name.


# ================================================================= 5. Copying
print("\n=== 5. Making an actual copy ===")
original = ["The Overstory", "Piranesi"]
real_copy = original.copy()     # also: list(original)  or  original[:]

real_copy.append("Educated")
print(f"original:  {original}")
print(f"real_copy: {real_copy}")
print(f"Same object? {original is real_copy}")

print("\n...but a copy is only one layer deep:")
shelves = [["Overstory", "Piranesi"], ["Educated"]]
shallow = shelves.copy()

shallow[0].append("SNUCK IN")   # reaching INSIDE the copy

print(f"shallow: {shallow}")
print(f"shelves: {shelves}   <-- changed!")

# .copy() made a new outer list, but the two INNER lists are still shared:
#
#     shelves ---> [ * , * ]
#                    |   |
#                    v   v
#                  [..] [..]        <-- one copy of each, pointed at twice
#                    ^   ^
#                    |   |
#     shallow ---> [ * , * ]
#
# copy.deepcopy() follows the pointers all the way down and copies everything.
deep = copy.deepcopy(shelves)
deep[0].append("only in the deep copy")
print(f"\nafter deepcopy and edit:")
print(f"deep:    {deep}")
print(f"shelves: {shelves}   <-- safe this time")


# ==================================================== 6. The default-argument trap
print("\n=== 6. The trap that catches everyone once ===")


def log_book_BROKEN(title, so_far=[]):
    """Looks innocent. Is not."""
    so_far.append(title)
    return so_far


print(f"first call:  {log_book_BROKEN('Piranesi')}")
print(f"second call: {log_book_BROKEN('Educated')}   <-- where did Piranesi come from?")
print(f"third call:  {log_book_BROKEN('Klara')}")

# The default value `[]` is created ONCE, when Python reads the `def` line -
# not once per call. Every call that doesn't pass a list shares that same
# list, forever, for the life of the program.


def log_book_FIXED(title, so_far=None):
    """The standard fix: default to None, make the list inside."""
    if so_far is None:
        so_far = []          # a fresh list on every call
    so_far.append(title)
    return so_far


print(f"\nfixed, first call:  {log_book_FIXED('Piranesi')}")
print(f"fixed, second call: {log_book_FIXED('Educated')}")


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# There is only ONE rule in this whole file:
#
#     `=` points a name at a value. It never copies.
#
# Everything else follows from whether that value can be changed in place.
# Numbers and strings can't, so you never notice. Lists and dictionaries can,
# so you notice hard.
#
# SEE IT ANIMATED
# ------------------------------------------------------------------------------
# Paste sections 1 and 5 into https://pythontutor.com and step through them.
# The arrows in its diagram are literally the arrows drawn in the comments
# above. This is the single best twenty minutes you can spend on this topic.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - In section 1, change `your_shelf = my_shelf` to `your_shelf = my_shelf.copy()`
#   and predict both prints before running.
# - In section 4, make add_a_book return `shelf + [title]` instead of
#   appending. Which version would you rather receive from an AI, and why?
# - Call log_book_BROKEN a fourth time. The list keeps growing across calls.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Draw me an ASCII diagram of the names and objects in memory after each
#    line of section 1."
# - "Does this function modify its argument or return a new value?" - a good
#    question to ask about EVERY function an AI writes for you.
# - "Find every place in this file where a mutable value is shared when it
#    probably shouldn't be."
# ==============================================================================
