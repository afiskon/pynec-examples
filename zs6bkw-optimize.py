#!/usr/bin/env python3 -u
# vim: set ai et ts=4 sw=4:

import PyNEC
from math import pi, tan
from common import *

def vswr(z, z0 = 50):
    Gamma =  abs((z - z0) / (z + z0))
    return float((1 + Gamma) / (1 - Gamma))

def calc_impedance(length, angle, height, freq_mhz):
    nec = geometry(length, angle, height)
    ifrq_linear_step = 0
    nec.fr_card(ifrq_linear_step, 1, freq_mhz, 0)
    nec.xq_card(0) # execute simulation
    ipt = nec.get_input_parameters(0)
    return ipt.get_impedance()

def transform_impedance(zl, freq_mhz, el_len, z0):
    x = 2*pi*el_len / (300 / freq_mhz)
    return z0*(zl+1j*z0*tan(x))/(z0+1j*zl*tan(x))

# f_list = [3.540, 7.020, 10.115, 14.035, 18.080, 21.035, 24.900, 28.035] # cw
f_list = [3.65, 7.1, 10.115, 14.2, 18.080, 21.1, 24.900, 29.0] # ssb
# z0_list = ['25', '50', '75', '100', '150', '200', '250', '300', '400', '450']
z0_list = ['50']

# checked - there are no solutions below 310 Ohm
for line_z0 in range(310, 610, 10):
    print("--- z0 = {} ---".format(line_z0))
    for line_len_cm in range(1000, 1500, 10):
        line_len = line_len_cm / 100 # electrical length, without VF
        for len_cm in range(1000, 1500, 10):
            length = len_cm/100
            for angle in [100]: # inv-v
                # max_length = height/sin((90-angle/2)*pi/180) = 15.55
                for height_cm in [1000]:
                    height = height_cm / 100
                    good_bands = {}
                    swrs = {}
                    for freq in f_list:
                        zl = calc_impedance(length, angle, height, freq)
                        z = transform_impedance(zl, freq, line_len, line_z0)
                        for sys_z0 in z0_list:
                            if sys_z0 not in good_bands.keys():
                                good_bands[sys_z0] = []
                                swrs[sys_z0] = []
                            swr = round(vswr(z, int(sys_z0)), 1)
                            if swr < 2:
                                good_bands[sys_z0] += [freq]
                                swrs[sys_z0] += [swr]

                    for sys_z0 in z0_list:
                        if len(good_bands[sys_z0]) >= 3:
                            print("sys_z0 = {}, line_z0 = {}, line_el_len = {}, el_length = {}, height = {}, angle = {}, nbands = {}, good_bands = {}, swrs = {}, worse_swr = {}".format(sys_z0, line_z0, line_len, length, height, angle, len(good_bands[sys_z0]), good_bands[sys_z0], swrs[sys_z0], max(swrs[sys_z0])))
