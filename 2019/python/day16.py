
import itertools
import typing


class FFT:
    def __init__(self, input_signal: str, base_pattern: typing.List[int] = None):
        self.signal = self._convert_signal(input_signal)
        if base_pattern is None:
            self.base_pattern = [0, 1, 0, -1]
        else:
            self.base_pattern = base_pattern.copy()
        self.signal_len = len(self.signal)
        self.pattern_len = len(self.base_pattern)
        self.current_signal = self.signal.copy()

    @staticmethod
    def _convert_signal(signal: str):
        return [int(x) for x in signal]

    def __reset(self):
        self.current_signal = self.signal.copy()

    def make_iterator(self, pos):
        if pos <= 0:
            pos = 1
        n = 1
        while True:
            yield self.base_pattern[(n // pos) % 4]
            n += 1

    def compute_signal(self, signal: typing.List[int] = None):
        if signal is None:
            signal = self.current_signal
        signal_len = len(signal)
        self.current_signal = list(map(
            lambda z: abs(sum(z)) % 10,
            [map(lambda x, y: x * y, signal, self.make_iterator(p + 1)) for p in range(signal_len)])
        )


# Tests ----
a = FFT("12345678")
for i in range(4):
    a.compute_signal()
print(a.current_signal)

a = FFT("80871224585914546619083218645595")
for i in range(100):
    a.compute_signal()
print(a.current_signal[0:8])

a = FFT("19617804207202209144916044189917")
for i in range(100):
    a.compute_signal()
print(a.current_signal[0:8])

a = FFT("69317163492948606335995924319873")
for i in range(100):
    a.compute_signal()
print(a.current_signal[0:8])

with open("../data/data16.txt") as f:
    data = f.read().strip()

a = FFT(data)
for i in range(100):
    a.compute_signal()
print(a.current_signal[0:8])
