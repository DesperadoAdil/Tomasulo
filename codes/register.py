# -*- coding: UTF-8 -*-

class Register():

    def __init__(self, id):
        self.name = 'F' + str(id)
        self.status = None
        self.value = 0

    def __repr__(self):
        return '%5r\tSTATUS: %5r\tVALUE: %5r' % (self.name, self.status, self.value)
