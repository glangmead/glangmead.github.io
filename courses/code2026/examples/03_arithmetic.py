"""
CLASS 1 - ARITHMETIC
================================================================================

THE PROMPT
----------
Third piece for my beginners' class, same reading-list data plus what each
book cost me.

Write ONE program about arithmetic. Cover: + - * /, the two kinds of
division (/ and //), remainder with %, powers, order of operations,
round(), and the difference between a whole number and a decimal number.

Two things I specifically want them to SEE, not just be told:
- that 0.1 + 0.2 is not 0.3, and why that matters for money;
- that dividing by zero crashes, and what the crash looks like.

Rules: single file, no imports except `statistics` if you need it, prints as
it goes, f-strings, comment the surprising parts only. Keep every number
small enough to check by hand.

================================================================================
"""

pages = [502, 245, 352, 303, 622, 476]
prices = [18.99, 16.00, 13.49, 17.00, 20.00, 15.99]  # dollars, paperback

# ------------------------------------------------------------------ the basics
print("--- Four operations ---")
print(f"add:      502 + 245 = {502 + 245}")
print(f"subtract: 502 - 245 = {502 - 245}")
print(f"multiply: 502 * 2   = {502 * 2}")
print(f"divide:   502 / 2   = {502 / 2}")

# Notice the .0 on that last one. `/` ALWAYS produces a decimal number
# (a "float"), even when it divides evenly. 502 / 2 is 251.0, not 251.
print(f"type of 502 + 245: {type(502 + 245).__name__}")
print(f"type of 502 / 2:   {type(502 / 2).__name__}")


# -------------------------------------------------------------- two divisions
print("\n--- The two divisions ---")
total_pages = sum(pages)
print(f"{total_pages} pages over 6 books")
print(f"true division  {total_pages} / 6 = {total_pages / 6}")
# `//` is floor division: divide and throw away the fractional part.
print(f"floor division {total_pages} // 6 = {total_pages // 6}")
# `%` (modulo) is the leftover from that division. // and % come as a pair.
print(f"remainder      {total_pages} % 6 = {total_pages % 6}")
print(f"check: 6 * {total_pages // 6} + {total_pages % 6} = {6 * (total_pages // 6) + total_pages % 6}")

# // and % together are how you convert one unit into another.
print("\n--- If I read 30 pages a day ---")
days = total_pages // 30
leftover = total_pages % 30
print(f"{total_pages} pages = {days} full days plus {leftover} pages")
print(f"which is {days // 7} weeks and {days % 7} days")


# ------------------------------------------------------------------- averages
print("\n--- Averages ---")
average_pages = sum(pages) / len(pages)
print(f"average book: {average_pages} pages")
# round(x, 1) means "one digit after the decimal point".
print(f"rounded:      {round(average_pages, 1)} pages")
# int() is NOT rounding - it chops. int(416.6) is 416, not 417.
print(f"round(416.6) = {round(416.6)}   but   int(416.6) = {int(416.6)}")


# --------------------------------------------------------- order of operations
print("\n--- Order of operations ---")
# Multiplication and division happen before addition and subtraction, same as
# in school. Parentheses override that. These two lines are NOT the same.
print(f"2 + 3 * 10   = {2 + 3 * 10}")
print(f"(2 + 3) * 10 = {(2 + 3) * 10}")
print(f"powers use **:  2 ** 10 = {2 ** 10}")


# ------------------------------------------------------- the money problem (!)
print("\n--- Money, and the thing nobody warns you about ---")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"Is 0.1 + 0.2 equal to 0.3?  {0.1 + 0.2 == 0.3}")

# That is not a bug in Python. Computers store decimals in binary, and 0.1
# in binary is a repeating fraction - like 1/3 is 0.3333... in decimal. It
# gets stored as *almost* 0.1, and the error shows up when you add.
spent = sum(prices)
print(f"\nI spent {spent} on books")
print(f"printed nicely: ${spent:.2f}")

# Worse: the SAME numbers added in a different ORDER give a different total.
# In real arithmetic, order never matters. In float arithmetic, it does.
backwards = sum(reversed(prices))
print(f"the same prices, added back to front: {backwards}")
print(f"are the two totals identical? {spent == backwards}")

# The professional fix for money: count whole CENTS as integers, and only
# turn them into dollars when you print. Integers are exact; floats are not.
cents = [1899, 1600, 1349, 1700, 2000, 1599]
total_cents = sum(cents)
print(f"in cents (exact): {total_cents} = ${total_cents / 100:.2f}")


# ------------------------------------------------------- dividing by zero
print("\n--- Dividing by zero ---")
books_read_today = 0
try:
    print(total_pages / books_read_today)
except ZeroDivisionError as error:
    # This is what a crash looks like when you catch it instead of letting it
    # stop the program. The name of the error IS the explanation.
    print(f"Python refused: {type(error).__name__}: {error}")


# ==============================================================================
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# 1. Two kinds of number. Whole numbers (int) are exact and unlimited in size.
#    Decimals (float) are approximate. `/` always gives you a float.
# 2. // and % are a pair: how many whole times it goes in, and what's left.
#    Every "convert seconds to minutes and seconds" problem is these two.
# 3. Never compare two floats with ==. Ask whether they're close enough.
# 4. Never store money as a float. Store cents as an int.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Print 0.1 + 0.2 with :.2f formatting. The wrongness hides. Where else
#   might it be hiding in a program you didn't write?
# - Delete the try/except and run it. Read the whole traceback bottom-up:
#   the LAST line says what went wrong, the lines above say where.
# - Change round(average_pages, 1) to round(average_pages, 3).
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Why is 0.1 + 0.2 == 0.30000000000000004? Explain it to someone who has
#    never heard of binary."
# - "Rewrite the money part of this program using the decimal module, and
#    tell me when that's the better choice than counting cents."
# - Careful: an AI will happily write `if total == 19.99:` for you. Now you
#   know to push back.
# ==============================================================================
