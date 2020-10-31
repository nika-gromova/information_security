import random
from struct import pack


class Reflector:
    def __init__(self, base):
        self.values = [i for i in range(base - 1, -1, -1)]

    def read_config(self, config_base):
        self.values = [i for i in range(config_base - 1, -1, -1)]

    def get(self, index):
        return self.values[index]

    def get_state(self):
        return self.values


class Rotor:
    def __init__(self, base):
        self.base = base - 1
        self.count = 0
        self.values = [i for i in range(self.base, -1, -1)]
        random.shuffle(self.values)

    def read_config(self, config, config_base):
        self.values = config.copy()
        self.count = 0
        self.base = config_base - 1

    def get(self, index):
        return self.values[index]

    def get_index_of(self, item):
        return self.values.index(item)

    def rotate(self):

        last = self.values[self.base]
        for i in range(self.base, 0, -1):
            self.values[i] = self.values[i - 1]
        self.values[0] = last
        self.count += 1

        if self.count % (self.base + 1) == 0:
            flag = 1
            self.count = 0
        else:
            flag = 0

        return flag

    def get_state(self):
        return self.values


class Enigma:
    def __init__(self, rotors_number, base):
        self.rotors_number = rotors_number
        self.rotors = [Rotor(base) for i in range(rotors_number)]
        self.reflector = Reflector(base)

    def get_state(self):
        state = []
        for rotor in self.rotors:
            state.append(rotor.get_state())
        state.append(self.reflector.get_state())
        return state

    def read_config(self, rotors_config, config_base):
        for i in range(len(rotors_config)):
            self.rotors[i].read_config(rotors_config[i], config_base)
        self.reflector.read_config(config_base)

    def encrypt_one(self, byte):
        result = byte
        for rotor in self.rotors:
            result = rotor.get(result)

        result = self.reflector.get(result)

        for rotor in self.rotors[::-1]:
            result = rotor.get_index_of(result)

        for rotor in self.rotors:
            res = rotor.rotate()
            if not res:
                break
        return result

    def encrypt(self, byte_list):
        result = b""
        for item in byte_list:
            result += pack("B", self.encrypt_one(item))

        return result
