# -*- coding: UTF-8 -*-
from .config import Config

class Instruction():

    def __init__(self, content):
        self.content = content
        content = content.split(',')
        self.op = content[0]
        self.rs = None
        self.Issue = None
        self.ExecComp = None
        self.WriteResult = None
        self.rgst_int = []
        for arg in content[1:]:
            if arg.startswith('0x'):
                arg = int(arg, 16)
                if arg >= 2147493648:
                    arg = ~(0xFFFFFFFF ^ arg)
            self.rgst_int.append(arg)

    def __repr__(self):
        return '%40r\tIssue: %5r\tExec Comp: %5r\tWrite Result: %5r\tRS: %s' % (self.content, self.Issue, self.ExecComp, self.WriteResult, self.rs)

    def free(self):
        self.Issue = None
        self.ExecComp = None
        self.WriteResult = None
