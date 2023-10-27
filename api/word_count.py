import nltk
from nltk.tokenize import word_tokenize

import time
import pandas as pd

from algorithms import KMPAlgo, NaiveStringMatching, SuffixArray, SuffixTree, RabinKarpAlgo


def stop_words_punc_filter(tokens, stop_words):
    filtered_words = []
    tags_to_exclude = ['DT', 'IN', 'CC', 'EX', 'LS', 'MD', 'POS', 'PRP', 'PRP$', 'SYM', 'RB', 'VBP']
    
    for w in tokens:
        if w.lower() not in stop_words:
            filtered_words.append(w.lower())

    pos_tags = nltk.pos_tag(filtered_words)
    filtered_meaningful_words = [word for word, pos in pos_tags if pos not in tags_to_exclude]

    return filtered_meaningful_words


def get_word_counts(text):
    stop_words = []
    with open('api/lib/stop_words.txt', "r") as f:
        stop_words = f.read().split()

    stop_words += [str(i) for i in range(10)] + list("abcdefghijklmnopqrstuvwxyz") + [x + y for x in "abcdefghijklmnopqrstuvwxyz" for y in "abcdefghijklmnopqrstuvwxyz"]

    # Clean the data (tokenize and remove stop words)
    word_tokens = word_tokenize(text)
    filtered_words = stop_words_punc_filter(word_tokens, stop_words)


    ##### Perform word count analysis using the different text search algorithms #####
    ##### We will be measure the time taken for the performance analysis as well #####
    # KMP
    start_time = time.time_ns()
    results_kmp = KMPAlgo.kmp_search(text, filtered_words)
    end_time = time.time_ns()
    t_kmp = end_time - start_time
    
    # Naive
    start_time = time.time_ns()
    results_naive = NaiveStringMatching.multiple_pattern_match(text, filtered_words)
    end_time = time.time_ns()
    t_naive = end_time - start_time

    # Suffix Array
    # construct suffix array first
    start_time = time.time_ns()
    suffix_array = SuffixArray.construct_suffix_array(text) 
    results_suffix_array = SuffixArray.search_suffix_array(text, filtered_words, suffix_array)
    end_time = time.time_ns()
    t_suff_arr = end_time - start_time

    # Suffix Tree
    start_time = time.time_ns()
    try:
        results_suffix_tree = SuffixTree.multiple_patterns(text, filtered_words)
    except:
        results_suffix_tree = {}
    end_time = time.time_ns()
    t_suff_tree = end_time - start_time

    # Rabin-Karp
    start_time = time.time_ns()
    try:
        results_rabinkarp = RabinKarpAlgo.multiple_patterns(text, filtered_words)
    except:
        results_rabinkarp = {}  
    end_time = time.time_ns()
    t_rk = end_time - start_time
    ##################################################################################


    # Sort the word counts
    sorted_dict_kmp = dict(sorted(results_kmp.items(), key=lambda item: len(item[1])))
    sorted_dict_naive = dict(sorted(results_naive.items(), key=lambda item: len(item[1])))
    sorted_dict_suffix_array = dict(sorted(results_suffix_array.items(), key=lambda item: len(item[1])))
    sorted_dict_suffix_tree = dict(sorted(results_suffix_tree.items(), key=lambda item: len(item[1])))
    sorted_dict_rabin = dict(sorted(results_rabinkarp.items(), key=lambda item: len(item[1])))

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

    data = {
        'kmp' : df_kmp,
        'naive': df_naive,
        'suffix_array': df_suffix_array,
        'suffix_tree': df_suffix_tree,
        'rabin_karp': df_rabin_karp,
    }

    times = {
        'kmp' : t_kmp,
        'naive': t_naive,
        'suffix_array': t_suff_arr,
        'suffix_tree': t_suff_tree,
        'rabin_karp': t_rk,
    }

    return data, times
