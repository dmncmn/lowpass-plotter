
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import numpy as np
from time import time

import src.front as front
from src.gen import Gen


class Common:

    @staticmethod
    def get_time(func):
        def wrapper(*args, **kwargs):
            before = time()
            func(*args, **kwargs)
            # print(f'{func.__name__}: {round(time()-before, 4)}s.')
        return wrapper


class Plot(front.UiMainWindow):

    def __init__(self):
        super().__init__()
        self.init_widgets()

        self.response_plot = self.filter_view
        self.response_plot.showGrid(True, True)
        self.response_plot.setXRange(0, 2500, padding=0)
        self.response_plot.setYRange(-70, 20, padding=0)
        self.response_plot.setLabel('left', 'Amplitude (dB)')
        self.response_plot.setLabel('bottom', 'Frequency (Hz)')

        self.time_plot = self.signal_view
        self.time_plot.showGrid(True, True)
        self.time_plot.setXRange(0.01, 0.1, padding=0)
        self.time_plot.setYRange(-2, 2, padding=0)
        self.time_plot.setLabel('left', 'Amplitude (V)')
        self.time_plot.setLabel('bottom', 'Time (s)')

        self.gen = Gen()
        self.filt = self.gen.f
        self.plot_data_1, self.plot_data_2, self.plot_data_3 = self.filt.plot_data

        self.iter_sin_x = self.iter_by_step([])
        self.iter_sin_y = self.iter_by_step([])

        self.__prev_freq_val = 0
        self.__prev_order_val = 0
        self.__prev_cut_val = 0
        self.__prev_tau_val = 0

        self.timer_response_plot = pg.QtCore.QTimer()
        self.timer_sin_plot = pg.QtCore.QTimer()

    @staticmethod
    def iter_by_step(data, step=100):
        for i in range(0, len(data), step):
            yield data[i: i+step]

    def plot_pyqt(self):

        self.response_curve_tau = self.response_plot.plot(clear=False, pen=pg.mkPen('b', width=2))
        self.response_curve_no_tau = self.response_plot.plot(clear=False, pen=pg.mkPen('r', width=2))
        self.current_freq_curve = self.response_plot.plot(clear=False, pen=pg.mkPen('w', width=2))
        self.sin_curve = self.time_plot.plot(clear=False, pen=pg.mkPen('g', width=2))

        self.timer_response_plot.timeout.connect(self.update_response_plot)
        self.timer_response_plot.start(25)
        self.timer_sin_plot.timeout.connect(self.update_sin_plot)
        self.timer_sin_plot.start(25)

        self.show()
        QtGui.QApplication.instance().exec_()

    @Common.get_time
    def update_response_plot(self):

        if (self.order_setter_value,
            self.cut_setter_value,
            self.tau_setter_value) != (self.__prev_order_val,
                                       self.__prev_cut_val,
                                       self.__prev_tau_val):

            self.filt.order = self.order_setter_value
            self.filt.f2 = self.cut_setter_value
            self.filt.tau = self.tau_setter_value

            self.plot_data_1, self.plot_data_2, self.plot_data_3 = self.filt.plot_data

            self.response_curve_no_tau.setData(*self.plot_data_1)
            self.response_curve_tau.setData(*self.plot_data_3)

            self.__prev_order_val = self.order_setter_value
            self.__prev_cut_val = self.cut_setter_value
            self.__prev_tau_val = self.tau_setter_value

    @Common.get_time
    def update_sin_plot(self):

        if self.freq_setter_value != self.__prev_freq_val:

            self.gen.sin_ = self.freq_setter_value
            self.gen.signal_filtered = 'sin'
            self.set_freq_text = self.gen.freq

            x, y = self.gen.signal_filtered
            self.current_amp_text = np.max(y[:-50])
            self.sin_curve.setData(x, y)
            self.current_freq_curve.setData([self.gen.freq, self.gen.freq], [-70, 20])
            self.__prev_freq_val = self.freq_setter_value
