"""
near_palindromes.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Variation on Exercise #29

Find SGB words that are near-palindromes
(edit distance of one or two letters away from a palindrome).
"""
from get_words import get_words
from euclidean_distance import euclidean_distance
from pprint import pprint


def is_near_palindrome(word,lo,hi):
    n = len(word)
    hn = n//2

    ds = []
    for ih in range(hn):
        d = euclidean_distance(word[ih], word[n-ih-1])
        ds.append(d)

    if (sum(ds) > lo) and (sum(ds) <= hi):
        return True

    return False


if __name__=="__main__":
    words = get_words()

    knp = 0
    near_palindromes = []

    # Euclidean distance tolerance
    lo = 0.0
    hi = 1.0

    for i in range(len(words)):
        if(is_near_palindrome(words[i],lo,hi)):
            knp += 1
            near_palindromes.append(words[i])

    print("\n\n")
    print("-"*40)
    print("Near Palindromes: \n")
    print(", ".join(near_palindromes))
    print("The number of near-palindromes is {0:d}".format(len(near_palindromes)))

    # Off by 2
    ob1or2_palindromes = []
    hi = 2.0

    for i in range(len(words)):
        if(is_near_palindrome(words[i],lo,hi)):
            knp += 1
            ob1or2_palindromes.append(words[i])

    ob2_palindromes = list(set(ob1or2_palindromes)-set(near_palindromes))

    print("\n\n")
    print("-"*40)
    print("Off-By-Two Palindromes: \n")
    print(", ".join(ob2_palindromes))
    print("The number of off-by-two palindromes is {0:d}".format(len(ob2_palindromes)))


    print("\n\n")

