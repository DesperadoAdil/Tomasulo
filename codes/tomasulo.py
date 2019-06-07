# -*- coding: UTF-8 -*-
from config import Config
from instruction import Instruction
from register import Register
from reservationstation import ReservationStation as RS
from hardware import Add, Mult, Load

class tomasulo():

    def __init__(self):
        self.memory = [0] * Config.MEMORY
        self.clock = 0
        self.PC = 0
        self.inst = []
        self.RS = RS()
        self.register = []
        for i in range(Config.RIGISTER):
            self.register.append(Register(i))
        print ("tomasulo!")

    def __repr__(self):
        for inst in self.inst:
            print (inst)
        print (self.RS)
        for register in self.register:
            print (register)
        return 'PC: %r' % self.PC

    def insert_inst(self, inst):
        self.inst.append(Instruction(inst.strip()))

    def step(self, n):
        while n > 0:
            self.clock += 1
            inst = self.inst[self.PC]
            #ISSUE
            res = self.RS.busy(inst)
            if res is not None:
                print ('%s free to go!' % inst.content)
                inst.Issue = self.clock
                #self.RS.fire(inst, res)

                if inst.op == Config.OP_LD:
                    self.RS.LB[res].busy = True
                    self.RS.LB[res].op = inst.op
                    self.RS.LB[res].im = inst.rgst_int[-1]
                    self.findRegister(inst.rgst_int[-2]).status = self.RS.LB[res].name
                elif inst.op == Config.OP_ADD or inst.op == Config.OP_SUB:
                    self.RS.ARS[res].busy = True
                    self.RS.ARS[res].op = inst.op
                    if self.findRegister(inst.rgst_int[-2]).status:
                        self.RS.ARS[res].qj = self.findRegister(inst.rgst_int[-2]).status
                    else:
                        self.RS.ARS[res].vj = self.findRegister(inst.rgst_int[-2]).value

                    if self.findRegister(inst.rgst_int[-1]).status:
                        self.RS.ARS[res].qk = self.findRegister(inst.rgst_int[-1]).status
                    else:
                        self.RS.ARS[res].vk = self.findRegister(inst.rgst_int[-1]).value

                    self.findRegister(inst.rgst_int[-3]).status = self.RS.ARS[res].name
                elif inst.op == Config.OP_MUL or inst.op == Config.OP_DIV:
                    self.RS.MRS[res].busy = True
                    self.RS.MRS[res].op = inst.op
                    if self.findRegister(inst.rgst_int[-2]).status:
                        self.RS.MRS[res].qj = self.findRegister(inst.rgst_int[-2]).status
                    else:
                        self.RS.MRS[res].vj = self.findRegister(inst.rgst_int[-2]).value

                    if self.findRegister(inst.rgst_int[-1]).status:
                        self.RS.MRS[res].qk = self.findRegister(inst.rgst_int[-1]).status
                    else:
                        self.RS.MRS[res].vk = self.findRegister(inst.rgst_int[-1]).value

                    self.findRegister(inst.rgst_int[-3]).status = self.RS.MRS[res].name
                elif inst.op == Config.OP_JUMP:
                    pass
                else:
                    return None
                self.PC += 1
            else:
                print ('no')

            #EXCUTE

            #WRITEBACK

            n -= 1

    def findRegister(self, str):
        for register in self.register:
            if register.name == str:
                return register


if __name__ == '__main__':
    toma = tomasulo()

    with open('samp.txt', encoding = 'utf8') as f:
        for line in f.readlines():
            toma.insert_inst(line)
    print (toma)

    while True:
        lin = input()
        if lin.lower() == "exit":
            break
        toma.step(int(lin))
        print (toma)
