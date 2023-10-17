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


# Get user input
# text = input("Enter the text: ")
#
# # Construct and display suffix tree
# suffix_tree = SuffixTree(text)
# suffix_tree.display()
