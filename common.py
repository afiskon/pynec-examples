import PyNEC
from math import pi, sin

def free_space(nec):
    #  0 - no ground plane
    #  1 - ground plane with current expansion
    # -1 - ground plane without current expansion
    nec.geometry_complete(0)

def good_ground(nec):
    conductivity = 0.0303 # S/m
    rel_dielectric_constant = 20.0
    nec.geometry_complete(1)
    nec.gn_card(0, 0, rel_dielectric_constant, conductivity, 0, 0, 0, 0)

def average_ground(nec):
    conductivity = 0.005 # S/m
    rel_dielectric_constant = 13.0
    nec.geometry_complete(1)
    nec.gn_card(0, 0, rel_dielectric_constant, conductivity, 0, 0, 0, 0)

def poor_ground(nec):
    conductivity = 0.001 # S/m
    rel_dielectric_constant = 3.0
    nec.geometry_complete(1)
    nec.gn_card(0, 0, rel_dielectric_constant, conductivity, 0, 0, 0, 0)

def geometry(length=5.22, angle=100, height=10, nr_segments=21,
        ground=average_ground):
    nec = PyNEC.nec_context()
    nec.set_extended_thin_wire_kernel(False)

    wire_radius = 0.0005 # 0.5 mm
    length_ratio = 1.0
    radius_ratio = 1.0

    eps = 0.1
    b = length*sin(pi*angle/2/180)
    a = length*sin(pi*(90 - angle/2)/180)

    geo = nec.get_geometry()
    # center
    geo.wire(1, 1, 0, -eps, height, 0, eps, height,
             wire_radius, length_ratio, radius_ratio)
    # left
    geo.wire(2, nr_segments, 0, -b, height-a, 0, -eps, height,
             wire_radius, length_ratio, radius_ratio)
    # right
    geo.wire(3, nr_segments, 0, b, height-a, 0, eps, height,
             wire_radius, length_ratio, radius_ratio)

    ground(nec)

    # voltage excitation in the center of the antenna
    segment_nr = 1
    voltage = 1.0+0j
    ex_voltage_excitation = 0
    nec.ex_card(ex_voltage_excitation, segment_nr, 1, 1,
                voltage.real, voltage.imag, 0, 0, 0, 0)
    return nec
