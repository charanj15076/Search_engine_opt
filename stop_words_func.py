import nltk
def stop_words_punc_filter(tokens, stop_words):
    filtered_words = []
    tags_to_exclude = ['DT', 'IN', 'CC', 'EX', 'LS', 'MD', 'POS', 'PRP', 'PRP$', 'SYM', 'RB']
    for w in tokens:
        if w.lower() not in stop_words:
            filtered_words.append(w.lower())

    pos_tags = nltk.pos_tag(filtered_words)
    filtered_meaningful_words = [word for word, pos in pos_tags if pos not in tags_to_exclude]
    return filtered_meaningful_words

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