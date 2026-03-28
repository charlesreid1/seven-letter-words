"""
palindromes.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Exercise #29

Find all SGB words that are palindromes (kayak)
or that are palindrome pairs (regal lager)
"""
from get_words import get_words
import sys

def is_palindrome(word):
    """Returns True if the word is a palindrome."""
    return word == word[::-1]

def is_palindrome_pair(word1, word2):
    """Returns True if word1 is the reverse of word2."""
    return word1 == word2[::-1]

if __name__ == "__main__":
    words = get_words()
    
    if not words:
        print("No words found.")
        sys.exit(0)

    # All words are expected to have the same length N
    N = len(words[0])
    
    # Enforce N to be odd
    if N % 2 == 0:
        print(f"Error: Word length N={N} must be odd.")
        sys.exit(1)

    print(f"Processing {N}-letter words...")

    palindromes = []
    palindrome_pairs = []

    # Check for palindromes
    for word in words:
        if is_palindrome(word):
            palindromes.append(word)

    print("-" * 40)
    print("Palindromes: \n")
    print(", ".join(palindromes))
    print(f"There are {len(palindromes)} palindromes.")

    # Check for palindrome pairs
    # Using a set for faster lookup of reverse words
    word_set = set(words)
    seen_pairs = set()

    for word in words:
        reversed_word = word[::-1]
        if reversed_word != word and reversed_word in word_set:
            # To avoid adding (word1, word2) and (word2, word1), 
            # we sort the pair or use a canonical ordering.
            pair = tuple(sorted((word, reversed_word)))
            if pair not in seen_pairs:
                palindrome_pairs.append(pair)
                seen_pairs.add(pair)

    print("-" * 40)
    print("Palindrome Pairs: \n")
    for pair in palindrome_pairs:
        print(", ".join(pair))
    print(f"There are {len(palindrome_pairs)} palindrome pairs.")
