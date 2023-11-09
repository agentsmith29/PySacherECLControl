import LaserLib as s
s.__doc__
from LaserLib import *

o=laserSacher()
o.connectMotor("USB0")

current_wavelength= o.getCurrentWavelength()
vel = o.getVelocity()
o.setVelocity(2.0)
acc = o.getAcceleration()
o.setAcceleration(2.0)
print(">>>>>>>>>>>>>>>>>>>> Current Wavelength is:", current_wavelength)
print(">>>>>>>>>>>>>>>>>>>> vel:", vel)
print(">>>>>>>>>>>>>>>>>>>> acc:", acc)

target_wavelength = float(input(">>>>>>>>>>>>>>>>>>>> Enter Target Wavelength in nm: "))
o.goToWvl(target_wavelength, False)
o.closeMotorConnection()
