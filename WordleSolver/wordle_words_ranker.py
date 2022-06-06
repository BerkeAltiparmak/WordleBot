import pandas as pd

df_wordle = pd.read_fwf('valid_wordle_words.txt', header=None)
"""df.columns = ['Wordle']"""
wordle_list = [v[0] for v in df_wordle.values]

df_all = pd.read_fwf('5letterwords_freqranked.txt', header=None)
ranked_list = [v[0] for v in df_all.values]

wordle_ranked = ['a'] * len(ranked_list)
trash_word_count = 0
for word in wordle_list:
    if word in ranked_list:
        idx = ranked_list.index(word)
        wordle_ranked[idx] = word
    else:
        trash_word_count += 1
        wordle_ranked[-trash_word_count] = word

with open('wordle_ranked.txt', 'w') as f:
    for word in wordle_ranked:
        if word != 'a':
            f.write(word)
            f.write('\n')
