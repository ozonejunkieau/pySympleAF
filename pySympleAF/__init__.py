from math import sqrt

from .exceptions import *
from .types import *

SAF_COMMAND = 0x1
SAF_STATUS = 0x2
SAF_CURRENT_POSITION = 0x3
SAF_SET_POSITION = 0x4
SAF_MAX_POSITION = 0x5
SAF_STEP_TIME_US = 0x6
SAF_DRIVER_CONFIG = 0x7
SAF_DRIVER_STATUS = 0x8
SAF_FIRMWARE_COMMIT_ID = 0x3FFFFFF9
SAF_DRIVER_TYPE = 0x3FFFFFFA
SAF_MCU_TYPE = 0x3FFFFFFB
SAF_FIRMWARE_STATE = 0x3FFFFFFC
SAF_GUID_1 = 0x3FFFFFFD
SAF_GUID_2 = 0x3FFFFFFE
SAF_GUID_3 =0x3FFFFFFF

SAF_INVALID_PACKET = 0xFFFFFFFF & 0x7FFFFFFF

SAF_VID = 0x0038
SAF_PID = 0x004e

SAF_PACKET_BYTES = 8
SAF_ENDIAN = "little"

TMC2209_V_FS = 0.325
TMC2209_DEFAULT_VREF = 2.5
SAF_TMC2209_RSENSE = 0.33

class SympleAutoFocus:
    def __init__(self, serial: str, r_sense: float = SAF_TMC2209_RSENSE, v_ref: float = TMC2209_DEFAULT_VREF ):

        self.serial: str = serial

        self._guid: int = 0
        self._guid_valid: int = 0

        self.v_ref: float = v_ref
        self.r_sense: float = r_sense
        self.increase_sensing_range: bool = False
        self.use_v_ref: bool = True

        self._driver_status: DriverStatus | None = None
        self._status: SAFStatus | None = None
        self._command_status: SAFCommand | None = None

        self._step_time_us: int | None = None

        self._current_position: int | None = None
        self._max_position: int | None = None
        self._target_position: int | None = None

        self._driver_type: SAFDriverType | None = None
        self._microcontroller_type: SAFMicrocontrollerType | None = None

        self._hold_current_bits: int | None = None
        self._run_current_bits: int | None = None

        self._stall_threshold_bits: int | None = None

        self._current_actual_bits: int | None = None
        self._stall_actual_bits: int | None = None

        self._commit: str | None = None

    @property
    def commit(self) -> int:
        if self._commit is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._commit

    @commit.setter
    def commit(self, commit) -> None:
        self._commit = commit

    @property
    def current_actual_bits(self) -> int:
        if self._current_actual_bits is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._current_actual_bits

    @current_actual_bits.setter
    def current_actual_bits(self, bits) -> None:
        self._current_actual_bits = bits


    @property
    def stall_actual_bits(self) -> int:
        if self._stall_actual_bits is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._stall_actual_bits

    @stall_actual_bits.setter
    def stall_actual_bits(self, bits) -> None:
        self._stall_actual_bits = bits


    @property
    def microcontroller_type(self) -> int:
        if self._microcontroller_type is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._microcontroller_type

    @microcontroller_type.setter
    def microcontroller_type(self, microcontroller_type) -> None:
        self._microcontroller_type = microcontroller_type

    @property
    def driver_type(self) -> int:
        if self._driver_type is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._driver_type

    @driver_type.setter
    def driver_type(self, driver_type) -> None:
        self._driver_type = driver_type

    @property
    def step_time_us(self) -> int:
        if self._step_time_us is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._step_time_us

    @step_time_us.setter
    def step_time_us(self, step_t) -> None:
        self._step_time_us = step_t


    @property
    def current_position(self) -> int:
        if self._current_position is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._current_position

    @current_position.setter
    def current_position(self, curr_pos) -> None:
        self._current_position = curr_pos

    @property
    def max_position(self) -> int:
        if self._max_position is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._max_position

    @max_position.setter
    def max_position(self, max_pos) -> None:
        self._max_position = max_pos

    @property
    def target_position(self) -> int:
        if self._target_position is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._target_position

    @target_position.setter
    def target_position(self, target_pos) -> None:
        self._target_position = target_pos



    @property
    def hold_current_amps(self) -> int:
        if self._hold_current_bits is None:
            raise SympleAFUninitialisedValue()
        else:
            return self.bits_to_current(self._hold_current_bits)

    @property
    def run_current_amps(self) -> int:
        if self._run_current_bits is None:
            raise SympleAFUninitialisedValue()
        else:
            return self.bits_to_current(self._run_current_bits)

    @property
    def stall_threshold(self) -> int:
        if self._stall_threshold_bits is None:
            raise SympleAFUninitialisedValue()
        else:
            return self._stall_threshold_bits

    def set_current_configuration(self, hold_current: int, run_current: int, stall_threshold: int):
        self._hold_current_bits = hold_current
        self._run_current_bits = run_current
        self._stall_threshold_bits = stall_threshold

    @property
    def v_fs(self) -> float:
        if self.use_v_ref:
            return TMC2209_V_FS * self.v_ref / TMC2209_DEFAULT_VREF
        else:
            return TMC2209_V_FS

    @property
    def i_max(self) -> float:
        return self.bits_to_current(0x1f)

    @property
    def i_min(self) -> float:
        return self.bits_to_current(0x00)

    def bits_to_current(self, in_bits: int) -> float:
        in_bits = in_bits & 0x1f

        i = (in_bits+1)/32 * (self.v_fs/self.r_sense+0.02)*1/sqrt(2)

        return i

    def current_to_bits(self, desired_current_amps: float) -> int:
        if desired_current_amps < 0:
            raise ValueError(f"Invalid current value: {desired_current_amps}")
        if desired_current_amps > self.i_max:
            return 0x1f

        bits = desired_current_amps /  ((self.v_fs/self.r_sense+0.02)*1/sqrt(2)) * 32 - 1
        bits = bits & 0x1f

        return bits

    def set_guid1(self, in_guid: int) -> None:
        self._guid = self._guid | in_guid
        self._guid_valid = self._guid_valid | (1 << 0)

    def set_guid2(self, in_guid: int) -> None:
        self._guid = self._guid | (in_guid << 32)
        self._guid_valid = self._guid_valid | (1 << 1)

    def set_guid3(self, in_guid: int) -> None:
        self._guid = self._guid | (in_guid << 64)
        self._guid_valid = self._guid_valid | (1 << 2)

    @property
    def guid(self) -> int:
        if self._guid_valid != 0b111:
            raise SympleAFUninitialisedValue()
        else:
            return self._guid

    def set_status(self, in_status: SAFStatus) -> None:
        self._status = in_status

    @property
    def status(self) -> SAFStatus:
        if self._status is None:
            raise SympleAFUninitialisedValue
        else:
            return self._status

    def set_driver_status(self, in_driver_status: DriverStatus) -> None:
        self._driver_status = in_driver_status

    @property
    def driver_status(self) -> DriverStatus:
        if self._driver_status is None:
            raise SympleAFUninitialisedValue
        else:
            return self._driver_status

    def set_command_status(self, in_command_status: SAFCommand) -> None:
        self._command_status = in_command_status

    @property
    def command_status(self) -> DriverStatus:
        if self._command_status is None:
            raise SympleAFUninitialisedValue
        else:
            return self._command_status


    def handle_packet(self, packet) -> None:

        this_packet_int = int.from_bytes(packet, byteorder=SAF_ENDIAN, signed=False)
        this_packet_type = this_packet_int & 0x7FFFFFFF
        this_packet_data = (this_packet_int >> 32) & 0xFFFFFFFF

        if this_packet_type ==  SAF_COMMAND:
            self.set_command_status(SAFCommand(this_packet_data))
        elif this_packet_type == SAF_STATUS:
            self.set_status(SAFStatus(this_packet_data))
        elif this_packet_type == SAF_CURRENT_POSITION:
            self.current_position = this_packet_data
        elif this_packet_type == SAF_SET_POSITION:
            self.target_position = this_packet_data
        elif this_packet_type == SAF_MAX_POSITION:
            self.max_position = this_packet_data
        elif this_packet_type == SAF_STEP_TIME_US:
            self.step_time_us = this_packet_data
        elif this_packet_type == SAF_DRIVER_CONFIG:
            ihold = this_packet_data & 0x1F
            irun = (this_packet_data >> 5) & 0x1F
            sgthrs = (this_packet_data >> 10) & 0x1FF
            self.set_current_configuration(ihold, irun, sgthrs)
        elif this_packet_type == SAF_DRIVER_STATUS:
            this_packet_flag_bits = (1 << 31) | (1 << 15) | (1 << 14) | (1 << 13) | (1 << 12) | (1 << 11) | (1 << 10)
            cs_actual = (this_packet_data >> 16) & 0x0F
            sg_result = this_packet_data  & 0x03FF
            self.current_actual_bits = cs_actual
            self.stall_actual_bits = sg_result
            self.set_driver_status(DriverStatus(this_packet_data & this_packet_flag_bits))
        elif this_packet_type == SAF_FIRMWARE_COMMIT_ID:
            commit = f"{this_packet_data:07x}"
            self.commit = commit
        elif this_packet_type == SAF_DRIVER_TYPE:
            self.driver_type = SAFDriverType(this_packet_data)
        elif this_packet_type == SAF_MCU_TYPE:
            self.microcontroller_type = SAFMicrocontrollerType(this_packet_data)
        elif this_packet_type == SAF_FIRMWARE_STATE:
            pass # undocumented
        elif this_packet_type == SAF_GUID_1:
            self.set_guid1(this_packet_data)
        elif this_packet_type == SAF_GUID_2:
            self.set_guid2(this_packet_data)
        elif this_packet_type == SAF_GUID_3:
            self.set_guid3(this_packet_data)
        elif this_packet_type == SAF_INVALID_PACKET:
            pass   # Ignore the packet
        else:
            raise SympleAFInvalidResponse(f"Received invalid type from controller: {this_packet_type:02X}")
