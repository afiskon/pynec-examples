#!/usr/bin/env python3

import matplotlib.pyplot as plt
import PyNEC
from common import *

nec = geometry()

freq_mhz = 14.035
ifrq_linear_step = 0
nec.fr_card(ifrq_linear_step, 1, freq_mhz, 0) 

azimuth = 0
nec.rp_card(calc_mode=0, n_theta=181, n_phi=1,
    output_format=1, normalization=0, D=0, A=0, # XNDA = 1000
    theta0=-90, phi0=azimuth, delta_theta=1, delta_phi=0, radial_distance=5000, gain_norm=0)
nec.xq_card(0) # execute simulation

rpt = nec.get_radiation_pattern(0)
gain = rpt.get_gain_tot()

gm = max(gain)
xs = [2*pi*float(90-theta)/360 for theta in range(gain.size)]
ys = [-36 if g-gm < -36 else g-gm for g in gain]

dpi = 80
fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
ax = plt.subplot(111, projection='polar')
ax.set_title('Azimuth {} deg'.format(azimuth))
ax.set_xlabel('Max gain: {:.2f} dBi'.format(gm))
ax.set_thetamin(-90) # set the limits
ax.set_thetamax(90)
ax.set_theta_offset(2*pi*90/360)
ax.plot(xs, ys, linestyle = 'solid', color='red')
ax.set_rmax(0)
ax.set_rticks([-6*i for i in range(0,7)])
ax.set_yticklabels([''] + [str(-6*i) for i in range(1,7)])
ax.set_thetagrids(range(-90, 91, 15))
ax.set_theta_direction(-1)
ax.grid(True)

fig.savefig('invv-azimuth.png')
