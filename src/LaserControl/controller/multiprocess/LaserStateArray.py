from ctypes import Structure, c_double, c_bool


class LaserStateArray(Structure):
    _fields_ = [
        ('connected', c_bool),
        ('moving', c_double),
        ('finished', c_bool),
        ('current_wavelength', c_double),
        ('velocity', c_double),
        ('acceleration', c_double),
        ('deceleration', c_double),
    ]