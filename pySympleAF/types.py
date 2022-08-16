from enum import IntFlag, IntEnum

class SAFCommand(IntFlag):
    UPDATE_SET_POSITION = (1 << 8)
    TOGGLE_HOME_DIRECTION_POSITIVE = (1 << 7)
    TOGGLE_HOME_DIRECTION_NEGATIVE = (1 << 6)
    TRIGGER_HOMEING = (1 << 5)
    ENABLE_STALL_DETECTION = (1 << 4)
    SAVE_STATE_TO_FLASH = (1 << 3)
    HALT_MOTOR = (1 << 2)
    ZERO_CURRENT_POSITION = ( 1 << 1)
    TOGGLE_INVERT_STEP_DIRECTION = ( 1 << 0 )

class SAFStatus(IntFlag):
    STEPPER_DRIVER_ENABLED = (1 << 8)
    STEPPER_DRIVER_COMM_ERROR = (1 << 7)
    STEPPER_DRIVER_ERROR = (1 << 6)
    HOME_DIRECTION_POSITIVE = (1 << 5)
    HOME_DIRECTION_NEGATIVE = (1 << 4)
    IS_HOMING = (1 << 3)
    IS_STALLED = (1 << 2)
    IS_MOVING = (1 << 1)
    INVERT_STEP_DIRECTION = (1 << 0)

class DriverStatus(IntFlag):
    MOTOR_STOPPED = (1 << 31)
    S2VSB = (1 << 15)
    S2VSA = (1 << 14)
    S2GB = (1 << 13)
    S2GA = (1 << 12)
    OVERTEMP_ERROR = (1 << 11)
    OVERTEMP_WARNING = (1 << 10)

class SAFMicrocontrollerType(IntEnum):
    STM32 = 0

class SAFDriverType(IntEnum):
    TMC2209 = 1