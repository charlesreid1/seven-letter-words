"""
letter_coverage.py

Compute the minimum number of words from seven-letter-words
needed to cover the first N letters of the alphabet, and count
how many word sets of that size cover them.

The word list is alphabetical, so it is shuffled with a seeded RNG
(SEED, or the first command line argument) before anything else.
WORDS(1000) is the first 1000 shuffled words, and the search visits
words in shuffled order, so the cover it reports is not biased
toward the start of the alphabet.

This is a set cover problem: the universe is the N letters, each word
is a subset of at most seven of them. Set cover is NP-hard in general,
but the universe here has at most 26 elements, so an exact branch and
bound search is fast. Branch on the uncovered letter that appears in
the fewest words, and prune when the words chosen so far plus
ceil(uncovered / k) cannot beat the best cover found, where k is the
largest number of letters any one word covers.

The count of minimum covers uses inclusion-exclusion over the subsets
S of the coverable letters. If f(S) is the number of words whose
letters among the first N all lie in S, the number of m-word sets
covering every coverable letter is the sum over S of
(-1)^(number of coverable letters not in S) * C(f(S), m).

https://charlesreid1.com/wiki/Five_Letter_Words
https://charlesreid1.com/wiki/Letter_Coverage
"""
import random
import sys
from math import comb

import numpy as np

from get_words import get_words

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0


def word2bitvector(word, N):
    """
    Turn a word into an integer bit vector representing letter coverage
    of the first N letters of the alphabet. Letters past the Nth are
    ignored.
    """
    bv = 0
    for c in word:
        i = ord(c) - ord('a')
        if i < N:
            bv |= 1 << i
    return bv


def popcount(bv):
    return bin(bv).count("1")


def min_cover(words, N):
    """
    Return (covered, solution): the set of letters among the first N
    that any word covers, and a shortest list of words covering all of
    them. Ties go to the first cover found in the order of words.
    """
    # One representative word per distinct coverage pattern.
    by_pattern = {}
    for w in words:
        bv = word2bitvector(w, N)
        if bv and bv not in by_pattern:
            by_pattern[bv] = w
    patterns = list(by_pattern.items())

    # Largest number of letters one word covers, for the lower bound.
    k = max(popcount(bv) for bv, w in patterns)

    # Words containing each letter, and the letters that can be covered at all.
    by_letter = [[(bv, w) for bv, w in patterns if bv >> i & 1] for i in range(N)]
    target = 0
    for i in range(N):
        if by_letter[i]:
            target |= 1 << i

    best = [len(patterns) + 1, None]

    def search(covered, chosen):
        if covered & target == target:
            if len(chosen) < best[0]:
                best[0] = len(chosen)
                best[1] = list(chosen)
            return

        remaining = popcount(target & ~covered)
        if len(chosen) + (remaining + k - 1) // k >= best[0]:
            return

        # Most constrained uncovered letter: fewest words contain it.
        uncovered = [i for i in range(N) if target >> i & 1 and not covered >> i & 1]
        i = min(uncovered, key=lambda i: len(by_letter[i]))

        for bv, w in by_letter[i]:
            chosen.append(w)
            search(covered | bv, chosen)
            chosen.pop()

    search(0, [])
    return target, best[1]


def count_covers(words, N, m):
    """
    Return the number of m-word sets that cover every letter among the
    first N that any word covers, by inclusion-exclusion (see the
    module docstring).
    """
    # Number the coverable letters 0..n-1.
    target = 0
    for w in words:
        target |= word2bitvector(w, N)
    letters = [i for i in range(N) if target >> i & 1]
    n = len(letters)
    pats = [sum(1 << j for j, i in enumerate(letters) if bv >> i & 1)
            for bv in (word2bitvector(w, N) for w in words)]

    # f[S] = number of words whose pattern lies in S (subset-sum transform).
    f = np.bincount(pats, minlength=1 << n).astype(np.uint32)
    for j in range(n):
        v = f.reshape(-1, 2, 1 << j)
        v[:, 1, :] += v[:, 0, :]

    # c[S] = C(f[S], m) = f(f-1)...(f-m+1) / m!, exact in uint64 while
    # C(W, m-1) * W fits. Once f - r + 1 hits 0, c stays 0 even after f wraps.
    assert comb(len(words), m - 1) * len(words) < 2**64
    c = np.ones(1 << n, dtype=np.uint64)
    for r in range(1, m + 1):
        c *= f
        c //= r
        f -= 1
    del f

    # Alternating sum: fold out one letter at a time, c[S] = c[S+x] - c[S].
    # uint64 arithmetic wraps mod 2^64, and the true count is below 2^64.
    for _ in range(n):
        half = len(c) // 2
        c = c[half:] - c[:half]
    return int(c[0])


def report(words, N, label):
    covered, solution = min_cover(words, N)
    count = count_covers(words, N, len(solution))
    letters = ", ".join(chr(ord('a') + i) for i in range(N) if covered >> i & 1)
    print("Takes {0:d} words to cover {1:d} letters ({2:s}) from {3:s}".format(
        len(solution), popcount(covered), letters, label))
    print(solution)
    print("{0:d} sets of {1:d} words cover these letters".format(count, len(solution)))
    print("")


if __name__ == "__main__":

    words = get_words()
    random.Random(SEED).shuffle(words)
    print("Word list shuffled with seed {0:d}; WORDS(1000) is the first 1000 shuffled words".format(SEED))
    print("")

    # Searching for words covering first N letters
    N = 15

    report(words[:1000], N, "WORDS(1000)")

    # The whole alphabet
    report(words[:1000], 26, "WORDS(1000)")
    report(words, 26, "WORDS({0:d})".format(len(words)))

    # Minimum cover for each N, from WORDS(1000)
    print("{0:>3s}  {1:>5s}  {2:>6s}  {3:s}".format("N", "words", "covers", "one cover"))
    for N in range(5, 27):
        covered, solution = min_cover(words[:1000], N)
        count = count_covers(words[:1000], N, len(solution))
        print("{0:3d}  {1:5d}  {2:6d}  {3:s}".format(N, len(solution), count, " ".join(solution)))
