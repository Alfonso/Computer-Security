def main():
    with open("key-02", "wb") as fh:
        fh.write(b"\x02")
        fh.close
if __name__ == "__main__":
    main()