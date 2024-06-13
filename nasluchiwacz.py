import random
from pylab import xlabel, ylabel, savefig, clf
import time

from rtlsdr import RtlSdr
import numpy as np
from Gui_nasluchiwacz import *
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

M = 10**6
N = 4*1024

sdr = RtlSdr()
sdr.sample_rate = 2.048 * M
sdr.gain = 30

freqs = {0: [38*M, 43*M], 1: [100*M, 110*M], 2: [200*M, 220*M], 3: [430*M, 440*M], 4: [865*M, 870*M]}

dates = [datetime.now()]
states = list(freqs.keys())
counter = len(states)

img_num = 0


def take_img(number,freq,f_space,PSD):
    clf()
    plt.plot(f_space+freq/M, PSD)
    plt.plot(f_space[np.argmax(PSD)]+freq/M,np.max(PSD),'rx')
    plt.grid()
    xlabel('Frequency (MHz)')
    ylabel('Relative power (dB)')
    name = f"plots/img_{number}.png"
    savefig(name)


def sweep(step):
    global img_num, states, counter

    if counter == 0:
        states = list(freqs.keys())
        counter = len(states)

    state = random.choice(states)
    start_freq = freqs[state][0]
    end_freq = freqs[state][1]
    f_space = np.linspace(sdr.sample_rate/-2, sdr.sample_rate/2,N)/1e6
    
    for freq in range(start_freq, end_freq, step):
        sdr.center_freq = freq
        samples = sdr.read_samples(N)
        samples = samples * np.hamming(N)
        S = np.fft.fftshift(np.fft.fft(samples))
        psd = np.abs(S)**2 / len(samples)
        PSD = 10*np.log10(psd)
        PSD_MAX = np.max(PSD)
        
        freq_max = f_space[np.argmax(PSD)]

        if PSD_MAX >= 20:
            dates.append(datetime.now())
            if dates[-1] - dates[-2] > timedelta(seconds=2):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                img_num = img_num + 1
                with open("detected_freq.txt", "a") as f:
                    f.write(f"Detected Pmax frequency: {freq/M+freq_max:.2f} MHz, Power: {PSD_MAX:.2f} dBm, Date: {current_time}, img_num = {img_num}\n")
                take_img(img_num, freq, f_space, PSD)
                time.sleep(1)
            del dates[:-1]

    states.remove(state)
    counter -= 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    step = 1 * M

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("detected_freq.txt", "a") as f:
        f.write(f"\n========Starting detection, date: {start_time}==============\n")

    def periodic_sweep():
        sweep(step)

    timer = QTimer()
    timer.timeout.connect(periodic_sweep)
    timer.start(100)

    sys.exit(app.exec_())
