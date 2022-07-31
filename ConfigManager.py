import os

FILENAME = "config.cnf"


class Config:
    def __init__(self):
        self.__file = FILENAME
        self.options = dict()

    def load(self):
        with open(self.__file, 'r') as file:
            lc = 0
            for line in file.readlines():
                lc = lc + 1
                split = line.split('=')
                if len(split) > 2:
                    print("Chyba v nastavení na řádku: {0} ({1})".format(lc, ''.join(filter(str.isprintable, line))))
                    return False
                split[0] = ''.join(filter(str.isalnum, split[0])).lower()
                split[1] = ''.join(filter(str.isalnum, split[1])).lower()
                self.options[split[0].lower()] = split[1].lower()
        print("Nastavení načteno v pořádku")
        return True
