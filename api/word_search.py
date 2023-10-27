import time

from algorithms import KMPAlgo, NaiveStringMatching, SuffixArray, SuffixTreeIdx, RabinKarpAlgo


# This function returns the substrings given the locations of a term in a text
def get_substrings(result_set, text, term):
	pre_len = 30
	post_len = 30
	text_len = len(text)
	term_len = len(term)

	substr_list = []
	for key, idx_list in result_set.items():
		for idx in sorted(idx_list):
			idx = int(idx)
			start_idx = max(0, idx - pre_len)
			pre_ellipsis = "" if (start_idx == 0) else "..."
			
			end_idx = min(text_len, idx + term_len + post_len)
			post_ellipsis = "" if (end_idx == text_len) else "..."

			substr_list.append(pre_ellipsis + text[start_idx:end_idx] + post_ellipsis)

	return substr_list


# This function gets all the occurrences of a term using the different algorithms provided
def get_occurrences(text, term):
	
	# Use the different algorithms for the search. They should all yield the same result.
	# We will be measuring the time taken for each search as well.
	# KMP
	start_time = time.time_ns()
	results_kmp = KMPAlgo.kmp_search(text, [term])
	end_time = time.time_ns()
	t_kmp = end_time - start_time

	# Naive
	start_time = time.time_ns()
	results_naive = NaiveStringMatching.multiple_pattern_match(text, [term])
	end_time = time.time_ns()
	t_naive = end_time - start_time

	# Suffix Array
	# construct suffix array first
	start_time = time.time_ns()
	suffix_array = SuffixArray.construct_suffix_array(text) 
	results_suff_arr = SuffixArray.search_suffix_array(text, [term], suffix_array)
	end_time = time.time_ns()
	t_suff_arr = end_time - start_time

	# Suffix Tree
	start_time = time.time_ns()
	try:
		results_suff_tree = SuffixTree.multiple_patterns(text, [term])
	except:
		results_suff_tree = {}
	end_time = time.time_ns()
	t_suff_tree = end_time - start_time

	# Rabin-Karp
	start_time = time.time_ns()
	try:
		results_rk = RabinKarpAlgo.multiple_patterns(text, [term])
	except:
		results_rk = {}  
	
	end_time = time.time_ns()
	t_rk = end_time - start_time


	# Get the substrings for display purposes
	substrs_kmp = get_substrings(results_kmp, text, term)
	substrs_naive = get_substrings(results_naive, text, term)
	substrs_suff_arr = get_substrings(results_suff_arr, text, term)
	substrs_suff_tree = get_substrings(results_suff_tree, text, term)
	substrs_rk = get_substrings(results_rk, text, term)
	
	data = {
		'kmp' : substrs_kmp,
		'naive': substrs_naive,
		'suffix_array': substrs_suff_arr,
		'suffix_tree': substrs_suff_tree,
		'rabin_karp': substrs_rk,
	}

	times = {
		'kmp' : t_kmp,
		'naive': t_naive,
		'suffix_array': t_suff_arr,
		'suffix_tree': t_suff_tree,
		'rabin_karp': t_rk,
	}

	return data, times
