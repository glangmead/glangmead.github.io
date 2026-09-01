"""
CLASS 3 - OBJECTS
================================================================================

THE PROMPT
----------
My students just learned dictionaries and built a list of book records. Now
teach objects as the NEXT step in that same story, not as a new topic.

Structure it as an upgrade with a reason at each step:
1. Start from the list-of-dictionaries. Show three concrete things that go
   wrong with it - a typo in a key, a missing field, and behaviour that has
   nowhere to live.
2. Write a Book class that fixes them. Explain `self` as plainly as you can:
   it is just the first argument, and it means "the particular book this call
   is about".
3. Add a method, and make the point that a method is a function that comes
   with its data attached.
4. Add __repr__ so printing one isn't useless.
5. Show @dataclass writing most of that for you, and say when to use which.
6. Show a Library class that HOLDS Books - an object made of objects.
7. Tie it back to the variables lesson: objects are mutable, so two names for
   one book is the same trap as two names for one list.

Rules: single file, `dataclasses` may be imported, prints as it goes. No
inheritance - I want them to leave thinking objects are simple, because at
this level they are.

================================================================================
"""

from dataclasses import dataclass, field


# ======================================================= 1. Where dicts run out
print("=== 1. What goes wrong with a list of dictionaries ===")

library_as_dicts = [
    {"title": "Piranesi", "author": "Susanna Clarke", "pages": 245, "read": 245},
    {"title": "The Overstory", "author": "Richard Powers", "pages": 502, "read": 130},
]

first = library_as_dicts[0]

# Problem 1: a typo in a key is not a typo to Python. It's a new key.
first["titel"] = "Piranessi"          # meant "title". No error. No warning.
print(f"the record now has a bogus field: {list(first.keys())}")

# Problem 2: nothing says what fields a book must have. This is a "book":
sketchy = {"title": "Educated"}       # no author, no pages. Perfectly legal.
print(f"this is also a 'book': {sketchy}")

# Problem 3: behaviour has nowhere to live. "How far through am I?" is a fact
# ABOUT a book, but it has to be written as a loose function somewhere else,
# and nothing connects the two.
def progress_of(record):
    return record["read"] / record["pages"]

print(f"progress, computed at arm's length: {progress_of(library_as_dicts[1]):.0%}")


# ================================================================ 2. A class
print("\n=== 2. The same thing as a class ===")


class Book:
    # __init__ runs once, when a new Book is made. Its job is to attach the
    # fields. `self` is the book being made - Python passes it in for you.
    def __init__(self, title, author, pages, read=0):
        self.title = title      # "on THIS book, set title to the title given"
        self.author = author
        self.pages = pages
        self.read = read


piranesi = Book("Piranesi", "Susanna Clarke", 245, read=245)
overstory = Book("The Overstory", "Richard Powers", 502, read=130)

# A dot instead of square brackets. That's the visible difference.
print(f"{piranesi.title} by {piranesi.author}")

# And now the typo IS an error, at the moment you make it:
try:
    print(overstory.titel)
except AttributeError as error:
    print(f"caught the typo: AttributeError: {error}")

# And you cannot make a Book without an author, because __init__ demands one:
try:
    Book("Educated")
except TypeError as error:
    print(f"caught the missing field: TypeError: {error}")


# ================================================================= 3. Methods
print("\n=== 3. Behaviour that lives with the data ===")


class Book:  # same class again, now with things it can DO
    def __init__(self, title, author, pages, read=0):
        self.title = title
        self.author = author
        self.pages = pages
        self.read = read

    def progress(self):
        """What fraction of this book I've read."""
        return self.read / self.pages

    def is_finished(self):
        return self.read >= self.pages

    def read_pages(self, how_many):
        """Record some reading. Changes this book."""
        self.read = min(self.read + how_many, self.pages)

    def __repr__(self):
        """What Python should show when it prints this object."""
        return f"<Book {self.title!r} {self.read}/{self.pages}>"


piranesi = Book("Piranesi", "Susanna Clarke", 245, read=245)
overstory = Book("The Overstory", "Richard Powers", 502, read=130)

print(f"{overstory.title}: {overstory.progress():.0%} done")
print(f"finished? {overstory.is_finished()}")

overstory.read_pages(200)
print(f"after reading 200 more: {overstory.progress():.0%}")

# `overstory.progress()` is Python's way of writing `progress(overstory)`.
# That is all the dot does. The thing before the dot becomes `self`. There is
# no magic here, and if you remember only one sentence about objects, that's
# a good one to keep.


# =============================================================== 4. __repr__
print("\n=== 4. Why __repr__ matters ===")
print(f"with __repr__:    {overstory}")
print(f"a whole list:     {[piranesi, overstory]}")
# Without __repr__ that would have printed <__main__.Book object at 0x10f2c3d10>,
# which tells you nothing. Every class you keep should have one.


# ============================================================== 5. @dataclass
print("\n=== 5. Letting Python write the boring part ===")


@dataclass
class Album:
    """@dataclass writes __init__ and __repr__ from these field lines."""
    title: str
    artist: str
    year: int
    tracks: int = 0

    def is_long(self):
        return self.tracks > 12


music_box = Album("Music Box", "Mariah Carey", 1993, tracks=10)
print(music_box)                       # free __repr__
print(f"long album? {music_box.is_long()}")
print(f"equality is free too: {music_box == Album('Music Box', 'Mariah Carey', 1993, 10)}")

# Reach for @dataclass when the class is mostly "a bundle of named fields".
# Write __init__ by hand when creating the object involves real work -
# validating input, opening a file, computing something.


# ========================================================== 6. Objects of objects
print("\n=== 6. An object made of objects ===")


@dataclass
class Library:
    name: str
    # A mutable default needs `field(default_factory=list)` - this is the
    # same trap as `def f(items=[])` from the variables lesson, and
    # dataclasses refuse to let you write it the broken way.
    books: list = field(default_factory=list)

    def add(self, book):
        self.books.append(book)

    def total_pages(self):
        return sum(book.pages for book in self.books)

    def unfinished(self):
        return [book for book in self.books if not book.is_finished()]


shelf = Library("Living room")
shelf.add(piranesi)
shelf.add(overstory)
shelf.add(Book("Educated", "Tara Westover", 352))

print(f"{shelf.name}: {len(shelf.books)} books, {shelf.total_pages()} pages")
print(f"still reading: {shelf.unfinished()}")

# `[book for book in self.books if ...]` is a list comprehension: "the list of
# each book, for every book in self.books, where the condition holds." It's the
# same as a for-loop with an append, written on one line. AI-written Python is
# full of these, so learn to read them even before you write them.


# ============================================ 7. Objects are mutable (careful)
print("\n=== 7. Same trap as the variables lesson ===")

my_copy = piranesi          # NOT a copy. A second name for the same Book.
my_copy.title = "PIRANESI (annotated)"
print(f"piranesi.title is now: {piranesi.title}")
print(f"same object? {piranesi is my_copy}")

# Everything from the variables lesson applies unchanged. Objects are
# mutable, so `=` sharing them is the same hazard as `=` sharing a list.
# When a function takes an object, ask the same question: does it change what
# I gave it, or hand me back something new?


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# A dictionary and an object hold the same information. The difference:
#   - a dict's keys are DATA, decided while the program runs;
#     an object's attributes are DESIGN, decided when you write the class.
#   - a dict is a pile of values; an object is values plus the operations
#     that make sense on them.
#   - a typo in a dict key is silent; a typo in an attribute name is an error.
#
# The give-away question: "do I know the field names while I'm typing?"
# Yes -> object.  No, they come from data or a user -> dictionary.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Delete `__repr__` and print a Book. That ugly output is what most objects
#   look like by default.
# - Give Library a `books: list = []` default instead of field(default_factory).
#   Python will refuse to define the class. Read what it says.
# - Add a `pages_left()` method and use it in the report.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Convert my list of dictionaries into a class, and list every bug the
#    conversion would have prevented."
# - "Should this be a dataclass or a regular class? Argue both sides."
# - "Rewrite the list comprehension in unfinished() as a plain for-loop so I
#    can see they're the same." (A great habit whenever AI code gets dense.)
# ==============================================================================
