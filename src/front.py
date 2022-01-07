
from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtCore, QtWidgets
from collections import deque


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._freq_text = ''
        self._signal_freq = 10
        self.__tau = 1/1000000.0
        self.__cut = 10
        self.__order = 5
        self.__current_amp = 1.0

        self.__signal_type = 'sin'
        self.signals = deque(['square', 'sin'])

        self.central_widget = QtWidgets.QWidget()
        self.filter_view = PlotWidget()
        self.signal_view = PlotWidget()
        self.current_freq = QtWidgets.QLabel()
        self.freq_setter = QtWidgets.QDial()
        self.tau_setter = QtWidgets.QDial()
        self.current_tau = QtWidgets.QLabel()
        self.cut_setter = QtWidgets.QDial()
        self.current_cut = QtWidgets.QLabel()
        self.order_setter = QtWidgets.QDial()
        self.current_order = QtWidgets.QLabel()
        self.current_amp = QtWidgets.QLabel()

    def init_widgets(self):

        width, height, span = 1024, 690, 10
        self.resize(width, height)
        self.setStyleSheet("QMainWindow {background: '#1f1f1f';}")
        self.setWindowTitle('Filter');

        self.central_widget.setParent(self)
        self.setCentralWidget(self.central_widget)

        self.filter_view.setParent(self.central_widget)
        self.filter_view.setGeometry(QtCore.QRect(span, span, 700, 340))
        self.filter_view.setBackground("1f1f1f")

        self.signal_view.setParent(self.central_widget)
        self.signal_view.setGeometry(QtCore.QRect(span, 340+span, 700, 340))
        self.signal_view.setBackground("1f1f1f")

        self.tau_setter.setParent(self.central_widget)
        self.tau_setter.setRange(1, 500000)
        self.tau_setter.setSingleStep(5)
        self.tau_setter.setGeometry(QtCore.QRect(span+700+span, span, 100, 100))
        self.tau_setter.setStyleSheet(
            "background-color: #F0F8FF;"
        )
        self.tau_setter.valueChanged.connect(self.__tau_setter)

        self.current_tau.setParent(self.central_widget)
        self.current_tau.setGeometry(QtCore.QRect(span+700+span+100+span, span, 300, 100))
        self.current_tau.setText(f"tau\n{round(self.__tau, 4)}")
        self.current_tau.setStyleSheet(
            "font-size: 50px; color: #F0F8FF;"
        )

        self.cut_setter.setParent(self.central_widget)
        self.cut_setter.setRange(10, 2000)
        self.cut_setter.setSingleStep(1)
        self.cut_setter.setGeometry(QtCore.QRect(span+700+span, span+100+span, 100, 100))
        self.cut_setter.setStyleSheet(
            "background-color: #FFFACD;"
        )
        self.cut_setter.valueChanged.connect(self.__cut_setter)

        self.current_cut.setParent(self.central_widget)
        self.current_cut.setGeometry(QtCore.QRect(span+700+span+100+span, span+100+span, 300, 100))
        self.current_cut.setText(f"fc\n{self.__cut} Hz")
        self.current_cut.setStyleSheet(
            "font-size: 50px; color: #FFFACD;"
        )

        self.order_setter.setParent(self.central_widget)
        self.order_setter.setRange(5, 100)
        self.order_setter.setSingleStep(1)
        self.order_setter.setGeometry(QtCore.QRect(span+700+span, span+100+span+100+span, 100, 100))
        self.order_setter.setStyleSheet(
            "background-color: #FFFACD;"
        )
        self.order_setter.valueChanged.connect(self.__order_setter)

        self.current_order.setParent(self.central_widget)
        self.current_order.setGeometry(QtCore.QRect(span+700+span+100+span, span+100+span+100+span, 300, 100))
        self.current_order.setText(f"N\n{self.__order}")
        self.current_order.setStyleSheet(
            "font-size: 50px; color: #FFFACD;"
        )

        self.freq_setter.setParent(self.central_widget)
        self.freq_setter.setRange(1, 2000)
        self.freq_setter.setSingleStep(1)
        self.freq_setter.setGeometry(QtCore.QRect(span+700+span, 340+span, 100, 100))
        self.freq_setter.setStyleSheet(
            "background-color: #F0FFF0;"
        )
        self.freq_setter.valueChanged.connect(self.__freq_setter)

        self.current_freq.setParent(self.central_widget)
        self.current_freq.setGeometry(QtCore.QRect(span+700+span+100+span, 340+span, 300, 100))
        self.current_freq.setStyleSheet(
            "font-size: 50px; color: #F0FFF0;"
        )

        self.current_amp.setParent(self.central_widget)
        self.current_amp.setGeometry(QtCore.QRect(span+700+span+100+span, 340+span+100+span, 300, 100))
        self.current_amp.setText(f"Umax\n{self.__current_amp} V")
        self.current_amp.setStyleSheet(
            "font-size: 50px; color: #F0FFF0;"
        )

    @property
    def freq_setter_value(self):
        return self._signal_freq

    @freq_setter_value.setter
    def freq_setter_value(self, val):
        self.__freq_setter(val)

    def __freq_setter(self, val):
        self._signal_freq = val

    @property
    def freq_setter_signal(self):
        return self.__signal_type

    def __tau_setter(self, val):
        self.__tau = val / 1000000.0
        self.current_tau.setText(f'tau\n{round(self.__tau,4)}')

    @property
    def tau_setter_value(self):
        return self.__tau

    @tau_setter_value.setter
    def tau_setter_value(self, val):
        self._tau_setter(val)

    def __cut_setter(self, val):
        self.__cut = val
        self.current_cut.setText(f'fc\n{self.__cut} Hz')

    @property
    def cut_setter_value(self):
        return self.__cut

    @cut_setter_value.setter
    def cut_setter_value(self, val):
        self.__cut_setter(f'{val} Hz')

    def __order_setter(self, val):
        self.__order = val
        self.current_order.setText(f"N\n{self.__order}")

    @property
    def order_setter_value(self):
        return self.__order

    @order_setter_value.setter
    def order_setter_value(self, val):
        self.__order_setter(val)

    @property
    def set_freq_text(self):
        return self._freq_text

    @set_freq_text.setter
    def set_freq_text(self, val):
        self._freq_text = f'f\n{val} Hz'
        self.current_freq.setText(self._freq_text)

    @property
    def current_amp_text(self):
        return self.__current_amp

    @current_amp_text.setter
    def current_amp_text(self, val):
        self.__current_amp = val
        self.current_amp.setText(f"Umax\n{round(self.__current_amp, 3)} V")
