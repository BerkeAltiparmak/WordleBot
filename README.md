# WordleBot

A Wordle Bot that finds the most optimal words to try next by following these steps:

(Before game)
1) Looks at the dictionary of the words
2) Chooses only those that are valid in the context of the Wordle

(During game)
1) Considers the information we have on what the mystery word's letters can be
2) Chooses a couple of letters (<=5) to try to include in the next word to try
3) Chooses the next word to try by looking at the list of most common words that includes the chosen words.

The performance of this WordleBot: the average tries to find the mystery word is less than 4, and always solves the Wordle.

