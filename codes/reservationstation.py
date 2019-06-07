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

    def __repr__(self):
        return '%5r\tBusy: %5r\tRemain: %5r\tFU: %5r\tOP: %5r\t Immediate: %5r' % (self.name, self.busy, self.remain, self.FU, self.op, self.im)


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

    def __repr__(self):
        return '%5r\tBusy: %5r\tRemain: %5r\tFU: %5r\tOP: %5r\tVj: %5r\tVk: %5r\tQj: %5r\tQk: %5r' % (self.name, self.busy, self.remain, self.FU, self.op, self.vj, self.vk, self.qj, self.qk)


class ARS(RS):

    def __init__(self, id):
        self.name = 'ARS' + str(id)


class MRS(RS):

    def __init__(self, id):
        self.name = 'MRS' + str(id)


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
