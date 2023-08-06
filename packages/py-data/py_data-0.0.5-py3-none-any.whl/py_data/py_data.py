# Epic package to load/save data.
import os


class Data:
    values = {}

    def __init__(self, name):
        self.name = name + ".data"
        self.read_file()

    def read_file(self):
        if os.path.isfile(self.name):
            with open(self.name, "r", encoding="UTF-8") as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if value.isdigit():
                        self.values[key] = int(value)
                    else:
                        self.values[key] = value
        else:
            file = open(self.name, "w+", encoding="UTF-8")
            file.close()

    def write_file(self):
        with open(self.name, "w", encoding="UTF-8") as file:
            for key in self.values.keys():
                value = self.values[key]
                line = str(key) + "=" + str(value) + "\n"
                file.write(line)

    def append_file(self, key, value):
        with open(self.name, "a+", encoding="UTF-8") as file:
            line = str(key) + "=" + str(value) + "\n"
            file.write(line)

    def save_value(self, key, value):
        if key not in self.values.keys():
            self.values[key] = value
            self.append_file(key, value)
            return True, 1
        else:
            self.values[key] = value
            self.write_file()
            return True, 0

    def read_value(self, key):
        if key in self.values.keys():
            return self.values[key]
        else:
            raise KeyError("Key doesn't exist")

    def save(self):
        self.write_file()


if __name__ == "__main__":
    print("testing")

    dataobj = Data("testing")
    print(dataobj.values)
    dataobj.save_value("x", 400)
    dataobj.save_value("c", "Apelsin")
    dataobj.save_value("d", "Palk")
    dataobj.save_value("b", 126)
    print(type(dataobj.read_value("x")))
    print(dataobj.read_value("c"))
    print(dataobj.read_value("b"))
    dataobj.save()
