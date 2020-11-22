from itertools import chain, combinations_with_replacement
import time

def work_back(work, length):

    go_back = 1
    # loop in reverse
    for idx in range( length, -1, -1 ):
        # check if at last char
        if work[idx] == chr(126):
            go_back = 1
            work[idx] = chr(33)
        else:
            go_back = 0
            work[idx] = chr( ord(work[idx]) + 1 )
            break

    if go_back == 1:
        work.append( chr(33) )
        length += 1

    return work, length

def powerset(iterable, length):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    return chain.from_iterable(combinations_with_replacement(iterable, r) for r in range(length, length + 1))


iterable = [ chr(i) for i in range(33, 127) ]
start = time.time()
#print( list(powerset( iterable, 3 )) )
ret = list(powerset( iterable, 4 ))
end = time.time()
#print(ret)
print( end - start )
