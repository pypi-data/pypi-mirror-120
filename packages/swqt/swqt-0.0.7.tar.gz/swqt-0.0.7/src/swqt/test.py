from PyQt5.QtWidgets import QApplication
import sys
from swqt import ShockwaveWidget, InputLineEdit


class Main(ShockwaveWidget):
    def __init__(self):
        super(Main, self).__init__()
        a = InputLineEdit(self, icon_name='fa5s.camera', placeholder='adss')


app = QApplication(sys.argv)
m = Main()
m.show()
sys.exit(app.exec_())
