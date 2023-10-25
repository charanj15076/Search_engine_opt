import nltk
from nltk.tokenize import word_tokenize

import pandas as pd

from algorithms import KMPAlgo, NaiveStringMatching, SuffixArray, SuffixTree, RabinKarpAlgo


def stop_words_punc_filter(tokens, stop_words):
    filtered_words = []
    tags_to_exclude = ['DT', 'IN', 'CC', 'EX', 'LS', 'MD', 'POS', 'PRP', 'PRP$', 'SYM', 'RB']
    
    for w in tokens:
        if w.lower() not in stop_words:
            filtered_words.append(w.lower())

    pos_tags = nltk.pos_tag(filtered_words)
    filtered_meaningful_words = [word for word, pos in pos_tags if pos not in tags_to_exclude]

    return filtered_meaningful_words


def get_word_counts(text):
    stop_words = []

    with open('lib/stop_words.txt', "r") as f:
        stop_words = f.read().split()

    # text = ("As I walked through the bustling city streets,"
    #         " I couldn't help but notice the endless stream of people."
    #         " People of all ages, backgrounds, "
    #         "and walks of life were going about their daily routines. "
    #         "The city's vibrant energy, energy that drew people from all over the world, "
    #         "was palpable. I watched as people rushed past, past the towering skyscrapers "
    #         "that defined the city's skyline. The city's skyline was a testament to its growth, "
    #         "growth that seemed unstoppable. Unstoppable, it was a place where dreams could come"
    #         " true, where you could make your dreams come true with hard work and determination.")

    word_tokens = word_tokenize(text)
    filtered_words = stop_words_punc_filter(word_tokens,stop_words)


    # Perform word count analysis using the different text search algorithms
    results_kmp = KMPAlgo.kmp_search(text,filtered_words)
    # print(results_kmp)
    
    results_naive = NaiveStringMatching.multiple_pattern_match(text,filtered_words)
    # print(results_naive)

    # construct suffix array first
    suffix_array = SuffixArray.construct_suffix_array(text) 
    results_suffix_array = SuffixArray.search_suffix_array(text,filtered_words,suffix_array)

    results_suffix_tree = SuffixTree.multiple_patterns(text,filtered_words)

    results_rabinkarp = RabinKarpAlgo.multiple_patterns(text,filtered_words)

    # Sort the word counts
    sorted_dict_kmp = dict(sorted(results_kmp.items(), key=lambda item: len(item[1])))
    sorted_dict_naive = dict(sorted(results_naive.items(), key=lambda item: len(item[1])))
    sorted_dict_suffix_array = dict(sorted(results_suffix_array.items(), key=lambda item: len(item[1])))
    sorted_dict_suffix_tree = dict(sorted(results_suffix_tree.items(), key=lambda item: len(item[1])))
    sorted_dict_rabin = dict(sorted(results_rabinkarp.items(), key=lambda item: len(item[1])))


    # print("KMP Matching---------------")
    # for pattern, indices in sorted_dict_kmp.items():
    #     print(pattern,":",len(indices))
    #     # print(f"Pattern '{pattern}' found at indices: {', '.join(map(str, indices))}")
    #
    #
    # print("Naive Matching--------------------")
    # for pattern2, indices2 in sorted_dict_naive.items():
    #     print(pattern2,":",len(indices2))
    #
    #
    # print("suffix array matching--------------------")
    # for pattern3, indices3 in sorted_dict_suffix_array.items():
    #     print(pattern3,":",len(indices3))


    # Build the frequency lists
    word_counts_kmp = [{'Word': word, 'count': len(values)} for word, values in sorted_dict_kmp.items()]
    word_counts_naive = [{'Word': word, 'count': len(values)} for word, values in sorted_dict_naive.items()]
    word_counts_suffix_array = [{'Word': word, 'count': len(values)} for word, values in sorted_dict_suffix_array.items()]
    word_counts_suffix_tree = [{'Word': word, 'count': len(values)} for word, values in sorted_dict_suffix_tree.items()]
    word_counts_rabin = [{'Word': word, 'count': len(values)} for word, values in sorted_dict_rabin.items()]

    # Convert the list of dictionaries into a DataFrame
    df_kmp = pd.DataFrame(word_counts_kmp)
    df_naive = pd.DataFrame(word_counts_naive)
    df_suffix_array = pd.DataFrame(word_counts_suffix_array)
    df_suffix_tree = pd.DataFrame(word_counts_suffix_tree)
    df_rabin_karp = pd.DataFrame(word_counts_rabin)

    print(df_suffix_array)
    print(df_naive)
    print(df_kmp)
    print(df_suffix_tree)
    print(df_rabin_karp)

    return df_kmp, df_naive, df_suffix_array, df_suffix_tree, df_rabin_karp
