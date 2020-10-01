import time, os
from progress.bar import ChargingBar
from subprocess import check_output
import hashlib


def generate_key():
    output = check_output("wmic diskdrive get serialnumber", shell=True).decode()
    serialnumber = output.split('\n')[1].rstrip()
    return hashlib.sha256(serialnumber.encode('utf-8')).hexdigest()


def get_key():
    if not os.path.exists('./keyfile.txt'):
         return '1'
    file = open('keyfile.txt', 'r')
    if not file:
        return '1'
    return file.readline().split('\n')[0]


def check_key():
    current_key = get_key()
    real_key = generate_key()
    return get_key() == generate_key()


def main():
    answ = str(input("Do ypu really want to install my app? [y/n]: "))
    if answ == "y":
        mylist = [1,2,3]
        bar = ChargingBar("Installing", max = 3)
        bar.next()
        time.sleep(1)

        if os.path.exists('./keyfile.txt'):
            bar.finish()
            print("You have already installed my app")
        else:
            bar.next()
            time.sleep(1)
            file = open('keyfile.txt', 'w')
            if not file:
                bar.finish()
                print("Errors in file system")                
            else:
                file.write(generate_key())
                file.close
                bar.next()
                time.sleep(1)
                bar.finish()
                print("Installed successfully")
        
    elif answ == "n":
        print("Bye!")
    else:
        print("incorrect input")


if __name__ == "__main__":
    main()



