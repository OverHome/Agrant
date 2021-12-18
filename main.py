from MainWindow import *

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Profile()
    ex.show()
    sys.exit(app.exec_())
