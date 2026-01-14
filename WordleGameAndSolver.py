
import typing
import random
import math

from urllib.request import Request, urlopen
url="https://raw.githubusercontent.com/tabatkins/wordle-list/255b9469c4dad99a3b95cc4ddbe139b3d3747868/words"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

web_byte = urlopen(req).read()

webpage = web_byte.decode('utf-8')
words = webpage[:-1].split("\n")
random.shuffle(words)
selectwordlist = words[0:250]
word = words[0]


class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)


def checkpositions(whole_word: str, char: str) -> typing.List[int]:
    positions = []
    pos = whole_word.find(char)
    while pos != -1:
        positions.append(pos)
        pos = whole_word.find(char, pos + 1)
    return positions


def checkwordle(word: str, current_guess: str) -> typing.List[str]:
    output = ["gray"] * len(word)
    counted_pos = set()
    for x, (word_char, current_guess_char) in enumerate(zip(word, current_guess)):
        if word_char == current_guess_char:
            output[x] = "green"
            counted_pos.add(x)
    for x, current_guess_char in enumerate(current_guess):
        if current_guess_char in word and output[x] != "green":
            positions = checkpositions(whole_word=word, char=current_guess_char)
            for pos in positions:
                if pos not in counted_pos:
                    output[x] = "yellow"
                    counted_pos.add(pos)

                    break
    return output



def cutlist(bad_guess,wordlist):
    unwanted = []
    for j in range(5):
        if checkwordle(word, bad_guess)[j] == "gray":
            for i in range(len(wordlist)):
                if bad_guess[j] in wordlist[i] and (i not in unwanted):
                    unwanted.append(i)
        if checkwordle(word, bad_guess)[j] == "yellow":
            for i in range(len(wordlist)):
                if bad_guess[j] not in wordlist[i] and (i not in unwanted):
                    unwanted.append(i)
       
    unwanted.sort()
    if unwanted[0] == 0:
        unwanted.pop(0)
    for i in reversed(unwanted):
        wordlist.pop(i)
    return wordlist


def findprob(guess):
    order = checkwordle(word, guess)
    probability = 0
    info = 0
    completedletters = []
    for i in range(5):
        for j in range(len(selectwordlist)):                
            if (checkwordle(word, selectwordlist[j])[i] == order[i]) and (guess[i] in selectwordlist[j]):
                probability += 1
            if guess[i] in completedletters:
                probability = 0
        if probability > 0:
            info += math.log2(probability)
        probability = 0
        completedletters.append(guess[i])
   
       
    return info
                   

def findtheword(selectwordlist):
    highest_info = 0
    highest_word = ""  
    for i in range(len(selectwordlist)):
        guess = selectwordlist[i]
        information = findprob(guess)
        if information > highest_info:
            highest_info = information
            highest_word = guess
       
    if highest_info == 0:
        print("the recommended word is:", selectwordlist[0], "giving", 0.0, "bit of information")
        return
    print("the recommended word is:", highest_word, "giving", highest_info, "bits of information")


word = word.lower()
import os
os.system("")  
COLOR = {"ENDC": "\033[0m",}

invalid = "1234567890!£$%^&*()_+{}¬@~>?<|-=[];#,."
guesses = 6
current_guess = ""
wordle = []
usedletters = ""
pure_word = ""
valid = True
win = False
previous_wordle = "\n\nprevious guesses:\n"

for i in range(len(word)):
    wordle += "_"
print(wordle)

mode = input("chose a mode 'game' or 'helper'")

while guesses > 0 and win == False:
    current_guess = ""
    print("\n guesses =", guesses)
    if mode == "helper":
        findtheword(selectwordlist)
    current_guess = input("input your guess of the word\n")
    current_guess = current_guess.lower()
    for i in range(len(current_guess)):
        if current_guess[i] in invalid:
            valid = False
            print("there are invalid characters in your guess")
    uppercase_guess = current_guess.upper() + current_guess[1:-1]
    if len(current_guess) == len(word) and valid == True and (current_guess in words) or (uppercase_guess in words):
        wordle = ""
        pure_word = checkwordle(word,current_guess)
        for j in range(len(word)):
            if pure_word[j] == "gray":
                wordle += ANSI.background(7) + ANSI.color_text(49) + ANSI.style_text(90) + current_guess[j]
            elif pure_word[j] == "yellow":
                wordle += ANSI.background(7) + ANSI.color_text(49) + ANSI.style_text(33) + current_guess[j]
            else:
                wordle += ANSI.background(7) + ANSI.color_text(49) + ANSI.style_text(32) + current_guess[j]
           
        previous_wordle += wordle
        previous_wordle += COLOR["ENDC"] + "\n"
       
        print(previous_wordle)
       
        for l in range(len(word)):
            if current_guess[l] != word[l]:
                win = False
                guesses -= 1
                break
            else:
                win = True
    elif current_guess not in words and valid == True and len(word) == len(current_guess):
        print("your guess is not in our wordlist")
    if win == False and mode == "helper":
        selectwordlist = cutlist(current_guess, selectwordlist)
   
if win == True:
    print("\n well done, the word was", word)
elif win == False and mode == "game":
    print("\n you lost, the word was", word)






