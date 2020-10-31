from enigma import Enigma
from sys import argv


BASE = 256
ENIGMA_CONFIG = "initial_state"
# argv[1] - rotors number
# argv[2] - file to encode


def write_to_bfile(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)


def read_from_bfile(file_name):
    file_to_encode = open(file_name, 'rb')
    data = file_to_encode.read()
    file_to_encode.close()
    return data


def read_config(rotors_num):
    config = []
    with open(ENIGMA_CONFIG, 'r') as file:
        for i in range(rotors_num):
            config.append(list(map(int, file.readline()[:-1].split(" "))))
    return config


def main():
    if not argv[1] or not argv[2]:
        print("1st arg - rotors number, 2nd - file name")
    enigma = Enigma(int(argv[1]), BASE)

    # save state here
    state = enigma.get_state()
    for i in range(len(state)):
        state[i] = list(map(str, state[i]))

    with open(ENIGMA_CONFIG, 'w') as file_state:
        for lst in state:
            file_state.write(" ".join(lst))
            file_state.write("\n")

    # files for results
    file_name_encoded = "encoded_" + argv[2]
    file_name_decoded = "decoded_" + argv[2]

    # data to encrypt
    data = read_from_bfile(argv[2])
    if not data:
        print("file is empty. nothing to encode")
        return
    # print("data to encrypt: ", data)

    # encryption

    result = enigma.encrypt(data)
    write_to_bfile(file_name_encoded, result)
    # print("encoded: ", result)

    # decryption

    # reset to initial state
    config = read_config(int(argv[1]))
    enigma.read_config(config, BASE)
    data = read_from_bfile(file_name_encoded)
    if not data:
        print("file is empty. nothing to decode")
        return

    result = enigma.encrypt(data)
    write_to_bfile(file_name_decoded, result)
    # print("decoded: ", result)


if __name__ == "__main__":
    main()
