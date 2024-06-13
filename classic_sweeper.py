from PyQt5.QtCore import QTimer
from rtlsdr import RtlSdr
import numpy as np
from Gui_ver1 import *
import sys

M = 10**6

# Inicjalizacja RTL-SDR
sdr = RtlSdr()
sdr.sample_rate = 2.048 * M
sdr.freq_correction = 60
sdr.gain = 30

# Zakresy częstotliwości
freqs = {0: [38*M, 43*M], 1: [100*M, 110*M], 2: [200*M, 220*M], 3: [430*M, 440*M], 4: [865*M, 870*M]}

# Funkcja sweep
def sweep(step):
    state = window.current_state
    powers = []
    start_freq = freqs[state][0]
    end_freq = freqs[state][1]

    for freq in range(start_freq, end_freq, step):
        sdr.center_freq = freq
        samples = sdr.read_samples(2048)
        Amax = np.max(np.abs(samples))
        p = 20 * np.log10(Amax)
        powers.append(p)
        QApplication.processEvents()

    window.update_led(max(powers), window.led_bar.min_db, window.led_bar.max_db)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    step = 1 * M

    def periodic_sweep():
        sweep(step)

    timer = QTimer()
    timer.timeout.connect(periodic_sweep)
    timer.start(100)

    sys.exit(app.exec_())
