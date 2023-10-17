from stop_words_func import stop_words_punc_filter
from Algorithms import KMPAlgo
import nltk
from nltk.tokenize import word_tokenize


stop_words = []

with open('stop_words.txt', "r") as f:
    stop_words = f.read().split()

text = ("As I walked through the bustling city streets,"
        " I couldn't help but notice the endless stream of people."
        " People of all ages, backgrounds, "
        "and walks of life were going about their daily routines. "
        "The city's vibrant energy, energy that drew people from all over the world, "
        "was palpable. I watched as people rushed past, past the towering skyscrapers "
        "that defined the city's skyline. The city's skyline was a testament to its growth, "
        "growth that seemed unstoppable. Unstoppable, it was a place where dreams could come"
        " true, where you could make your dreams come true with hard work and determination.")

word_tokens = word_tokenize(text)

tags_to_exclude = ['DT', 'IN','CC','EX','LS','MD','POS','PRP','PRP$','SYM']
filtered_words = stop_words_punc_filter(word_tokens,stop_words)
pos_tags = nltk.pos_tag(filtered_words)
# print(pos_tags)
filtered_meaningful_words = [word for word, pos in pos_tags if pos not in tags_to_exclude]
print(filtered_meaningful_words)
# print("herhe")
results = KMPAlgo.kmp_search(text,filtered_meaningful_words)
# print("herehee",results)
sorted_dict = dict(sorted(results.items(), key=lambda item: len(item[1])))
for pattern, indices in sorted_dict.items():
    print("pattern and no of times",pattern,len(indices))
    # print(f"Pattern '{pattern}' found at indices: {', '.join(map(str, indices))}")

