from typing import Optional

import pandas as pd
import math

try:
    df = pd.read_fwf('wordle_ranked.txt', header=None)
except FileNotFoundError:
    df = pd.DataFrame('a')
df.columns = ['Wordle']
greenless_df = df

turns = 0
green_letters = dict()
yellow_letters = dict()
grey_letters = dict()
g_already_filtered = []
y_already_filtered = []
n_already_filtered = []


def update_after_guess():
    global df, greenless_df
    for grey in grey_letters:
        if grey not in n_already_filtered and grey not in green_letters:
            df = df[df['Wordle'].str.contains(grey, na=False) == False]
            n_already_filtered.append(grey)
        elif grey in green_letters:
            df = df[df['Wordle'].str.find(grey, grey_letters[grey] - 1, green_letters[grey]) == -1]
        greenless_df = df
    for yellow in yellow_letters:
        if yellow not in y_already_filtered:
            df = df[df['Wordle'].str.contains(yellow, na=False)]
            df = df[df['Wordle'].str.find(yellow, yellow_letters[yellow] - 1, yellow_letters[yellow]) == -1]
            y_already_filtered.append(yellow)
        greenless_df = df
    for green in green_letters:
        if green in yellow_letters:
            yellow_letters.pop(green)
            y_already_filtered.remove(green)
        if green not in g_already_filtered:
            df = df[df['Wordle'].str.contains(green, na=False)]
            df = df[df['Wordle'].str.find(green, green_letters[green] - 1, green_letters[green]) != -1]
            g_already_filtered.append(green)
            greenless_df = greenless_df[greenless_df['Wordle'].str.find(green, green_letters[green] - 1,
                                                                        green_letters[green]) == -1]


def get_results_from_user(guess: str):
    result = input("What's the outcome?'")
    for i in range(1, 6):
        if result[i] == 'g':
            green_letters[guess[i-1]] = i
        elif result[i] == 'y':
            yellow_letters[guess[i-1]] = i
        elif result[i] == 'n':
            grey_letters[guess[i - 1]] = i
        else:
            print('Your input must be incorrect')


def get_most_freq_letters_in_dataframe(rem_df: pd.DataFrame) -> list:
    freq_dict = dict()
    index: Optional[int]
    for index, row in rem_df.iterrows():
        word = row['Wordle']
        for l in word:
            if l in freq_dict:
                freq_dict[l] += -100 / math.log(index + 50) ** 2
            else:
                freq_dict[l] = -1.0

    return [k for k, v in sorted(freq_dict.items(), key=lambda item: item[1])]  # sort by value


while turns <= 6 and len(green_letters) < 5:
    turns += 1
    guess = ""
    if turns == 1:
        guess = 'crane'
        print(guess)
        get_results_from_user(guess)
        update_after_guess()
    elif len(green_letters) * 2 + len(yellow_letters) >= 4:
        guess = df.iloc[0][0]
        print(guess)
        get_results_from_user(guess)
        update_after_guess()
    else:
        guess_df = greenless_df
        freq_list = get_most_freq_letters_in_dataframe(df)
        print(freq_list)
        print(df)
        for green in green_letters:
            freq_list.remove(green)

        future_guess_df = guess_df
        freq_idx = 0
        while len(future_guess_df) != 0:
            guess_df = future_guess_df
            future_guess_df = future_guess_df[future_guess_df['Wordle'].
                str.contains(freq_list[freq_idx], na=False)]
            freq_idx += 1
        guess = guess_df.iloc[0][0]
        print(guess)
        get_results_from_user(guess)
        update_after_guess()
