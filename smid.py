refs= [ 'data\\CZ_KKY_APK_dump.ref-1.pkl']

import pickle
import time
start = time.time()
from main import initialize, find_similar
print( " - doba importu:", time.time()-start)

n=1

for refx in refs:
    pkl_file = open(refx, 'rb')
    ref = pickle.load(pkl_file)
    pkl_file.close()
    start = time.time()
    print(refx)
    data = initialize("data\\CZ_KKY_APK_dump.txt", 'utf-8')
    print( " - doba načtení:", time.time()-start)
    chyb = 0
    start = time.time()
    for i in range(n):
        for word,dist in ref:
            similar = find_similar(word, data, distance = dist)
            chyb_local = ref[(word,dist)].symmetric_difference(similar)   # s.symmetric_difference(t) 	reslult is a new set with elements in either s or t but not both
            if len(chyb_local) > 0:
                print( "\nchyba    :", word, dist)
                print( "nalezeno :", similar)
                print( "správně  :", ref[(word,dist)])
            chyb += len(chyb_local)
    print( " - doba hledání prumer:", (time.time()-start)/n)
    print( 'errors:', chyb)