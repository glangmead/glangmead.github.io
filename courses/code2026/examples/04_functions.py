"""
CLASS 2 - FUNCTIONS
================================================================================

THE PROMPT
----------
My beginners have seen lists, loops and arithmetic. Now functions.

Write ONE program, still about my reading list, that teaches functions by
showing the SAME job done three ways, worst to best:
  (a) copy-pasted three times,
  (b) pulled into a function,
  (c) that function used inside a bigger function.

Then, in the same file, demonstrate:
- a function that PRINTS versus a function that RETURNS, and why mixing
  them up is the single most common beginner bug;
- what a function that returns nothing actually gives you;
- default values for arguments;
- calling with names instead of position;
- a docstring, and how to read one with help().

Rules: single file, no imports, runs top to bottom, f-strings. Comment WHY,
not WHAT. Keep each function under ten lines.

================================================================================
"""

books = ["The Overstory", "Piranesi", "Educated"]
pages = [502, 245, 352]
prices = [18.99, 16.00, 13.49]


# ============================================================== (a) the bad way
print("--- Three books, three copies of the same arithmetic ---")

value = 502 / 18.99
print(f"The Overstory: {round(value, 1)} pages per dollar")

value = 245 / 16.00
print(f"Piranesi: {round(value, 1)} pages per dollar")

value = 352 / 13.49
print(f"Educated: {round(value, 1)} pages per dollar")

# Three near-identical blocks. If the formula is wrong, it is wrong in three
# places. If I buy a fourth book, I write it a fourth time. This is the itch
# that functions scratch.


# ============================================================ (b) the function
def pages_per_dollar(page_count, price):
    """How many pages you get for each dollar spent.

    Give it a page count and a price; it hands back a number.
    It does not print anything - that's the caller's business.
    """
    return page_count / price


print("\n--- The same thing, once ---")
for title, page_count, price in zip(books, pages, prices):
    value = pages_per_dollar(page_count, price)
    print(f"{title}: {round(value, 1)} pages per dollar")

# Read the definition and the call as two separate moments:
#   `def` says what the machine IS. Nothing happens.
#   `pages_per_dollar(502, 18.99)` is when it RUNS.
# The names `page_count` and `price` only exist inside the function, for the
# length of one call. They are not the same as `pages` and `prices` outside.


# ================================================= (c) functions using functions
def best_value(titles, page_counts, price_list):
    """Return the title with the most pages per dollar."""
    winner = titles[0]
    best_so_far = pages_per_dollar(page_counts[0], price_list[0])
    for title, page_count, price in zip(titles, page_counts, price_list):
        # Small function used inside a bigger one. This is the whole game:
        # solve a small piece, name it, then stop thinking about how it works.
        score = pages_per_dollar(page_count, price)
        if score > best_so_far:
            best_so_far = score
            winner = title
    return winner


print("\n--- Best value ---")
print(f"Cheapest reading per page: {best_value(books, pages, prices)}")


# ================================================ print versus return (READ THIS)
def shout_it(title):
    """Prints. Hands back nothing."""
    print(f"  (inside shout_it) {title.upper()}")


def make_it_loud(title):
    """Prints nothing. Hands back a string."""
    return title.upper()


print("\n--- print vs return ---")
result_a = shout_it("Piranesi")
result_b = make_it_loud("Piranesi")

print(f"shout_it printed while it ran, and gave back: {result_a}")
print(f"make_it_loud printed nothing, and gave back: {result_b}")

# `None` is Python's word for "no value at all". A function with no `return`
# hands back None automatically. This is why beginners see
#     favorites = sort_my_books(books)
#     print(favorites)      ->  None
# The function worked fine; it just didn't hand anything back.
#
# Rule of thumb: a function that computes should RETURN. Only the outermost
# layer of a program should print. A function that prints can only ever be
# used one way; a function that returns can be used a hundred ways.
print(f"\nBecause it returns, I can keep using it: {make_it_loud('Educated') + '!!!'}")


# ============================================= defaults and calling by name
def describe(title, page_count, pace=30):
    """Estimate reading time.

    pace is pages per day; it defaults to 30 if you don't say.
    """
    days = page_count / pace
    return f"{title} takes about {round(days)} days at {pace} pages/day"


print("\n--- Default values ---")
print(describe("The Overstory", 502))               # pace not given -> 30
print(describe("The Overstory", 502, 100))          # by position
print(describe("The Overstory", 502, pace=15))      # by name - clearer
print(describe(page_count=502, title="The Overstory"))  # names, any order

# Naming your arguments at the call site is free documentation. Compare:
#     resize(img, 100, 200, True, False)
#     resize(img, width=100, height=200, keep_ratio=True, sharpen=False)
# When an AI hands you the first kind, ask it for the second.


# ===================================================== reading the instructions
print("\n--- The docstring is the instruction manual ---")
help(describe)


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# 1. Defining a function runs nothing. Calling it runs it.
# 2. A function's argument names are private to that function.
# 3. print shows a human. return hands a value back to the program. They are
#    not alternatives - they do completely different jobs.
# 4. No return means None.
# 5. A good function has a name that says what it gives you, and a docstring
#    that a stranger can read without reading the body.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Delete `return` from pages_per_dollar (leave the expression). Run it.
#   Everything becomes None. Now you have seen the bug in the wild.
# - Call pages_per_dollar(18.99, 502) - arguments backwards. It does not
#   crash. It gives a confidently wrong answer. Positional arguments do that.
# - Add a `pace` default of 0 and see which error you get.
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Here are three near-identical blocks of code. What function would remove
#    the duplication? Show me the function but don't rewrite my program yet."
# - "Write three test cases for pages_per_dollar, including one where the
#    price is zero."  (Then decide what SHOULD happen in that case - that's
#    your job, not the AI's.)
# ==============================================================================
