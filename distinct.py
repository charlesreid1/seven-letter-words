"""
distinct.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Exercise #27

How many SGB words contain exactly k distinct letters, for 1 <= k <= 5?
"""
from get_words import get_words

if __name__=="__main__":
    words = get_words()

    wrd = words[0]
    n = len(wrd)

    lengths = [[] for i in range(n+1)]

    for word in words:
        k = len(set(word))
        lengths[k].append(word)

    for i in range(1,n+1):
        print("-"*40)
        print("Number of words with {0:d} letters: {1:d}".format(i, len(lengths[i])))
        print(", ".join(lengths[i][0:n]))

