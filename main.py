import string
from collections import OrderedDict
import time
from functools import lru_cache as cache


@cache(maxsize=None)
def levenshtein(s1, s2, s1_len):
    s2_len = len(s2)
    if s1_len < s2_len:
        return levenshtein(s2, s1, s2_len)

    # len(s1) >= len(s2)
    if s2_len == 0:
        return s1_len

    previous_row = range(s2_len + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)

            if (insertions < deletions and insertions < substitutions):
                current_row.append(insertions)
            elif (deletions < substitutions and deletions < insertions):
                current_row.append(deletions)
            else:
                current_row.append(substitutions)

            # current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def initialize(filepath, coding="cp1250"):
    all_words = set()
    with open(filepath, "r", encoding=coding) as file:
        for line in file:
            for word in line.split():
                word = word.strip(string.punctuation).lower()
                all_words.add(word)
    all_words.remove("")
    all_words = list(OrderedDict.fromkeys(all_words))
    return all_words


def find_similar(word, data, distance):
    word = word.lower()
    ret = []
    word_len = len(word)
    for x in data:
        if (distance == levenshtein(word, x, word_len)):
            ret.append(x)
    return ret

if __name__ == '__main__':
    start = time.time()
    data = initialize("data\\CZ_KKY_APK_dump.txt", 'utf-8')
    print('počet slov:', len(data), " - doba načtení:", time.time() - start)
