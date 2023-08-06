from PyQt5.QtWidgets import QApplication, QButtonGroup
import sys
from qtawesome import icon
from swqt import ShockwaveWidget, InputLineEdit, FuncButton, FuncButtonGroup


class Main(ShockwaveWidget):
    def __init__(self):
        super(Main, self).__init__()
        # a = InputLineEdit(self, icon_name='fa5s.camera', placeholder='adss')
        self.g = FuncButtonGroup(self)

        self.a = FuncButton(self.g, icon('fa.times', color='azure'), 'a', self)
        self.b = FuncButton(self.g, icon('fa.times', color='azure'), 'b', self)
        self.c = FuncButton(self.g, icon('fa.times', color='azure'), 'C', self)
        self.d = FuncButton(self.g, icon('fa.times', color='azure'), 'D', self)

        self.g.addButtons([self.a, self.b, self.c, self.d])

        self.a.setGeometry(0, 0, 50, 50)
        self.b.setGeometry(0, 50, 50, 50)
        self.c.setGeometry(0, 100, 50, 50)
        self.d.setGeometry(0, 150, 50, 50)



app = QApplication(sys.argv)
m = Main()
m.show()
sys.exit(app.exec_())
