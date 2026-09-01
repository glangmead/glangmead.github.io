"""
LISTS
================================================================================
A program to keep track of what I read this year.

That's the whole reason it exists. Everything below is one person, with a
shelf of books and a question, reaching for the simplest thing that answers it.

Read it top to bottom. It prints as it goes, so you can follow along.
================================================================================
"""

# A list is written with square brackets, items separated by commas.
# This list holds strings (text). Order matters: it's the order I read them.
books = [
    "The Overstory",
    "Piranesi",
    "Educated",
    "Klara and the Sun",
    "The Warmth of Other Suns",
    "Project Hail Mary",
]

print("The whole list:", books)

# len() tells you how many items are in the list.
print("How many books:", len(books))

# Positions are numbered starting at ZERO, not one. This is the #1 beginner
# surprise in every programming language. books[0] is the FIRST book.
print("The first book:", books[0])
print("The third book:", books[2])

# A negative position counts backward from the end. -1 is the last item.
print("The last book:", books[-1])

# A slice takes a run of items. books[0:3] means "from 0, up to but NOT
# including 3" - so items 0, 1, 2. Three books, not four.
print("The first three:", books[0:3])
print("Everything after the first three:", books[3:])

# .append() adds one item onto the end. Notice it changes `books` itself
# rather than handing back a new list - there is no `books = ` here.
books.append("Tomorrow, and Tomorrow, and Tomorrow")
print("After appending, the list is:", books)
print("And now the count is:", len(books))

# .remove() takes the item's VALUE, not its position, and deletes the first
# match. It is an error if the value isn't there.
books.remove("Educated")
print("After removing 'Educated':", books)

# `in` asks a yes/no question and gives back True or False.
print("Did I read Piranesi?", "Piranesi" in books)
print("Did I read Moby-Dick?", "Moby-Dick" in books)

# .index() finds WHERE something is.
print("Piranesi is at position:", books.index("Piranesi"))

# sorted() hands back a NEW list in alphabetical order and leaves the
# original alone. Compare the next two lines carefully.
print("Sorted alphabetically:", sorted(books))
print("But the original is untouched:", books)

# .sort() is the other one: it rearranges the list in place and hands back
# nothing. This pair - sorted() vs .sort() - trips up everyone once.
books.sort()
print("After books.sort(), the original IS changed:", books)


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# 1. Counting starts at 0. The "third book" is books[2].
# 2. A slice stops one short: books[0:3] gives you three items, 0 through 2.
# 3. Some operations change the list you already have (.append, .remove,
#    .sort) and some hand you a brand new one (sorted). The tell: if you had
#    to write `x = ` in front of it, it made something new.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Change books[0:3] to books[1:3] and predict the output BEFORE you run it.
# - Try books[10]. Read the error message out loud. That error - IndexError -
#   is one you will meet a hundred more times.
# - Swap sorted(books) for sorted(books, reverse=True).
#
# ==============================================================================
# IN CLASS: PROMPTS TO RUN LIVE
# ------------------------------------------------------------------------------
# Paste this whole file in first, then ask for one of these. We run them on
# the projector and read the answer together. You have just read this code,
# so you are qualified to judge what comes back - that's the point.
#
# PORT IT
#   "Port this to JavaScript, Swift, Java and C#. Same output, same comments,
#    same order. Show them side by side, nothing else."
#   -> Find the list in each one. Find the loop. Find where counting starts.
#      Four languages disagree about almost everything except the ideas.
#      (We can't run the Swift in class. Don't assume it compiles.)
#
# EXTEND IT
#   "This program uses append, remove, index, sort and sorted. What are the
#    ten other list operations I'll actually reach for in my first year?
#    One line of code each, with the result as a comment. No explanations."
#   -> Then we run it. "No explanations" is doing real work in that prompt;
#      try it without and see how much you have to scroll.
#
# BREAK IT
#   "Give me three inputs that make this program crash, and say which line
#    breaks for each one."
#   -> Then we actually try them. Sometimes it's wrong about which line.
#      Being wrong here is more useful to you than being right.
#
# CRITIQUE IT
#   "What would a professional Python programmer change about this code?
#    Rank the changes by how much they actually matter."
#   -> Argue with the ranking. Some of it is taste, some of it is real, and
#      telling those apart is most of what senior people get paid for.
#
# SCALE IT
#   "What in this program breaks if the list has ten million books in it?"
#   -> Nothing you've seen yet explains the answer. That's fine. Notice which
#      words in the reply you don't know; they're the syllabus for later.
# ==============================================================================
