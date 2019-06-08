# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont

class Instruction(QWidget):

    def __init__(self, inst=None):
        super().__init__()
        self.inst = inst
        if inst:
            self.content = QLabel(inst.content, self)
            self.Issue = QLabel(str(inst.Issue) if inst.Issue else None, self)
            self.ExecComp = QLabel(str(inst.ExecComp) if inst.ExecComp else None, self)
            self.WriteResult = QLabel(str(inst.WriteResult) if inst.WriteResult else None, self)
        else:
            self.content = QLabel('指令', self)
            self.Issue = QLabel('发射周期', self)
            self.ExecComp = QLabel('执行完毕', self)
            self.WriteResult = QLabel('写回结果', self)

        layout = QHBoxLayout()
        layout.addWidget(self.content)
        layout.addStretch()
        layout.addWidget(self.Issue)
        layout.addStretch()
        layout.addWidget(self.ExecComp)
        layout.addStretch()
        layout.addWidget(self.WriteResult)
        layout.setSpacing(20)

        self.setLayout(layout)
