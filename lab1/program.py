from installer import check_key


def main():
    if check_key():
        print("Hello, world!")
    else:
        print("Sorry, you should first install my app")



if __name__ == "__main__":
    main()
