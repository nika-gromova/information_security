from sys import argv
from aes128 import encrypt_block


def write_to_bfile(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)


def read_from_bfile(file_name):
    file_to_encode = open(file_name, 'rb')
    data = file_to_encode.read()
    file_to_encode.close()
    return data


def main():
    if not argv[1] or not argv[2]:
        print("main.py file_to_encrypt key_file")

    file_name = argv[1]
    key_file = argv[2]
    # files for results
    file_name_encoded = "encoded_" + file_name
    file_name_decoded = "decoded_" + file_name

    # data to encrypt
    data = read_from_bfile(file_name)
    if not data:
        print("file is empty. nothing to encode")
        return
    print("data to encrypt: ", data)

    key = read_from_bfile(key_file)
    if not key:
        print("key is empty. try again")
        return
    if len(key) > 16:
        print("key is too long. try again")
        return
    for symbol in key:
        if symbol > 0xff:
            print('key must contain only latin alphabet and numbers')
            return

    # encryption
    encrypted_data = []
    temp = []
    flag = False
    for byte in data:
        flag = True
        temp.append(byte)
        if len(temp) == 16:
            flag = False
            encrypted_part = encrypt_block(temp, key)
            encrypted_data.extend(encrypted_part)
            del temp[:]
    if flag:
        for i in range(16 - len(temp)):
            temp.append(0x0)

    encrypted_data.extend(encrypt_block(temp, key))

    write_to_bfile(file_name_encoded, bytes(encrypted_data))
    print("encoded: ", encrypted_data)

    # decryption


if __name__ == "__main__":
    main()