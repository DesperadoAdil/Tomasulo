# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from PyQt5 import QtCore, QtGui, QtWidgets

from tomasulo.tomasulo import Tomasulo as TomasuloCore
from tomasulo.hardware import Add, Mult, Load
#from instruction import Instruction as InstructionWidget

class Tomasulo(QWidget):

    def __init__(self):
        super().__init__()
        self.reshape()
        self.initIcon()
        self.initToolTip()
        self.initButton()

        self.tomasulo = TomasuloCore()
        self.initData()
        self.inst = QTableWidget()
        self.inst.setRowCount(1000)
        self.inst.setColumnCount(4)
        self.inst.setHorizontalHeaderLabels(["指令", "发射周期", "执行完毕", "写回结果"])
        self.inst.verticalHeader().setVisible(False)
        self.inst.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.inst.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.inst.setSelectionMode(QAbstractItemView.SingleSelection)
        self.inst.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.inst.resizeColumnsToContents()
        self.inst.setShowGrid(False)
        self.initInst()

        buttonlayout = QVBoxLayout()
        buttonlayout.addWidget(self.stepbtn)
        buttonlayout.addWidget(self.stepsbtn)
        buttonlayout.addStretch()

        layout = QHBoxLayout(self)
        layout.addLayout(buttonlayout)
        layout.addWidget(self.inst)
        layout.addStretch()
        layout.setSpacing(20)

        self.show()

    def reshape(self):
        self.resize(1080, 900)
        self.setWindowTitle("Tomasulo")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initIcon(self):
        self.setWindowIcon(QIcon('static/icon.png'))

    def initToolTip(self):
        QToolTip.setFont(QFont('SansSerif', 10))

    def initButton(self):
        self.stepbtn = QPushButton("单步执行", self)
        self.stepbtn.setToolTip("执行一步!")
        self.stepbtn.clicked.connect(self.step)

        self.stepsbtn = QPushButton("多步执行", self)
        self.stepsbtn.setToolTip("执行多步!")
        self.stepsbtn.clicked.connect(self.stepsdialog)

    def initData(self):
        with open('static/test/test0.nel', encoding = 'utf8') as f:
            for line in f.readlines():
                self.tomasulo.insert_inst(line)

    def initInst(self):
        i = 0
        for inst in self.tomasulo.inst:
            content = QTableWidgetItem(inst.content)
            content.setToolTip(inst.content)
            self.inst.setItem(i, 0, content)
            Issue = QTableWidgetItem(str(inst.Issue) if inst.Issue else None)
            Issue.setTextAlignment(Qt.AlignHCenter)
            self.inst.setItem(i, 1, Issue)
            ExecComp = QTableWidgetItem(str(inst.ExecComp) if inst.ExecComp else None)
            ExecComp.setTextAlignment(Qt.AlignHCenter)
            self.inst.setItem(i, 2, ExecComp)
            WriteResult = QTableWidgetItem(str(inst.WriteResult) if inst.WriteResult else None)
            WriteResult.setTextAlignment(Qt.AlignHCenter)
            self.inst.setItem(i, 3, WriteResult)
            i += 1

    def step(self):
        self.tomasulo.step()
        #print (self.tomasulo)
        self.initInst()

    def steps(self, step):
        self.tomasulo.step(step)
        self.initInst()

    def stepsdialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("请输入执行步数 ")
        dialog.setWindowModality(Qt.ApplicationModal)
        line = QLineEdit(dialog)
        line.setAlignment(Qt.AlignLeft)
        line.setValidator(QIntValidator())
        line.setText('1')
        btn = QPushButton("确定", dialog)

        def btnclicked():
            self.steps(int(line.text()))
            dialog.close()
        btn.clicked.connect(btnclicked)

        layout = QHBoxLayout(dialog)
        layout.addWidget(line)
        layout.addWidget(btn)

        dialog.exec_()

    '''def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()'''


if __name__ == '__main__':
    if len(sys.argv) == 1:
        toma = TomasuloCore()
        with open('tomasulo/samp.txt', encoding = 'utf8') as f:
            for line in f.readlines():
                toma.insert_inst(line)
        print (toma)
        while True:
            for loader in Load.values():
                print (loader)
            for adder in Add.values():
                print (adder)
            for multer in Mult.values():
                print (multer)
            lin = input()
            if lin.lower() == "exit":
                break
            elif lin.lower() == "reset":
                toma.reset()
            else:
                toma.step(int(lin))
            print (toma)
    elif len(sys.argv) == 2 and sys.argv[1].lower() == 'gui':
        app = QApplication(sys.argv)
        w = Tomasulo()
        sys.exit(app.exec_())
    else:
        pass
