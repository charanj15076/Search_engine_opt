def naive_string_matching(text, pattern):
    n = len(text)
    m = len(pattern)
    occurrences = []  # List to store the starting indices of matches

    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            occurrences.append(i)

    return occurrences

def multiple_pattern_match(text, patterns):
    """
    Search for multiple patterns in a text using the naive string matching algorithm.
    """
    results = {}

    for pattern in patterns:
        occurrences = naive_string_matching(text, pattern)
        if occurrences:
            results[pattern] = occurrences

    return results



# Get user input
# text = "ABABDABACDABABCABAB"
# patterns = ["AB", "ABAB", "CD", "ABC"]
#
# results = multiple_pattern_match(text, patterns)
# for pattern, indices in results.items():
#     print("pattern and no of times",pattern,len(indices))
#     # print(f"Pattern '{pattern}' found at indices: {', '.join(map(str, indices))}")
