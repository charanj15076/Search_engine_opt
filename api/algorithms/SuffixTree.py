from timeout import timeout

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.trie = Trie()
        self.build()

    def build(self):
        for i in range(len(self.text)):
            self.trie.insert(self.text[i:])

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
            occurrences.append(prefix)
        for char, child in node.children.items():
            occurrences += self.find_occurrences(child, pattern, prefix + char)
        return occurrences

@timeout(10)
def multiple_patterns(text,patterns):
    text = text.lower()
    suffix_tree = SuffixTree(text)
    result= {pattern: set() for pattern in patterns}
    for pattern in patterns:
        occurances = suffix_tree.search(pattern)
        if occurances:
            result[pattern].update(occurances)
        else:
            result[pattern].add(0)
    return result



# Example of usage for multiple pattern matching:
# text = "ABABDABACDABABCABAB"
# patterns = ["AB", "ABAB", "CD", "ABC"]
#
# results = multiple_patterns(text,patterns)
# for pattern, occurrences in results.items():
#     if occurrences:
#         print(f"Pattern '{pattern}' found at indices: {occurrences}")
#     else:
#         print(f"Pattern '{pattern}' not found in the text.")
