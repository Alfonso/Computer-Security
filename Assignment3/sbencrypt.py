#!/usr/bin/python3
import sys

# Constants
BLOCK_SIZE = 16

def create_IV(seed):
    iv = []
    val = lcg( seed )
    iv.append( val )
    for idx in range( BLOCK_SIZE - 1 ):
        val = lcg( val )
        iv.append( val )
    # print(iv)
    return iv

# linear congruential generator
def lcg(x_n):
    return (1103515245 * x_n + 12345) % 256

# sbdm hash
def sbdm(str):
    max = 18446744073709551615 + 1
    hash, c = 0, 0
    for char in str:
        c = ord(char)
        hash = c + (hash << 6) + (hash << 16) - hash
        # print("{}: {}".format(c, hash))

    # have to mod by max because I am using python
    return hash % max

# padding
def pad( m ):
    if len( m ) == 0:
        # return a whole block worth of padding
        temp_list = []
        for i in range( BLOCK_SIZE ):
            temp_list.append( BLOCK_SIZE )
        m = bytes( temp_list )
        return m
    # return amount based on how many bytes left out of BLOCK_SIZE

    # add the curr values in m to a temp list that we are
    # then going to add the padding to
    temp_list = []
    for val in m:
        temp_list.append( val )

    # tack on the remaining padding
    for idx in range( BLOCK_SIZE - len(m) ):
        temp_list.append( BLOCK_SIZE - len(m) )

    m = bytes( temp_list )

    return m

# byte shuffling
def bs(temp, key_stream):

    # convert to list to be able to swap
    temp = list(temp)

    for i in range( BLOCK_SIZE ):
        first = key_stream[i] & (BLOCK_SIZE - 1)
        second = (key_stream[i] >> 4) & (BLOCK_SIZE - 1)
        # print('temp: {}'.format(temp))
        # print('keys: {}'.format(key_stream))
        # print('first: {}, second: {}'.format(first,second))
        temp[first], temp[second] = temp[second], temp[first]

    return bytes( temp )

def xor(plain, other):
    res = []
    for idx in range(len(plain)):
        res.append( plain[idx] ^ other[idx] )
    return bytes( res )

def main():
    # check args
    if len(sys.argv) != 4:
        print("incorrect number of args")
        return -1

    password = sys.argv[1]

    # check the file
    start_file = open(sys.argv[2], "rb")
    end_file = open(sys.argv[3], "wb+")

    if not start_file:
        print("File does not exist")
        return -1

    # create the seed
    seed = sbdm( password )

    # create the iv
    iv = create_IV( seed )
    # print('iv: {}'.format(iv))

    run = True
    first = True
    cipher = []

    # read data block by block
    while run:
        # we want to read BLOCK_SIZE bytes
        m = start_file.read( BLOCK_SIZE )

        # check if at end
        if len( m ) != BLOCK_SIZE:
            # pad
            m = pad( m )
            run = False

        # xor plain and iv / old cipher
        if first:
            first = False
            # XOR
            temp = xor( m, iv )
            # Gen new key_stream
            key_stream = create_IV( iv[-1] )
        else:
            # XOR
            temp = xor( m, cipher )
            key_stream = create_IV( key_stream[-1] )
        
        # swap using key stream
        swap = bs( temp, key_stream )

        # xor plain and key stream
        cipher = xor( swap, key_stream )
        
        # print('after xor: {}'.format(list(cipher)))

        # write cipher
        end_file.write( cipher )
    
    start_file.close()
    end_file.close()

if __name__ == "__main__":
    main()