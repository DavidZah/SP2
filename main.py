import numpy as np
import time
import pickle
import os.path
import traceback


def levenshtein(word, hypotesiz,word_len):
    hyp_len = len(hypotesiz)
    if word == hypotesiz:
        return 0
    elif word_len == 0:
        return hyp_len
    elif hyp_len == 0:
        return word_len
    v0 = [None] * (hyp_len + 1)
    v1 = [None] * (hyp_len + 1)

    len_v0 = len(v0)
    for i in range(len_v0):
        v0[i] = i
    for i in range(word_len):
        v1[0] = i + 1
        for j in range(hyp_len):
            cost = 0 if word[i] == hypotesiz[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len_v0):
            v0[j] = v1[j]

    return v1[hyp_len]

def initialize(path,ecoding):
    f = open(path, 'r',encoding=ecoding)
    data = f.read()
    data = data.split()
    return data


def find_similar(word,data,distance):
    ret = []
    word_len = len(word)

    for x in data:
        if(distance == levenshtein(word,x)):
           ret.append(x)
    return ret



if __name__ == '__main__':
    start = time.time()
    data = initialize("data\\CZ_KKY_APK_dump.txt", 'utf-8')
    print('počet slov:', len(data), " - doba načtení:", time.time() - start)



    # load reference data
    pkl_file = open('data\\CZ_KKY_APK_dump.ref.pkl', 'rb')
    ref = pickle.load(pkl_file)
    pkl_file.close()

    print(len(ref))
    print(ref.keys())
    print(ref[('sazky', 2)])
    # print('-----')
    # for key in ref:
    #    print(key, ref[key])
    # local test ---------

    for word, dist in ref:
        similar = find_similar(word, data, distance=dist)
        # print word, dist,  similar
        chyb_local = ref[(word, dist)].symmetric_difference(
            similar)  # s.symmetric_difference(t) 	reslult is a new set with elements in either s or t but not both
        if len(chyb_local) > 0:
            print("\nchyba    :", word, dist)
            print("nalezeno :", similar)
            print("správně  :", ref[(word, dist)])

