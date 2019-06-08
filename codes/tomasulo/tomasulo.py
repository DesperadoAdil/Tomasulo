# -*- coding: UTF-8 -*-
from .config import Config
from .instruction import Instruction
from .register import Register
from .reservationstation import ReservationStation as RS
from .hardware import Add, Mult, Load

class Tomasulo():

    def __init__(self):
        self.clock = 0
        self.PC = Register('PC')
        self.inst = []
        self.RS = RS()
        self.register = {}
        for i in range(Config.RIGISTER):
            self.register['F'+str(i)] = Register('F'+str(i))

    def __repr__(self):
        for inst in self.inst:
            print (inst)
        print (self.RS)
        print (self.PC)
        for register in self.register.values():
            print (register)
        return 'Clock: %r' % self.clock

    def insert_inst(self, inst):
        self.inst.append(Instruction(inst.strip()))

    def reset(self):
        self.clock = 0
        self.PC.free()
        for inst in self.inst:
            inst.free()

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

    def end(self):
        return self.PC.value >= len(self.inst) and self.RS.isfree()

    def step(self, n=1):
        while n > 0:
            self.clock += 1

            #WRITEBACK
            for LB in self.RS.LB.values():
                if LB.busy is True and LB.remain == 0:
                    if self.inst[LB.inst].WriteResult is None and self.inst[LB.inst].rs == LB.name:
                        self.inst[LB.inst].WriteResult = self.clock
                    for register in self.register.values():
                        if register.status == LB.name:
                            register.status = None
                            register.value = LB.im
                    self.RS.write(LB.name, LB.im)
                    LB.free()

            for ARS in self.RS.ARS.values():
                if ARS.busy is True and ARS.remain == 0:
                    if self.inst[ARS.inst].WriteResult is None and self.inst[ARS.inst].rs == ARS.name:
                        self.inst[ARS.inst].WriteResult = self.clock
                    if ARS.op != Config.OP_JUMP:
                        for register in self.register.values():
                            if register.status == ARS.name:
                                register.status = None
                                register.value = ARS.result()
                        self.RS.write(ARS.name, ARS.result())
                    else:
                        self.PC.status = None
                        self.PC.value = ARS.result()
                    ARS.free()

            for MRS in self.RS.MRS.values():
                if MRS.busy is True and MRS.remain == 0:
                    if self.inst[MRS.inst].WriteResult is None and self.inst[MRS.inst].rs == MRS.name:
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
                        if self.inst[LB.inst].ExecComp is None and self.inst[LB.inst].rs == LB.name:
                            self.inst[LB.inst].ExecComp = self.clock
                        Load[LB.FU].free()

            for ARS in self.RS.ARS.values():
                if ARS.busy is True and ARS.remain is not None:
                    ARS.remain -= 1
                    if ARS.remain == 0:
                        if self.inst[ARS.inst].ExecComp is None and self.inst[ARS.inst].rs == ARS.name:
                            self.inst[ARS.inst].ExecComp = self.clock
                        Add[ARS.FU].free()

            for MRS in self.RS.MRS.values():
                if MRS.busy is True and MRS.remain is not None:
                    MRS.remain -= 1
                    if MRS.remain == 0:
                        if self.inst[MRS.inst].ExecComp is None and self.inst[MRS.inst].rs == MRS.name:
                            self.inst[MRS.inst].ExecComp = self.clock
                        Mult[MRS.FU].free()

            #ISSUE
            if self.PC.status is None and self.PC.value < len(self.inst):
                inst = self.inst[self.PC.value]
                res = self.RS.busy(inst)
                if res is not None:
                    if inst.Issue is None:
                        inst.Issue = self.clock
                        if inst.op == Config.OP_LD:
                            inst.rs = self.RS.LB[res].name
                        elif inst.op == Config.OP_ADD or inst.op == Config.OP_SUB or inst.op == Config.OP_JUMP:
                            inst.rs = self.RS.ARS[res].name
                        elif inst.op == Config.OP_MUL or inst.op == Config.OP_DIV:
                            inst.rs = self.RS.MRS[res].name
                        else:
                            return

                    if inst.op == Config.OP_LD:
                        self.RS.LB[res].busy = True
                        self.RS.LB[res].op = inst.op
                        self.RS.LB[res].inst = self.PC.value
                        self.RS.LB[res].im = inst.rgst_int[-1]
                        self.register[inst.rgst_int[-2]].status = self.RS.LB[res].name
                    elif inst.op == Config.OP_ADD or inst.op == Config.OP_SUB:
                        self.RS.ARS[res].busy = True
                        self.RS.ARS[res].op = inst.op
                        self.RS.ARS[res].inst = self.PC.value
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
                        self.RS.MRS[res].inst = self.PC.value
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
                        self.RS.ARS[res].busy = True
                        self.RS.ARS[res].op = inst.op
                        self.RS.ARS[res].inst = self.PC.value
                        if self.register[inst.rgst_int[-2]].status:
                            self.RS.ARS[res].qj = self.register[inst.rgst_int[-2]].status
                        else:
                            self.RS.ARS[res].vj = self.register[inst.rgst_int[-2]].value

                        self.RS.ARS[res].vk = inst.rgst_int[-1]
                        self.RS.ARS[res].qk = inst.rgst_int[-3]
                        self.PC.status = self.RS.ARS[res].name
                    else:
                        return
                    if inst.op != Config.OP_JUMP:
                        self.PC.value += 1
                else:
                    pass

            #EXCUTE HardWare
            ready = []
            for LB in self.RS.LB.values():
                if LB.busy is True and LB.FU is None:
                    ready.append(LB)
            ready = sorted(ready, key=lambda x:x.inst)
            loaderlist = []
            for loader in Load.values():
                if loader.status is None:
                    loaderlist.append(loader)
            lenth = min(len(ready), len(loaderlist))
            for i in range(lenth):
                loader = loaderlist[i]
                LB = ready[i]
                loader.op =  self.inst[LB.inst].op
                loader.status = LB.name
                loader.vj = LB.im
                LB.remain = Config.TIME[loader.op]
                LB.FU = loader.name

            ready = []
            for ARS in self.RS.ARS.values():
                if ARS.busy is True and ARS.FU is None and ARS.vj is not None and ARS.vk is not None:
                    ready.append(ARS)
            ready = sorted(ready, key=lambda x:x.inst)
            adderlist = []
            for adder in Add.values():
                if adder.status is None:
                    adderlist.append(adder)
            lenth = min(len(ready), len(adderlist))
            for i in range(lenth):
                adder = adderlist[i]
                ARS = ready[i]
                adder.op =  self.inst[ARS.inst].op
                adder.status = ARS.name
                if adder.op == Config.OP_JUMP:
                    if ARS.vj != ARS.qk:
                        ARS.vk = 1
                    ARS.vj = self.PC.value
                adder.vj = ARS.vj
                adder.vk = ARS.vk
                ARS.remain = Config.TIME[adder.op]
                ARS.FU = adder.name

            ready = []
            for MRS in self.RS.MRS.values():
                if MRS.busy is True and MRS.FU is None and MRS.vj is not None and MRS.vk is not None:
                    ready.append(MRS)
            ready = sorted(ready, key=lambda x:x.inst)
            multerlist = []
            for multer in Mult.values():
                if multer.status is None:
                    multerlist.append(multer)
            lenth = min(len(ready), len(multerlist))
            for i in range(lenth):
                multer = multerlist[i]
                MRS = ready[i]
                multer.op =  self.inst[MRS.inst].op
                multer.status = MRS.name
                multer.vj = MRS.vj
                multer.vk = MRS.vk
                if MRS.op == Config.OP_DIV and MRS.vk == 0:
                    MRS.remain = 1
                else:
                    MRS.remain = Config.TIME[multer.op]
                MRS.FU = multer.name

            n -= 1
