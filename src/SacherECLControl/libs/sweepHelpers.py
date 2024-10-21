import numpy as np
from numpy import ndarray

def ramp(
        t: ndarray, 
        distance: float, 
        speed: float, 
        acceleration: float, 
        deceleration: float = None
        ) -> ndarray:
    if deceleration is None: 
        deceleration = acceleration
    assert acceleration > 0
    assert deceleration > 0

    distanceSign = np.sign(distance)
    absDistance = np.abs(distance)

    # Calculate distance covered during acceleration
    timeToSpeed = speed / acceleration
    distanceAcceleration = 0.5 * speed * timeToSpeed

    # Calculate distance covered during deceleration
    timeToBreak = speed / deceleration
    distanceDeceleration = 0.5 * speed * timeToBreak

    # Calculate distance covered during constant speed
    distanceAtSpeed = absDistance - distanceAcceleration - distanceDeceleration
    assert distanceAtSpeed >= 0 # TODO: if smaller than zero, sweep is incomplete and
    # no constant speed is possible -> calculate when to switch to deceleration
    timeAtSpeed = distanceAtSpeed / speed

    # Calculate total time
    totalTime = timeToSpeed + timeAtSpeed + timeToBreak

    # conform measured time array to expected sweep duration
    dt = t[-1] - t[0]
    assert dt > 0
    _t = (t - t[0]) * totalTime / dt

    # Create masks
    accMsk = _t  < timeToSpeed
    spdMsk = (_t >= timeToSpeed) & (_t < timeToSpeed + timeAtSpeed)
    decMsk = _t >= (timeToSpeed + timeAtSpeed)

    # Query time values
    netAccTimes = _t[accMsk]
    netDecTimes = _t[decMsk] - timeToSpeed - timeAtSpeed
    netAtSpeedTimes = _t[spdMsk] - timeToSpeed

    # Query distance values
    return distanceSign * np.r_[
        netAccTimes**2 / 2 * acceleration,
        distanceAcceleration + netAtSpeedTimes * speed,
        distanceAcceleration + distanceAtSpeed + speed * netDecTimes - 0.5 * deceleration * netDecTimes ** 2,
    ]
