#!/usr/bin/env python3

import matplotlib.pyplot as plt
import PyNEC
from common import *

def vswr(z, z0):
    Gamma =  abs((z - z0) / (z + z0))
    return float((1 + Gamma) / (1 - Gamma))

nec = geometry()

system_impedance = 50
count = 100
start_freq = 13.8
stop_freq = 14.6
step_size = (stop_freq - start_freq) / count
ifrq_linear_step = 0
nec.fr_card(ifrq_linear_step, count, start_freq, step_size)
nec.xq_card(0) # execute simulation

freqs = []
vswrs = []
for idx in range(0, count):
    ipt = nec.get_input_parameters(idx)
    z = ipt.get_impedance()
    freqs.append(ipt.get_frequency() / 1000000)
    vswrs.append(vswr(z, system_impedance))

dpi = 80
plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
plt.plot(freqs, vswrs)
plt.title("SWR vs Frequency")
plt.xlabel("Frequency, MHz")
plt.ylabel("SWR")
plt.axis([start_freq, stop_freq, 1.0, 3.0])
plt.grid(True)
plt.savefig("invv-swr.png")
