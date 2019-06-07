# -*- coding: UTF-8 -*-
from config import Config

class HardWare():
    name = ''
    op = None
    status = None
    vj = None
    vk = None


class Adder(HardWare):

    def __init__(self, id):
        self.name = 'Add' + str(id)

    def result(self):
        if slef.op == Config.OP_ADD:
            return self.vj + slef.vk
        elif self.op == Config.OP_SUB:
            return self.vj - slef.vk
        else:
            return None


class Multer(HardWare):

    def __init__(self, id):
        self.name = 'Mult' + str(id)

    def result(self):
        if slef.op == Config.OP_MUL:
            return self.vj * slef.vk
        elif self.op == Config.OP_DIV:
            if self.vk != 0:
                return self.vj / slef.vk
            else:
                 return self.vj
        else:
            return None


class Loader(HardWare):

    def __init__(self, id):
        self.name = 'Load' + str(id)

    def result(self):
        if slef.op == Config.OP_LD:
            return self.vj
        else:
            return None


Add = []
for i in range(Config.ADDER):
    Add.append(Adder(i))

Mult = []
for i in range(Config.MULTER):
    Mult.append(Multer(i))

Load = []
for i in range(Config.LOADER):
    Load.append(Loader(i))
