def compute_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text, patterns):
    text = text.lower()
    n = len(text)
    results = {pattern: set() for pattern in patterns}

    for pattern in patterns:
        m = len(pattern)
        pi = compute_prefix_function(pattern)
        j = 0  # Number of characters matched

        for i in range(n):
            while j > 0 and text[i] != pattern[j]:
                j = pi[j - 1]  # Fall back in the pattern
            if text[i] == pattern[j]:
                j += 1  # Match the next character
            if j == m:  # A complete match is found
                results[pattern].add(i - m + 1)
                j = pi[j - 1]  # Prepare for the next possible match

    return results

#example run for kmp multiple patterns

# text = "ABABDABACDABABCABAB"
# patterns = ["AB", "ABAB", "CD", "ABC"]
#
# results = kmp_search(text, patterns)
# for pattern, indices in results.items():
#     print("pattern and no of times",pattern,len(indices))
#     # print(f"Pattern '{pattern}' found at indices: {', '.join(map(str, indices))}")
