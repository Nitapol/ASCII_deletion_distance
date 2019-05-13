import re

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

phrase = "Purple cow"


# text = [ '1. What is the biggest planet of our Solar system?\n',
#          '2. How to make tea\n?',
#          "3. Which our Solar system's biggest planet?\n"
#          '4. How to make tea\n?',
#         ]
#
# In this case it should result:-
# 3 . Which our Solar system's biggest planet?


print(is_phrase_in(phrase, "Purple cows make the best pets!"))   # False
print(is_phrase_in(phrase, "Your purple cow trampled my hedge!"))  # True
from difflib import SequenceMatcher

sentences = []
for line in text:
        sentences.append(line)
# with open('./bp.txt', 'r') as f:
#     for line in f:
#         # only consider lines that have numbers at the beginning
#         if line.split('.')[0].isdigit():
#             sentences.append(line.split('\n')[0])
for line in sentences:
    print(line)
max_prob = 0
similar_sentence = None
length = len(sentences)
for i in range(length):
    for j in range(i+1,length):
        match_ratio = SequenceMatcher(None, sentences[i], sentences[j]).ratio()
        if  match_ratio > max_prob:
            max_prob = match_ratio
            similar_sentence = sentences[j]
if similar_sentence is not None:
    print(max_prob)
    print(similar_sentence)


import timeit
for i in range(96,1,-1): # [96, 95, 94, 93, 92, 91]:  # range(100, 90, -1):
    tm = timeit.repeat('np.matmul(a, b)', number = 10000,
        setup = 'import numpy as np; a, b = np.random.rand({0},{1}), np.random.rand({2})'.format(i,96,96))
    print(i, sum(tm) / 5)
