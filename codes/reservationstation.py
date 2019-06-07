# -*- coding: UTF-8 -*-
from config import Config

class LoadBuffer():

    def __init__(self, id):
        self.inst = None
        self.name = 'LB' + str(id)
        self.busy = False
        self.remain = None
        self.FU = None
        self.op = None
        self.im = None

    def free(self):
        self.inst = None
        self.busy = False
        self.remain = None
        self.FU = None
        self.op = None
        self.im = None

    def __repr__(self):
        return '%5r\tBusy: %5r\tRemain: %5r\tFU: %5r\tOP: %5r\tImmediate: %5r\tInst: %s' % (self.name, self.busy, self.remain, self.FU, self.op, self.im, self.inst)


class RS():
    inst = None
    name = ''
    busy = False
    remain = None
    FU = None
    op = None
    vj = None
    vk = None
    qj = None
    qk = None

    def free(self):
        self.inst = None
        self.busy = False
        self.remain = None
        self.FU = None
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None

    def __repr__(self):
        return '%5r\tBusy: %5r\tRemain: %5r\tFU: %5r\tOP: %5r\tVj: %5r\tVk: %5r\tQj: %5r\tQk: %5r' % (self.name, self.busy, self.remain, self.FU, self.op, self.vj, self.vk, self.qj, self.qk)


class ARS(RS):

    def __init__(self, id):
        self.name = 'ARS' + str(id)

    def result(self):
        if self.op == Config.OP_ADD:
            return self.vj + self.vk
        elif self.op == Config.OP_SUB:
            return self.vj - self.vk
        else:
            return None


class MRS(RS):

    def __init__(self, id):
        self.name = 'MRS' + str(id)

    def result(self):
        if self.op == Config.OP_MUL:
            return self.vj * self.vk
        elif self.op == Config.OP_DIV:
            if self.vk != 0:
                return self.vj / self.vk
            else:
                 return self.vj
        else:
            return None


class ReservationStation():

    def __init__(self):
        self.LB = {}
        for i in range(Config.LB):
            self.LB['LB'+str(i)] = LoadBuffer(i)
        self.ARS = {}
        for i in range(Config.ARS):
            self.ARS['ARS'+str(i)] = ARS(i)
        self.MRS = {}
        for i in range(Config.MRS):
            self.MRS['MRS'+str(i)] = MRS(i)

    def __repr__(self):
        for LB in self.LB.values():
            print (LB)
        for ARS in self.ARS.values():
            print (ARS)
        for MRS in self.MRS.values():
            print (MRS)
        return ''

    def busy(self, inst):
        if inst.op == Config.OP_LD:
            for LB in self.LB.values():
                if LB.busy is False:
                    return LB.name
        elif inst.op == Config.OP_ADD or inst.op == Config.OP_SUB:
            for ARS in self.ARS.values():
                if ARS.busy is False:
                    return ARS.name
        elif inst.op == Config.OP_MUL or inst.op == Config.OP_DIV:
            for MRS in self.MRS.values():
                if MRS.busy is False:
                    return MRS.name
        else:
            return None
        return None

    def write(self, name, value):
        for ARS in self.ARS.values():
            if ARS.qj == name:
                ARS.qj = None
                ARS.vj = value
            if ARS.qk == name:
                ARS.qk = None
                ARS.vk = value
        for MRS in self.MRS.values():
            if MRS.qj == name:
                MRS.qj = None
                MRS.vj = value
            if MRS.qk == name:
                MRS.qk = None
                MRS.vk = value
