def construct_suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort(key=lambda x: x[0])
    suffix_array = [item[1] for item in suffixes]
    return suffix_array

# Get user input
# text = input("Enter the text: ")
#
# # Construct and print suffix array
# suffix_array = construct_suffix_array(text)
# print("Suffix Array:", suffix_array)
