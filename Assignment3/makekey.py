def main():
    with open("key-03", "wb") as fh:
        fh.write(b"\x03")
        fh.close
if __name__ == "__main__":
    main()