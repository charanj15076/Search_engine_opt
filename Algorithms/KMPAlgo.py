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
    n = len(text)
    results = {}
    for pattern in patterns:
        m = len(pattern)
        pi = compute_prefix_function(pattern)
        i = 0 #index for text
        j = 0  # index for pattern

        while i < n :
            if pattern[j] == text[i]:
                i+=1
                j+=1
            if j == m:
                if pattern in results:
                    results[pattern].append(i-j)
                else:
                    results[pattern] = [i-j]
                j = pi[j-1]
            elif i<n and pattern[j] != text[i]:
                if j!=0:
                    j = pi[j-1]
                else:
                    i+=1
    return results

#example run for kmp multiple patterns

# text = "ABABDABACDABABCABAB"
# patterns = ["AB", "ABAB", "CD", "ABC"]
#
# results = kmp_search(text, patterns)
# for pattern, indices in results.items():
#     print("pattern and no of times",pattern,len(indices))
#     # print(f"Pattern '{pattern}' found at indices: {', '.join(map(str, indices))}")
