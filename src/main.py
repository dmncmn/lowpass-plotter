
import sys
from PyQt5 import QtWidgets
from src.plot import Plot


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    plot = Plot()
    plot.plot_pyqt()
    sys.exit(app.exec_())
