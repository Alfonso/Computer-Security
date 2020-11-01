import sys

def make_key_file():
    with open("key-80", "wb") as fh:
        fh.write(b"\x80")
        fh.close

def main():
    
    if len(sys.argv) != 4:
        print("Wrong number of arguments")
        return
    
    # define files
    key_file = open(sys.argv[1], "rb")
    cipher_file = open(sys.argv[2], "rb")
    plain_file = open(sys.argv[3], "wb+")
    if not (plain_file and cipher_file):
        print("Error with opening files")
        return

    # decrypt
    while True:
        c = cipher_file.read(1)
        if not c:
            break
        
        if key_file:
            k = key_file.read(1)
            if not k:
                key_file.seek(0)
                k = key_file.read(1)
        else:
            k = 0

        p = int.from_bytes(c,byteorder=sys.byteorder) - int.from_bytes(k,byteorder=sys.byteorder) + 256
        p %= 256
        plain_file.write(int.to_bytes(p,byteorder=sys.byteorder,length=1))
    
    key_file.close()
    plain_file.close()
    key_file.close()

if __name__ == "__main__":
    main()