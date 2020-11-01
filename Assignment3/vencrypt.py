import sys

def make_key_file():
    with open("key-01", "wb") as fh:
        fh.write(b"\x01")
        fh.close

def main():

    if len(sys.argv) != 4:
        print("Wrong number of arguments")
        return
    
    # define files
    #make_key_file()
    #key_file = open("key-01", "rb")
    key_file = open(sys.argv[1], "rb")

    plain_file = open(sys.argv[2], "rb")
    cipher_file = open(sys.argv[3], "wb+")
    if not (plain_file and cipher_file):
        print("Error with opening files")
        return

    # encrypt
    while True:
        p = plain_file.read(1)
        if not p:
            break 
        
        if key_file:
            k = key_file.read(1)
            if not k:
                key_file.seek(0)
                k = key_file.read(1)
        else:
            k = 0

        c = int.from_bytes(p,byteorder=sys.byteorder) + int.from_bytes(k,byteorder=sys.byteorder)
        c %= 256 
        cipher_file.write(int.to_bytes(c,byteorder=sys.byteorder,length=1))
    
    key_file.close()
    plain_file.close()
    key_file.close()

if __name__ == "__main__":
    main()