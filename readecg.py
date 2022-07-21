import iir_filter
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = "happy.dat"
seq = np.loadtxt(filename)
time = seq[:,0]
volt = seq[:,3]
volt = volt - 2048
volt = volt * 2E-3 * 500 / 1000
# plt.plot(time, volt)
# plt.show()

plt.title('ECG')

f0 = 48.0
f1 = 52.0
fs = 1000.0

sos1 = signal.butter(6, [f0/fs*2, f1/fs*2], 'bandstop', output='sos')
f2 = 25.0
sos2 = signal.butter(6, f2/fs*2, output='sos')
f3 = 2.0
sos3 = signal.butter(6, f3/fs*2, 'highpass', output='sos')

iir1 = iir_filter.IIR_filter(sos1)
iir2 = iir_filter.IIR_filter(sos2)
iir3 = iir_filter.IIR_filter(sos3)

y2 = np.zeros(len(volt))
for i in range(len(volt)):
    y2[i] = iir1.filter(iir2.filter(iir3.filter(volt[i])))

time = (time[int(0.1*len(time)):])
y2 = (y2[int(0.1*len(y2)):])
plt.plot(time, y2)
plt.show()
