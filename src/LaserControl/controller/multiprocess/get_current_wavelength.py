from controller.LaserCon import LaserCon


def _get_current_wavelength(con: LaserCon() = None) -> float:
    if con is None or not isinstance(con, LaserCon):
        raise ValueError("laco must be a LaserConn object")
    else:
        print(con.current_wavelength)
        return con.current_wavelength
