
import numpy as np
from typing import NoReturn

import scipy.signal
from src.filter import Filter


class Gen:

    def __init__(self):
        self.f1 = 0
        self._sin_data = (0, 0)
        self._sin_data_filtered = ([0], [0])

        self._square_data = (0, 0)
        self.nyq = 2500

        self.f = Filter()
        self.f.get_filter = (0.1, 300, 700, 900)

        self.sin_ = 500
        self.square_ = 100

        self.signal_filtered = 1

        self.freq = 100

    @property
    def sin_(self) -> tuple:
        return self._sin_data

    @sin_.setter
    def sin_(self, freq: float) -> NoReturn:
        t = 0.1
        fs = 2*self.nyq
        x = np.arange(t * fs) / fs
        y = np.sin(2 * np.pi * freq * x)
        self.freq = freq
        self._sin_data = x, y

    @property
    def signal_filtered(self):
        return self._sin_data_filtered

    @signal_filtered.setter
    def signal_filtered(self, val):
        if val == 'square':
            data = self.square_
        else:
            data = self.sin_

        self._sin_data_filtered = (data[0], self.f.apply_filter(data[1]))

    @property
    def square_(self) -> tuple:
        return self._square_data

    @square_.setter
    def square_(self, freq: float) -> NoReturn:
        t = 0.1
        fs = 2*self.nyq
        x = np.arange(t * fs) / fs
        y = scipy.signal.square(2 * np.pi * freq * x)
        self.freq = freq
        self._square_data = x, y
