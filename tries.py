#!/usr/bin/env python
from get_words import get_words
import sys
import math

"""
tries.py

Donald Knuth, Art of Computer Programming, Volume 4 Fascicle 0
Exercise #35

Problem:
What letters of the alphabet can be used
as the starting letter of sixty-four words that
form a complete binary trie within
WORDS(n), given n?
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class Node(object):
    def __init__(self, letter, count=0):
        self.letter = letter
        self.count = count
        self.children = []
        self.parent = None


class TryTrieTree(object):
    def __init__(self, words):
        self.root = None
        self.words = words
        self.target_depth = 6

    def set_root(self, root_letter):
        self.root = Node(root_letter)

    def get_prefix_from_node(self, node):
        if node == None or node == self.root:
            return ""
        prefix = ""
        while node.parent != None:
            node = node.parent
            prefix = node.letter + prefix
        return prefix

    def get_node_from_prefix(self, prefix):
        assert self.root != None
        if prefix == '':
            return None
        assert prefix[0] == self.root.letter
        if len(prefix) == 1:
            return self.root

        parent_prefix, suffix = prefix[:len(prefix)-1], prefix[len(prefix)-1]
        parent = self.get_node_from_prefix(parent_prefix)
        for child in parent.children:
            if child.letter == suffix:
                return child
        raise ValueError("Prefix '{}' not found in trie".format(prefix))

    def assemble(self, target_depth):
        assert self.root != None
        self.target_depth = target_depth
        prefix = ''
        candidate = self.root.letter
        self._assemble(prefix, candidate, self.words)

    def _assemble(self, prefix, candidate, words):
        prefix_depth = len(prefix)
        candidate_depth = prefix_depth + 1

        ppc = prefix + candidate
        words_with_candidate = [w for w in words if w[:candidate_depth] == ppc]

        min_branches_req = int(math.pow(2, self.target_depth - (candidate_depth - 1)))
        max_number_branches = len(words_with_candidate)

        if max_number_branches >= min_branches_req:
            parent = self.get_node_from_prefix(prefix)
            if prefix == '':
                new_child = self.root
            else:
                new_child = Node(candidate)
                new_child.parent = parent
                parent.children.append(new_child)

            if candidate_depth == self.target_depth:
                new_child.count = max_number_branches
                return

            for new_candidate in ALPHABET:
                new_prefix = prefix + candidate
                self._assemble(new_prefix, new_candidate, words_with_candidate)

    def bubble_up(self):
        self._bubble_up(self.root)

    def _bubble_up(self, node):
        if len(node.children) == 0:
            return
        for child in node.children:
            self._bubble_up(child)
        large_children = [child for child in node.children if child.count >= 2]
        node.count = len(large_children)

    def __str__(self):
        def _str_recursive(node, depth):
            s = "  " * depth + f"{node.letter}: {node.count}\n"
            for child in node.children:
                if child.count >= 2 or (not child.children and child.count >= 2):
                    s += _str_recursive(child, depth + 1)
            return s
        return _str_recursive(self.root, 0)


def find_max_depth(letter, words, max_possible=6):
    best_tree = None
    for depth in range(max_possible, 0, -1):
        tree = TryTrieTree(words)
        tree.set_root(letter)
        tree.assemble(depth)
        tree.bubble_up()
        if tree.root.count >= 2:
            return depth, tree
    return 0, None


def trie_search(n):
    words = get_words()
    words = words[:n]

    print(f"Searching for the deepest perfect binary trie for each letter in WORDS({n}):")
    print(f"{'Letter':<10} {'Max Depth':<10} {'Words Required':<15}")
    print("-" * 40)

    results = []
    best_overall_depth = 0
    best_overall_letter = None
    best_overall_tree = None

    for letter in ALPHABET:
        depth, tree = find_max_depth(letter, words)
        words_req = int(math.pow(2, depth))
        print(f"{letter:<10} {depth:<10} {words_req:<15}")
        results.append((letter, depth))
        if depth > best_overall_depth:
            best_overall_depth = depth
            best_overall_letter = letter
            best_overall_tree = tree

    if best_overall_tree:
        print(f"\nExample perfect binary trie for '{best_overall_letter}' (Depth {best_overall_depth}):")
        print(best_overall_tree)

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        n = 10000
    else:
        n = int(sys.argv[1])
        if n > 10000:
            n = 10000

    trie_search(n)
