from timeout_function_decorator import timeout

class RabinKarp:
    def __init__(self, text):
        self.text = text
        self.text_length = len(text)
        self.base = 256  # Assuming ASCII characters
        self.prime = 101  # A prime number for modulo operation
        self.patterns = []

    def calculate_hash_value(self, string, length):
        value = 0
        for i in range(length):
            value = (self.base * value + ord(string[i])) % self.prime
        return value

    def recalculate_hash_value(self, old_hash, old_char, new_char, pattern_length):
        new_hash = (self.base * (old_hash - ord(old_char) * (self.base ** (pattern_length - 1))) + ord(
            new_char)) % self.prime
        return new_hash

    def search_pattern(self, pattern):
        pattern_length = len(pattern)
        pattern_hash_value = self.calculate_hash_value(pattern, pattern_length)
        hash_value = self.calculate_hash_value(self.text[:pattern_length], pattern_length)

        occurrences = []

        for i in range(self.text_length - pattern_length + 1):
            if pattern_hash_value == hash_value:
                for j in range(pattern_length):
                    if self.text[i + j] != pattern[j]:
                        break
                else:
                    occurrences.append(i)

            if i < self.text_length - pattern_length:
                hash_value = self.recalculate_hash_value(hash_value, self.text[i], self.text[i + pattern_length],
                                                         pattern_length)

        return occurrences

@timeout(10)
def multiple_patterns(text,patterns):
    text = text.lower()
    rk_search = RabinKarp(text)
    result = {pattern: set() for pattern in patterns}
    for i, pattern in enumerate(patterns):
        occurrences = rk_search.search_pattern(pattern)
        result[pattern].update(occurrences)
    return result

# if __name__ == "__main__":
#
#     text = "ABABDABACDABABCABAB"
#     patterns = ["AB", "ABAB", "CD", "ABC"]
#     results = multiple_patterns(text,patterns)
#     for pattern, indices in results.items():
#         print("pattern and no of times",pattern,len(indices))
#         # print(f"Pattern '{pattern}' found at indices: {', '.join(map(str, indices))}")

