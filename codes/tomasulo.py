# -*- coding: UTF-8 -*-
from config import Config
from instruction import Instruction
from register import Register
from reservationstation import ReservationStation as RS
from hardware import Add, Mult, Load

class tomasulo():

    def __init__(self):
        self.clock = 0
        self.PC = 0
        self.inst = []
        self.RS = RS()
        self.register = {}
        for i in range(Config.RIGISTER):
            self.register['F'+str(i)] = Register(i)
        print ("tomasulo!")

    def __repr__(self):
        for inst in self.inst:
            print (inst)
        print (self.RS)
        for register in self.register.values():
            print (register)
        return 'PC: %r' % self.PC

    def insert_inst(self, inst):
        self.inst.append(Instruction(inst.strip()))

    def reset(self):
        self.clock = 0
        self.PC = 0
        for LB in self.RS.LB.values():
            LB.free()
        for ARS in self.RS.ARS.values():
            ARS.free()
        for MRS in self.RS.MRS.values():
            MRS.free()

        for register in self.register.values():
            register.free()

        for loader in Load.values():
            loader.free()
        for adder in Add.values():
            adder.free()
        for multer in Mult.values():
            multer.free()

    def step(self, n):
        while n > 0:
            self.clock += 1

            #WRITEBACK
            for LB in self.RS.LB.values():
                if LB.busy is True and LB.remain == 0:
                    self.inst[LB.inst].WriteResult = self.clock
                    for register in self.register.values():
                        if register.status == LB.name:
                            register.status = None
                            register.value = LB.im
                    self.RS.write(LB.name, LB.im)
                    LB.free()

            for ARS in self.RS.ARS.values():
                if ARS.busy is True and ARS.remain == 0:
                    self.inst[ARS.inst].WriteResult = self.clock
                    for register in self.register.values():
                        if register.status == ARS.name:
                            register.status = None
                            register.value = ARS.result()
                    self.RS.write(ARS.name, ARS.result())
                    ARS.free()

            for MRS in self.RS.MRS.values():
                if MRS.busy is True and MRS.remain == 0:
                    self.inst[MRS.inst].WriteResult = self.clock
                    for register in self.register.values():
                        if register.status == MRS.name:
                            register.status = None
                            register.value = MRS.result()
                    self.RS.write(MRS.name, MRS.result())
                    MRS.free()

            #EXCUTE
            for LB in self.RS.LB.values():
                if LB.busy is True and LB.remain is not None:
                    LB.remain -= 1
                    if LB.remain == 0:
                        self.inst[LB.inst].ExecComp = self.clock
                        Load[LB.FU].free()

            for ARS in self.RS.ARS.values():
                if ARS.busy is True and ARS.remain is not None:
                    ARS.remain -= 1
                    if ARS.remain == 0:
                        self.inst[ARS.inst].ExecComp = self.clock
                        Add[ARS.FU].free()

            for MRS in self.RS.MRS.values():
                if MRS.busy is True and MRS.remain is not None:
                    MRS.remain -= 1
                    if MRS.remain == 0:
                        self.inst[MRS.inst].ExecComp = self.clock
                        Mult[MRS.FU].free()

            #ISSUE
            inst = self.inst[self.PC]
            res = self.RS.busy(inst)
            if res is not None:
                print ('%s free to go!' % inst.content)
                inst.Issue = self.clock

                if inst.op == Config.OP_LD:
                    self.RS.LB[res].busy = True
                    self.RS.LB[res].op = inst.op
                    self.RS.LB[res].inst = self.PC
                    self.RS.LB[res].im = inst.rgst_int[-1]
                    self.register[inst.rgst_int[-2]].status = self.RS.LB[res].name
                elif inst.op == Config.OP_ADD or inst.op == Config.OP_SUB:
                    self.RS.ARS[res].busy = True
                    self.RS.ARS[res].op = inst.op
                    self.RS.ARS[res].inst = self.PC
                    if self.register[inst.rgst_int[-2]].status:
                        self.RS.ARS[res].qj = self.register[inst.rgst_int[-2]].status
                    else:
                        self.RS.ARS[res].vj = self.register[inst.rgst_int[-2]].value

                    if self.register[inst.rgst_int[-1]].status:
                        self.RS.ARS[res].qk = self.register[inst.rgst_int[-1]].status
                    else:
                        self.RS.ARS[res].vk = self.register[inst.rgst_int[-1]].value

                    self.register[inst.rgst_int[-3]].status = self.RS.ARS[res].name
                elif inst.op == Config.OP_MUL or inst.op == Config.OP_DIV:
                    self.RS.MRS[res].busy = True
                    self.RS.MRS[res].op = inst.op
                    self.RS.MRS[res].inst = self.PC
                    if self.register[inst.rgst_int[-2]].status:
                        self.RS.MRS[res].qj = self.register[inst.rgst_int[-2]].status
                    else:
                        self.RS.MRS[res].vj = self.register[inst.rgst_int[-2]].value

                    if self.register[inst.rgst_int[-1]].status:
                        self.RS.MRS[res].qk = self.register[inst.rgst_int[-1]].status
                    else:
                        self.RS.MRS[res].vk = self.register[inst.rgst_int[-1]].value

                    self.register[inst.rgst_int[-3]].status = self.RS.MRS[res].name
                elif inst.op == Config.OP_JUMP:
                    pass
                else:
                    return None
                self.PC += 1
            else:
                print ('no free RS!')

            #EXCUTE HardWare
            for LB in self.RS.LB.values():
                if LB.busy is True and LB.FU is None:
                    for loader in Load.values():
                        if loader.status is None:
                            loader.op =  self.inst[LB.inst].op
                            loader.status = LB.name
                            loader.vj = LB.im
                            LB.remain = Config.TIME[loader.op]
                            LB.FU = loader.name
                            break

            for ARS in self.RS.ARS.values():
                if ARS.busy is True and ARS.FU is None and ARS.vj is not None and ARS.vk is not None:
                    for adder in Add.values():
                        if adder.status is None:
                            adder.op =  self.inst[ARS.inst].op
                            adder.status = ARS.name
                            adder.vj = ARS.vj
                            adder.vk = ARS.vk
                            ARS.remain = Config.TIME[adder.op]
                            ARS.FU = adder.name
                            break

            for MRS in self.RS.MRS.values():
                if MRS.busy is True and MRS.FU is None and MRS.vj is not None and MRS.vk is not None:
                    for multer in Mult.values():
                        if multer.status is None:
                            multer.op =  self.inst[MRS.inst].op
                            multer.status = MRS.name
                            multer.vj = MRS.vj
                            multer.vk = MRS.vk
                            MRS.remain = Config.TIME[multer.op]
                            MRS.FU = multer.name
                            break

            n -= 1


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
        elif lin.lower() == "reset":
            toma.reset()
        else:
            toma.step(int(lin))
        print (toma)
        for loader in Load.values():
            print (loader)
        for adder in Add.values():
            print (adder)
        for multer in Mult.values():
            print (multer)
