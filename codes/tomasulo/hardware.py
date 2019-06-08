# -*- coding: UTF-8 -*-
from .config import Config

class HardWare():
    name = ''
    op = None
    status = None
    vj = None
    vk = None

    def free(self):
        self.op = None
        self.status = None
        self.vj = None
        self.vk = None

    def __repr__(self):
        return '%5r\tSTATUS: %5r\tOP: %5r\tVj: %5r\tVk: %5r' % (self.name, self.status, self.op, self.vj, self.vk)


class Adder(HardWare):

    def __init__(self, id):
        self.name = 'Add' + str(id)


class Multer(HardWare):

    def __init__(self, id):
        self.name = 'Mult' + str(id)


class Loader(HardWare):

    def __init__(self, id):
        self.name = 'Load' + str(id)


Add = {}
for i in range(Config.ADDER):
    Add['Add'+str(i)] = Adder(i)

Mult = {}
for i in range(Config.MULTER):
    Mult['Mult'+str(i)] = Multer(i)

Load = {}
for i in range(Config.LOADER):
    Load['Load'+str(i)] = Loader(i)
