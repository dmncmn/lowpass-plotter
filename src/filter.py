
import numpy as np
from scipy import signal


class Filter:

    def __init__(self):
        self.f1 = 0.1
        self.f2 = 500
        self.f3 = 200
        self.f4 = 500

        self.order = 50
        self.nyquist = 2500

        self._plot_data = ()
        self.freqs = 0
        self._filter = 0
        self._window = 'blackman'
        self.tau = 0.0001

    @property
    def get_filter(self):
        return self._filter

    def apply_filter(self, data):
        b1, a1, b2, a2 = self._filter
        return signal.lfilter(b1+b2, a1+a2, data)

    @get_filter.setter
    # @lru_cache(maxsize=24)
    def get_filter(self, freqs: tuple):

        f1, f2, f3, f4 = self.freqs = freqs

        b1 = signal.firwin(self.order,
                           [f1, f2],
                           window=self._window,
                           width=0.001,
                           nyq=self.nyquist,
                           pass_zero=False)

        b2 = [self.tau]
        a2 = [self.tau, -self.tau]

        self._filter = b1, [1.0], b2, a2

    @property
    def plot_data(self) -> tuple:
        self.get_filter = (self.f1, self.f2, self.f3, self.f4)
        b1, a1, b2, a2 = self.get_filter
        bcom = b1 + b2

        w1, h1 = signal.freqz(b1, [1.0])
        wcom, hcom = signal.freqz(b1 + b2, a1 + a2)

        plot_data_1 = (self.nyquist / np.pi * w1, 20 * np.log10(np.abs(h1)))
        plot_data_2 = [], []
        plot_data_com = (self.nyquist / np.pi * wcom, 20 * np.log10(np.abs(hcom)))

        self._plot_data = (plot_data_1, plot_data_2, plot_data_com)

        return self._plot_data


class ControlFilter(Filter):

    @property
    def set_window(self):
        return self._window

    @set_window.setter
    def set_window(self, window):
        self._window = window

    @property
    def set_cutoff(self):
        return self.f2

    @set_cutoff.setter
    def set_cutoff(self, freq):
        self.f2 = freq

    @property
    def set_order(self):
        return self.order

    @set_order.setter
    def set_order(self, order):
        self.order = order
