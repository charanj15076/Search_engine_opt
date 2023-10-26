######################################################
# SuffixTreeIdx is a modification of SuffixTree.
# Instead of returning the suffix when seeing the
# pattern, it will return the index of the occurrence
# of the pattern instead.
######################################################

class TrieNode:
    def __init__(self, idx):
        self.children = {}
        self.is_end_of_word = False
        self.idx = idx


class Trie:
    def __init__(self):
        self.root = TrieNode(0)

    def insert(self, word, idx):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(idx)
            node = node.children[char]
        node.is_end_of_word = True


class SuffixTreeIdx:
    def __init__(self, text):
        self.text = text
        self.trie = Trie()
        self.build()

    def build(self):
        for i in range(len(self.text)):
            self.trie.insert(self.text[i:], i)

    def display(self, node=None, prefix=''):
        node = node or self.trie.root
        if not node.children:
            print(prefix)
        else:
            for char, child in node.children.items():
                self.display(child, prefix + char)

    def search(self, pattern):
        node = self.trie.root
        for char in pattern:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        return self.find_occurrences(node, pattern)

    def find_occurrences(self, node, pattern, prefix=''):
        occurrences = []
        if node.is_end_of_word:
            occurrences.append(node.idx)
        for char, child in node.children.items():
            occurrences += self.find_occurrences(child, pattern, prefix + char)
        return occurrences

def multiple_patterns(text,patterns):
    text = text.lower()
    suffix_tree = SuffixTreeIdx(text)
    result= {pattern: set() for pattern in patterns}
    for pattern in patterns:
        occurances = suffix_tree.search(pattern)
        if occurances:
            result[pattern].update(occurances)
        else:
            result[pattern].add(0)
    return result


