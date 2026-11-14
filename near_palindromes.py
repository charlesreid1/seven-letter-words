"""
near_palindromes.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Variation on Exercise #29

Find words that are near-palindromes: every mirror pair of letters
matches except one, which is a single alphabet step apart, so the word
is one alphabet step away from a palindrome.
"""
from get_words import get_words
def is_near_palindrome(word,lo,hi):
    n = len(word)
    d = sum(abs(ord(word[i]) - ord(word[n-1-i])) for i in range(n//2))
    return lo < d <= hi

if __name__=="__main__":
    words = get_words()

    # Euclidean distance tolerance
    lo = 0.0
    hi = 1.0

    near_palindromes = [w for w in words if is_near_palindrome(w, lo, hi)]

    print("-"*40)
    print("Near Palindromes: \n")
    print(", ".join(near_palindromes))
    print("The number of near-palindromes is {0:d}".format(len(near_palindromes)))

