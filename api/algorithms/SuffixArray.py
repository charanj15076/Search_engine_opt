def construct_suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort(key=lambda x: x[0])
    suffix_array = [item[1] for item in suffixes]
    return suffix_array

def search_suffix_array(text, patterns, suffix_array):
    results = {pattern: set() for pattern in patterns}
    text_length = len(text)

    for pattern in patterns:
        low, high = 0, text_length - 1
        pattern_length = len(pattern)

        while low <= high:
            mid = (low + high) // 2
            suffix = text[suffix_array[mid]:suffix_array[mid] + pattern_length]

            if pattern == suffix:
                results[pattern].add(suffix_array[mid])
                # Search for other occurrences
                for i in range(mid + 1, len(suffix_array)):
                    next_suffix = text[suffix_array[i]:suffix_array[i] + pattern_length]
                    if next_suffix == pattern:
                        results[pattern].add(suffix_array[i])
                    else:
                        break
                for i in range(mid - 1, -1, -1):
                    prev_suffix = text[suffix_array[i]:suffix_array[i] + pattern_length]
                    if prev_suffix == pattern:
                        results[pattern].add(suffix_array[i])
                    else:
                        break
                break
            elif pattern < suffix:
                high = mid - 1
            else:
                low = mid + 1

    return results

# Example usage
# text = "banana"
# patterns = ["ana", "na"]
# suffix_array = construct_suffix_array(text)
#
# results = search_suffix_array(text, patterns, suffix_array)
# for pattern, occurrences in results.items():
#     if occurrences:
#         print(f"Pattern '{pattern}' found at indices: {occurrences}")
#     else:
#         print(f"Pattern '{pattern}' not found in the text.")
