def stop_words_punc_filter(tokens, stop_words):
    filtered_words = []
    for w in tokens:
        if w.lower() not in stop_words:
            filtered_words.append(w.lower())
    return filtered_words

#example run

# stop_words = []
#
# with open('stop_words.txt', "r") as f:
#     stop_words = f.read().split()
#
# word_tokens = ['This',
#  'is',
#  'a',
#  'sample',
#  'sentence',
#  ',',
#  'showing',
#  'off',
#  'the',
#  'stop',
#  'words',
#  'filtration',
#  '.']
#
# filtered_words = stop_words_punc_filter(word_tokens,stop_words)
# print("filtered_words",filtered_words)