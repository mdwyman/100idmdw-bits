"""
JJ-Xray Transfocators

Device uses PyDevice for focal size calculation and lens configuration control
"""

#TODO how to adapt for new BITS format and devices.yml?

from ophyd import Component as Cpt
from ophyd import FormattedComponent as FCpt
from ophyd import Device
from ophyd import EpicsSignal, EpicsSignalRO
from ophyd import EpicsMotor
from ophyd import PVPositioner


class fpower_index(PVPositioner):
    """
    focal power index "positioner"; increasing index, increasing focal power
    """
    readback = Cpt(EpicsSignalRO, '1:sortedIndex_RBV')
    setpoint = Cpt(EpicsSignal, '1:sortedInde')
    done = Cpt(EpicsSignalRO, 'sysBusy')

class focal_size(PVPositioner):
    """
    focal size positioner
    """
    readback = Cpt(EpicsSignalRO, 'fSize_actual')
    setpoint = Cpt(EpicsSignal, 'focalSize')
    done = Cpt(EpicsSignalRO, 'sysBusy')

class JJtransfocator(Device):

    focalPower = FCpt(fpower_index, "{prefix}")
    focalSize = FCpt(focal_size, "{prefix}")
#    fpower_index = Cpt(EpicsSignal, "1:sortedIndex", kind="hinted")
#    fpower_index_readback = Cpt(EpicsSignalRO, "1:sortedIndex_RBV", kind="hinted")
#    fsize_set = Cpt(EpicsSignal, "focalSize", kind="hinted")
#    fsize_readback = Cpt(EpicsSignalRO, "focalSize_actual", kind="hinted")

    q = Cpt(EpicsSignalRO, "q", kind="hinted")
    dq = Cpt(EpicsSignalRO, "dq", kind="hinted")
    sam_position_readback = Cpt(EpicsSignalRO, "samplePosition_RBV", kind="hinted")
    sam_position_offset_readback = Cpt(EpicsSignalRO, "samplePositionOffset_RBV", kind="hinted")

    energy_keV_local = Cpt(EpicsSignal, "EnergyLocal", kind="config")
    energy_keV_mono = Cpt(EpicsSignalRO, "EnergyBeamline", kind="config")
    energy_keV_lookup = Cpt(EpicsSignalRO, "energy_rbv", kind="hinted")
    
    beamMode = Cpt(EpicsSignal, "beamMode", string=True, kind="config")
    energyMode = Cpt(EpicsSignal, "energySelect", string=True, kind="config")

    
class JJtransfocator1x(JJtransfocator):
    '''
    Handles single transfocator system
    
    '''
    def __init__(
        self,
        prefix: str,
        pitch1_motor: str,
        yaw1_motor: str,
        x1_motor: str,
        y1_motor: str,
        z1_motor: str = '',
        *args,
        **kwargs,
    ):

        self._pitch1_motor = pitch1_motor
        self._yaw1_motor = yaw1_motor
        self._x1_motor = z1_motor
        self._y1_motor = y1_motor
        self._z1_motor = z1_motor

        super().__init__(prefix, *args, **kwargs)

    binary_crl1_config = Cpt(EpicsSignalRO, "1:lenses", kind="hinted")
    bw_crl1_config = Cpt(EpicsSignalRO, "1:lensConfig_BW")
    rbv_crl1_config = Cpt(EpicsSignalRO, "1:lensConfig_RBV", kind="hinted")

    crl1_z_pos = Cpt(EpicsSignalRO, "1:oePositionOffset_RBV")

    interLensDelay1 = Cpt(EpicsSignal, "1:interLensDelay", kind="config")
    
    pitch1 = FCpt(EpicsMotor, "{_pitch1_motor}", labels={"motors"})
    yaw1 = FCpt(EpicsMotor, "{_yaw1_motor}", labels={"motors"})
    x1 = FCpt(EpicsMotor, "{_x1_motor}", labels={"motors"})
    y1 = FCpt(EpicsMotor, "{_y1_motor}", labels={"motors"})
    
class JJtransfocator2x(JJtransfocator1x):
    
    '''
    Adds a second transfocator to beamline
    
    '''
    
    def __init__(
        self,
        prefix: str,
        pitch2_motor: str,
        yaw2_motor: str,
        x2_motor: str,
        y2_motor: str,
        z2_motor: str = '',
        *args,
        **kwargs,
    ):

        self._pitch2_motor = pitch2_motor
        self._yaw2_motor = yaw2_motor
        self._x2_motor = z2_motor
        self._y2_motor = y2_motor
        self._z2_motor = z2_motor

        super().__init__(prefix, *args, **kwargs)
    
    binary_crl2_config = Cpt(EpicsSignalRO, "2:lenses", kind="hinted")
    bw_crl2_config = Cpt(EpicsSignalRO, "2:lensConfig_BW")
    rbv_crl2_config = Cpt(EpicsSignalRO, "2:lensConfig_RBV", kind="hinted")

    crl2_z_pos = Cpt(EpicsSignalRO, "2:oePositionOffset_RBV")

    interLensDelay2 = Cpt(EpicsSignal, "2:interLensDelay", kind="config")

    pitch2 = FCpt(EpicsMotor, "{_pitch2_motor}", labels={"motors"})
    yaw2 = FCpt(EpicsMotor, "{_yaw2_motor}", labels={"motors"})
    x2 = FCpt(EpicsMotor, "{_x2_motor}", labels={"motors"})
    y2 = FCpt(EpicsMotor, "{_y2_motor}", labels={"motors"})
    
class JJtransfocator1xZ(JJtransfocator1x):
    
    def __init__(
        self,
        prefix: str,
        z1_motor: str,
        *args,
        **kwargs,
    ):

        self._z1_motor = z1_motor

        super().__init__(prefix, *args, **kwargs)
        
    z1 = FCpt(EpicsMotor, "{_z1_motor}", labels={"motors"})

class JJtransfocator2xZ(JJtransfocator2x):
    
    def __init__(
        self,
        prefix: str,
        z2_motor: str,
        *args,
        **kwargs,
    ):

        self._z2_motor = z2_motor

        super().__init__(prefix, *args, **kwargs)
        
    z2 = FCpt(EpicsMotor, "{_z2_motor}", labels={"motors"})
