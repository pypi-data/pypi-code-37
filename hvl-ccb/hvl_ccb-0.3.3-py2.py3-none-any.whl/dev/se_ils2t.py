"""
Device class for controlling a Schneider Electric ILS2T stepper drive over modbus TCP.
"""

import logging
from datetime import timedelta
from enum import Flag, IntEnum
from time import sleep
from typing import Dict, List, Any

import aenum
from bitstring import BitArray
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

from .base import SingleCommDevice
from ..comm import (
    ModbusTcpCommunication,
    ModbusTcpConnectionFailedException,
    ModbusTcpCommunicationConfig,
)
from ..configuration import configdataclass


class ILS2TException(Exception):
    """
    Exception to indicate problems with the SE ILS2T stepper motor.
    """

    pass


class IoScanningModeValueError(ILS2TException):
    """
    Exception to indicate that the selected IO scanning mode is invalid.
    """

    pass


class ScalingFactorValueError(ILS2TException):
    """
    Exception to indicate that a scaling factor value is invalid.
    """

    pass


@configdataclass
class ILS2TModbusTcpCommunicationConfig(ModbusTcpCommunicationConfig):
    """
    Configuration dataclass for Modbus/TCP communciation specific for the Schneider
    Electric ILS2T stepper motor.
    """

    #: The unit has to be 255 such that IO scanning mode works.
    unit: int = 255


class ILS2TModbusTcpCommunication(ModbusTcpCommunication):
    """
    Specific implementation of Modbus/TCP for the Schneider Electric ILS2T stepper
    motor.
    """

    @staticmethod
    def config_cls():
        return ILS2TModbusTcpCommunicationConfig


@configdataclass
class ILS2TConfig:
    """
    Configuration for the ILS2T stepper motor device.
    """

    #: initial maximum RPM for the motor, can be set up to 3000 RPM. The user is
    #: allowed to set a new max RPM at runtime using :meth:`ILS2T.set_max_rpm`,
    #: but the value must never exceed this configuration setting.
    rpm_max_init: int = 1500


class ILS2T(SingleCommDevice):
    """
    Schneider Electric ILS2T stepper drive class.
    """

    class RegDatatype(aenum.Enum):
        """
        Modbus Register Datatypes

        From the manual of the drive:

        =========== =========== ============== =============
        datatype    byte        min            max
        =========== =========== ============== =============
        INT8        1 Byte      -128           127
        UINT8       1 Byte      0              255
        INT16       2 Byte      -32_768        32_767
        UINT16      2 Byte      0              65_535
        INT32       4 Byte      -2_147_483_648 2_147_483_647
        UINT32      4 Byte      0              4_294_967_295
        BITS        just 32bits N/A            N/A
        =========== =========== ============== =============

        """
        _init_ = 'min max'
        INT32 = -2_147_483_648, 2_147_483_647

        def is_in_range(self, value: int) -> bool:
            return self.min <= value <= self.max

    class RegAddr(IntEnum):
        """
        ILS2T Modbus Register Adresses
        """
        POSITION = 7706  # INT32 position of the motor in user defined units
        IO_SCANNING = 6922  # BITS start register for IO scanning control
        # and status
        TEMP = 7200  # INT16 temperature of motor
        VOLT = 7198  # UINT16 dc voltage of motor
        SCALE = 1550  # INT32 user defined steps per revolution
        ACCESS_ENABLE = 282  # BITS not documented register
        # to enable access via IO scanning
        JOGN_FAST = 10506  # UINT16 revolutions per minute for fast Jog (1 to 3000)
        JOGN_SLOW = 10504  # UINT16 revolutions per minute
        # for slow Jog (1 to 3000)

        RAMP_TYPE = 1574  # INT16 ramp type, 0: linear / -1: motor optimized
        RAMP_ACC = 1556  # UINT32 acceleration
        RAMP_DECEL = 1558  # UINT32 deceleration
        RAMP_N_MAX = 1554  # UINT16 max rpm
        FLT_INFO = 15362  # 22 registers, code for error
        FLT_MEM_RESET = 15114  # UINT16 reset fault memory
        FLT_MEM_DEL = 15112  # UINT16 delete fault memory

    class Mode(IntEnum):
        """
        ILS2T device modes
        """
        PTP = 3  # point to point
        JOG = 1

    class ActionsPtp(IntEnum):
        """
        Allowed actions in the point to point mode (`ILS2T.Mode.PTP`).
        """
        ABSOLUTE_POSITION = 0
        RELATIVE_POSITION_TARGET = 1
        RELATIVE_POSITION_MOTOR = 2

    ACTION_JOG_VALUE = 0
    """
    The single action value for `ILS2T.Mode.JOG`
    """

    # Note: don't use IntFlag here - it allows other then enumerated values
    class Ref16Jog(Flag):
        """
        Allowed values for ILS2T ref_16 register (the shown values are the integer
        representation of the bits), all in Jog mode = 1
        """
        NONE = 0
        POS = 1
        NEG = 2
        FAST = 4
        # allowed combinations
        POS_FAST = POS | FAST
        NEG_FAST = NEG | FAST

    class State(IntEnum):
        """
        State machine status values
        """
        QUICKSTOP = 7
        READY = 4
        ON = 6

    DEFAULT_IO_SCANNING_CONTROL_VALUES = {
        'action': ActionsPtp.RELATIVE_POSITION_MOTOR.value,
        'mode': Mode.PTP.value,
        'disable_driver_di': 0,
        'enable_driver_en': 0,
        'quick_stop_qs': 0,
        'fault_reset_fr': 0,
        'execute_stop_sh': 0,
        'reset_stop_ch': 0,
        'continue_after_stop_cu': 0,
        'ref_16': ILS2TConfig.rpm_max_init,
        'ref_32': 0,
    }
    """
    Default IO Scanning control mode values
    """

    def __init__(self, com, dev_config=None) -> None:
        """
        Constructor for ILS2T.

        :param com: object to use as communication protocol.
        """

        # Call superclass constructor
        super().__init__(com, dev_config)

        # toggle reminder bit
        self._mode_toggle_mt = 0
        self.flt_list = []

    @staticmethod
    def default_com_cls():
        return ILS2TModbusTcpCommunication

    @staticmethod
    def config_cls():
        return ILS2TConfig

    def start(self) -> None:
        """
        Start this device.
        """

        logging.info("Starting device " + str(self))

        try:
            # try opening the port
            self.com.open()
        except ModbusTcpConnectionFailedException as exc:
            logging.error(exc)
            raise

        # writing 1 to register ACCESS_ENABLE allows to use the IO scanning mode.
        #  This is not documented in the manual!
        self.com.write_registers(self.RegAddr.ACCESS_ENABLE.value,
                                 [0, 1])

        # set maximum RPM from init config
        self.set_max_rpm(self.config.rpm_max_init)

    def stop(self) -> None:
        """
        Stop this device. Disables the motor (applies brake), disables access and
        closes the communication protocol.
        """

        logging.info("Stopping device " + str(self))
        self.disable()
        self.com.write_registers(self.RegAddr.ACCESS_ENABLE.value,
                                 [0, 0])
        self.com.close()

    def get_status(self) -> Dict[str, int]:
        """
        Perform an IO Scanning read and return the status of the motor.

        :return: dict with status information.
        """

        registers = self.com \
            .read_holding_registers(self.RegAddr.IO_SCANNING.value, 8)
        return self._decode_status_registers(registers)

    def do_ioscanning_write(self, **kwargs: int) -> None:
        """
        Perform a write operation using IO Scanning mode.

        :param kwargs:
            Keyword-argument list with options to send, remaining are taken
            from the defaults.
        """

        self._toggle()
        values = self._generate_control_registers(**kwargs)
        self.com.write_registers(self.RegAddr.IO_SCANNING.value,
                                 values)

    def _generate_control_registers(self, **kwargs: int) -> List[int]:
        """
        Generates the control registers for the IO scanning mode.
        It is necessary to write all 64 bit at the same time, so a list of 4 registers
        is generated.

        :param kwargs: Keyword-argument list with options different than the defaults.
        :return: List of registers for the IO scanning mode.
        """

        cleaned_io_scanning_mode = self._clean_ioscanning_mode_values(kwargs)

        action_bits = '{0:03b}'.format(cleaned_io_scanning_mode['action'])
        mode_bits = '{0:04b}'.format(cleaned_io_scanning_mode['mode'])
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)

        # add the first byte: Drive control
        builder.add_bits(
            [
                cleaned_io_scanning_mode['disable_driver_di'],
                cleaned_io_scanning_mode['enable_driver_en'],
                cleaned_io_scanning_mode['quick_stop_qs'],
                cleaned_io_scanning_mode['fault_reset_fr'],
                0,  # has to be 0 per default, no meaning
                cleaned_io_scanning_mode['execute_stop_sh'],
                cleaned_io_scanning_mode['reset_stop_ch'],
                cleaned_io_scanning_mode['continue_after_stop_cu'],
            ]
        )

        # add the second byte: Mode control
        builder.add_bits(
            [
                int(mode_bits[3]),
                int(mode_bits[2]),
                int(mode_bits[1]),
                int(mode_bits[0]),
                int(action_bits[2]),
                int(action_bits[1]),
                int(action_bits[0]),
                self._mode_toggle_mt,
            ]
        )

        # add the third and fourth byte:
        # Ref_16 (either JOG direction/speed, or RPM...)
        builder.add_16bit_uint(cleaned_io_scanning_mode['ref_16'])

        # add 4 bytes Ref_32, Target position
        builder.add_32bit_int(cleaned_io_scanning_mode['ref_32'])

        return builder.to_registers()

    def _clean_ioscanning_mode_values(self, io_scanning_values: Dict[str, int]) \
            -> Dict[str, int]:
        """
        Checks if the constructed mode is valid.

        :param io_scanning_values: Dictionary with register values to check
        :return: Dictionary with cleaned register values
        :raises ValueError: if `io_scanning_values` has unrecognized keys
        :raises IoScanningModeValueError: if either `'mode'` or either of corresponding
            `'action'`, `'ref_16'`, or `'ref_32'` keys of `io_scanning_values` has
            an invalid value.
        """

        # check if there are too much keys that are not recognized
        io_scanning_keys = set(io_scanning_values.keys())
        all_keys = set(self.DEFAULT_IO_SCANNING_CONTROL_VALUES.keys())
        superfluous_keys = io_scanning_keys.difference(all_keys)
        if superfluous_keys:
            raise ValueError("Unrecognized mode keys: {}".format(
                list(superfluous_keys)))

        # fill up io_scanning_values with defaults, if they are not set
        for mode_key, default_value in self.DEFAULT_IO_SCANNING_CONTROL_VALUES.items():
            if mode_key not in io_scanning_values:
                io_scanning_values[mode_key] = default_value

        # perform checks depending on mode
        # JOG mode
        if io_scanning_values['mode'] == self.Mode.JOG:

            if not io_scanning_values['action'] == self.ACTION_JOG_VALUE:
                raise IoScanningModeValueError(
                    'Wrong action: {}'.format(io_scanning_values['action'])
                )

            try:
                self.Ref16Jog(io_scanning_values['ref_16'])
            except ValueError:
                raise IoScanningModeValueError(
                    'Wrong value in ref_16 ({})'.format(io_scanning_values['ref_16'])
                )

            if not io_scanning_values['ref_32'] == 0:
                raise IoScanningModeValueError(
                    'Wrong value in ref_32 ({})'.format(io_scanning_values['ref_32'])
                )

            return io_scanning_values

        # PTP mode
        if io_scanning_values['mode'] == self.Mode.PTP:

            try:
                self.ActionsPtp(io_scanning_values['action'])
            except ValueError:
                raise IoScanningModeValueError(
                    'Wrong action: {}'.format(io_scanning_values['action'])
                )

            if not self._is_valid_rpm(io_scanning_values['ref_16']):
                raise IoScanningModeValueError(
                    'Wrong value in ref_16 ({})'.format(io_scanning_values['ref_16'])
                )

            if not self._is_int32(io_scanning_values['ref_32']):
                raise IoScanningModeValueError(
                    'Wrong value in ref_32 ({})'.format(io_scanning_values['ref_32'])
                )

            return io_scanning_values

        # default
        raise IoScanningModeValueError(
            'Wrong mode: {}'.format(io_scanning_values['mode'])
        )

    def _is_valid_rpm(self, num: int) -> bool:
        """
        Checks whether `num` is a valid RPM value.

        :param num: RPM value to check
        :return: `True` if `num` is a valid RPM value, `False` otherwise
        """

        return isinstance(num, int) and 0 < num <= self.config.rpm_max_init

    @classmethod
    def _is_int32(cls, num: int) -> bool:
        """
        Checks whether a number fits in a signed 32-bit integer.

        :param num: is the number to check.
        :return: check result.
        """

        return isinstance(num, int) and cls.RegDatatype.INT32.is_in_range(num)

    @staticmethod
    def _decode_status_registers(registers: List[int]) -> Dict[str, int]:
        """
        Decodes the the status of the stepper drive, derived from IOscanning.

        :param registers: List of 8 registers (6922-6930)
        :return: dict
        """

        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.Big)
        decoded = {
            'drive_control': decoder.decode_bits(),
            'mode_control': decoder.decode_bits(),
            'ref_16': decoder.decode_16bit_int(),
            'ref_32': decoder.decode_32bit_int(),
            'drive_status_1': decoder.decode_bits(),
            'drive_status_2': decoder.decode_bits(),
            'mode_status': decoder.decode_bits(),
            'drive_input': decoder.decode_bits(),
            'action_word_1': decoder.decode_bits(),
            'action_word_2': decoder.decode_bits(),
            'special_function_1': decoder.decode_bits(),
            'special_function_2': decoder.decode_bits(),
        }

        return {
            'mode': BitArray(decoded['mode_status'][3::-1]).int,
            'action': BitArray(decoded['mode_control'][6:3:-1]).int,
            'ref_16': decoded['ref_16'],
            'ref_32': decoded['ref_32'],
            'state': BitArray(decoded['drive_status_2'][3::-1]).int,
            'fault': decoded['drive_status_2'][6],
            'warn': decoded['drive_status_2'][7],
            'halt': decoded['drive_status_1'][0],
            'motion_zero': decoded['action_word_2'][6],
            'turning_positive': decoded['action_word_2'][7],
            'turning_negative': decoded['action_word_1'][0],
        }

    def _toggle(self) -> None:
        """
        To activate a command it is necessary to toggle the MT bit first.
        """

        self._mode_toggle_mt = (0 if self._mode_toggle_mt else 1)

    def relative_step(self, steps: int) -> None:
        """
        Turn the motor the relative amount of steps. This function does not enable or
        disable the motor automatically.
        positive numbers -> CW
        negative numbers -> CCW

        :param steps: Number of steps to turn the motor.
        """

        if not abs(steps) < 2_147_483_647:
            logging.warning('number of steps is too big: {}'.format(steps))

        logging.info('Perform number of steps: {}'.format(steps))

        self.do_ioscanning_write(
            enable_driver_en=1,
            mode=self.Mode.PTP.value,
            action=self.ActionsPtp.RELATIVE_POSITION_MOTOR.value,
            ref_32=steps
        )

    def absolute_position(self, position: int) -> None:
        """
        Turn the motor until it reaches the absolute position.
        This function does not enable or disable the motor automatically.

        :param position: absolute position of motor in user defined steps.
        """

        if not abs(position) < 2_147_483_647:
            logging.warning('position is out of range: {}'.format(position))

        logging.info('Absolute position: {}'.format(position))

        self.do_ioscanning_write(
            enable_driver_en=1,
            mode=self.Mode.PTP.value,
            action=self.ActionsPtp.ABSOLUTE_POSITION.value,
            ref_32=position
        )

    def relative_step_and_wait(self, steps: int) -> None:
        """
        Enable motor, perform relative steps and wait until done, disable.

        :param steps: Number of steps.
        """

        logging.info('Motor steps requested: {}'.format(steps))

        position_before = self.get_position()

        self.enable()
        sleep(1)
        self.relative_step(steps)
        sleep(2)

        while True:
            if self.get_status()['motion_zero']:
                self.disable()
                break

        # check if steps were made
        position_after = self.get_position()
        if position_before + steps != position_after:
            flt_dict = self.get_error_code()
            self.flt_list.append(flt_dict)
            if 'empty' in flt_dict[0].keys():
                logging.warning('no error in drive, '
                                'something different must have gone wrong')
                logging.warning(
                    'The position does not align with the requested step '
                    'number. Before: {0}, after: {1}, requested: {2}, '
                    'real difference: {3}'.format(
                        position_before,
                        position_after,
                        steps,
                        position_after - position_before,
                    )
                )
            else:
                # Despite drive error/malfunction don't break the code/experiment
                # execution by raising an error; continuing as nothing happened.
                logging.critical('error in drive, drive is know maybe locked')
                logging.critical(
                    'The position does not align with the requested step '
                    'number. Before: {0}, after: {1}, requested: {2}, '
                    'real difference: {3}'.format(
                        position_before,
                        position_after,
                        steps,
                        position_after - position_before,
                    )
                )

    def absolute_position_and_wait(self, position: int) -> None:
        """
        Enable motor, perform absolute position and wait until done, disable.

        :param position: absolute position of motor in user defined steps.
        """

        logging.info('absolute position requested: {}'.format(position))

        position_before = self.get_position()

        self.enable()
        sleep(1)
        self.absolute_position(position)
        sleep(2)

        while True:
            if self.get_status()['motion_zero']:
                self.disable()
                break

        # check if steps were made
        position_after = self.get_position()
        if position != position_after:
            flt_dict = self.get_error_code()
            self.flt_list.append(flt_dict)
            if 'empty' in flt_dict[0].keys():
                logging.warning('no error in drive, '
                                'something different must have gone wrong')
                logging.warning(
                    'The position does not align with the requested absolute position. '
                    'Before: {0}, after: {1}, requested: {2}'
                    .format(
                        position_before,
                        position_after,
                        position,
                    )
                )
            else:
                logging.critical('error in drive, drive is know maybe locked')
                logging.critical(
                    'The position does not align with the requested absolute position. '
                    'Before: {0}, after: {1}, requested: {2}'
                    .format(
                        position_before,
                        position_after,
                        position,
                    )
                )

    def disable(self) -> None:
        """
        Disable the driver of the stepper motor and enable the brake.
        """

        if self.get_status()['motion_zero']:
            logging.info('Disable motor, brake.')
            self.do_ioscanning_write(enable_driver_en=0, disable_driver_di=1)
        else:
            logging.warning('Cannot disable motor, still running!')

    def enable(self) -> None:
        """
        Enable the driver of the stepper motor and disable the brake.
        """

        self.do_ioscanning_write(enable_driver_en=1, disable_driver_di=0)
        logging.info('Enable motor, disable brake.')

    def get_position(self) -> int:
        """
        Read the position of the drive and store into status.

        :return: Position step value
        """

        value = self.com.read_input_registers(
            self.RegAddr.POSITION.value, 2)
        return self._decode_32bit(value, True)

    def get_temperature(self) -> int:
        """
        Read the temperature of the motor.

        :return: Temperature in degrees Celsius.
        """

        value = self.com.read_input_registers(
            self.RegAddr.TEMP.value, 2)
        return self._decode_32bit(value, True)

    def get_dc_volt(self) -> float:
        """
        Read the DC supply voltage of the motor.

        :return: DC input voltage.
        """

        value = self.com.read_input_registers(
            self.RegAddr.VOLT.value, 2)
        return self._decode_32bit(value, True) / 10

    @staticmethod
    def _decode_32bit(registers: List[int], signed: bool = True) -> int:
        """
        Decode two 16-bit ModBus registers to a 32-bit integer.

        :param registers: list of two register values
        :param signed: True, if register containes a signed value
        :return: integer representation of the 32-bit register
        """

        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.Big)
        if signed:
            return decoder.decode_32bit_int()
        else:
            return decoder.decode_32bit_uint()

    def user_steps(self, steps: int = 16384, revolutions: int = 1) -> None:
        """
        Define steps per revolution.
        Default is 16384 steps per revolution.
        Maximum precision is 32768 steps per revolution.

        :param steps: number of steps in `revolutions`.
        :param revolutions: number of revolutions corresponding to `steps`.
        """

        if not self._is_int32(revolutions):
            err_msg = 'Wrong scaling factor: revolutions = {}'.format(revolutions)
            logging.error(err_msg)
            raise ScalingFactorValueError(err_msg)

        if not self._is_int32(steps):
            err_msg = 'Wrong scaling factor: steps = {}'.format(steps)
            logging.error(err_msg)
            raise ScalingFactorValueError(err_msg)

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_32bit_int(steps)
        builder.add_32bit_int(revolutions)
        values = builder.to_registers()
        self.com.write_registers(self.RegAddr.SCALE.value, values)

    def quickstop(self) -> None:
        """
        Stops the motor with high deceleration rate and falls into error state. Reset
        with `reset_error` to recover into normal state.
        """

        logging.warning('Motor QUICK STOP.')
        self.do_ioscanning_write(quick_stop_qs=1)

    def reset_error(self) -> None:
        """
        Resets the motor into normal state after quick stop or another error occured.
        """

        logging.info('Reset motor after fault or quick stop.')
        self.do_ioscanning_write(fault_reset_fr=1)

    def jog_run(self, direction: bool = True, fast: bool = False) -> None:
        """
        Slowly turn the motor in positive direction.
        """

        status = self.get_status()

        if status['mode'] != self.Mode.JOG and not status['motion_zero']:
            logging.error('Motor is not in Jog mode or standstill, abort.')
            return

        if status['state'] != self.State.ON:
            # need to enable first
            logging.error('Motor is not enabled or in error state. Try .enable()')
            return

        ref_16 = self.Ref16Jog.NONE

        if direction:
            ref_16 = ref_16 | self.Ref16Jog.POS
            logging.info('Jog mode in positive direction enabled.')
        else:
            ref_16 = ref_16 | self.Ref16Jog.NEG
            logging.info('Jog mode in negative direction enabled.')

        if fast:
            ref_16 = ref_16 | self.Ref16Jog.FAST

        self.do_ioscanning_write(
            mode=self.Mode.JOG.value,
            action=self.ACTION_JOG_VALUE,
            enable_driver_en=1,
            ref_16=ref_16.value,
        )

    def jog_stop(self) -> None:
        """
        Stop turning the motor in Jog mode.
        """

        logging.info('Stop in Jog mode.')

        self.do_ioscanning_write(
            mode=self.Mode.JOG.value,
            action=self.ACTION_JOG_VALUE,
            enable_driver_en=1,
            ref_16=0,
        )

    def set_jog_speed(self, slow: int = 60, fast: int = 180) -> None:
        """
        Set the speed for jog mode. Default values correspond to startup values of
        the motor.

        :param slow: RPM for slow jog mode.
        :param fast: RPM for fast jog mode.
        """

        logging.info(
            'Setting Jog RPM. Slow = {0} RPM, Fast = {1} RPM.'.format(
                slow, fast
            )
        )
        self.com.write_registers(self.RegAddr.JOGN_SLOW.value,
                                 [0, slow])
        self.com.write_registers(self.RegAddr.JOGN_FAST.value,
                                 [0, fast])

    def get_error_code(self) -> Dict[int, Dict[str, Any]]:
        """
        Read all messages in fault memory.
        Will read the full error message and return the decoded values.
        At the end the fault memory of the motor will be deleted.
        In addition, reset_error is called to re-enable the motor for operation.

        :return: Dictionary with all information
        """

        ret_dict = {}
        self.com.write_registers(self.RegAddr.FLT_MEM_RESET.value,
                                 [0, 1])
        for i in range(10):
            registers = self.com.read_input_registers(
                self.RegAddr.FLT_INFO.value, 22)
            decoder = BinaryPayloadDecoder.fromRegisters(registers,
                                                         byteorder=Endian.Big)
            decoded = {
                'ignored0': decoder.skip_bytes(2),
                'error_code': decoder.decode_16bit_uint(),
                'ignored1': decoder.skip_bytes(2),
                'error_class': decoder.decode_16bit_uint(),
                'error_time': decoder.decode_32bit_uint(),
                'ignored2': decoder.skip_bytes(2),
                'error_addition': decoder.decode_16bit_uint(),
                'ignored3': decoder.skip_bytes(2),
                'error_no_cycle': decoder.decode_16bit_uint(),
                'ignored4': decoder.skip_bytes(2),
                'error_after_enable': decoder.decode_16bit_uint(),
                'ignored5': decoder.skip_bytes(2),
                'error_voltage_dc': decoder.decode_16bit_uint(),
                'ignored6': decoder.skip_bytes(2),
                'error_rpm': decoder.decode_16bit_int(),
                'ignored7': decoder.skip_bytes(2),
                'error_current': decoder.decode_16bit_uint(),
                'ignored8': decoder.skip_bytes(2),
                'error_amplifier_temperature': decoder.decode_16bit_int(),
                'ignored9': decoder.skip_bytes(2),
                'error_device_temperature': decoder.decode_16bit_int(),
            }
            flt_dict = {
                'error_code': hex(decoded['error_code'])[2:],
                'error_class': decoded['error_class'],
                'error_time': timedelta(seconds=decoded['error_time']),
                'error_addition': decoded['error_addition'],
                'error_no_cycle': decoded['error_no_cycle'],
                'error_after_enable': timedelta(seconds=decoded['error_after_enable']),
                'error_voltage_dc': decoded['error_voltage_dc'] / 10,
                'error_rpm': decoded['error_rpm'],
                'error_current': decoded['error_current'] / 100,
                'error_amplifier_temperature': decoded['error_amplifier_temperature'],
                'error_device_temperature': decoded['error_device_temperature'],
            }
            ret_dict[i] = flt_dict
            if flt_dict['error_code'] == '0':
                flt_dict = {'empty': None}
                ret_dict = {i: flt_dict}
                break
        self.com.write_registers(self.RegAddr.FLT_MEM_DEL.value,
                                 [0, 1])
        self.reset_error()
        return ret_dict

    def set_max_rpm(self, rpm: int) -> None:
        """
        Set the maximum RPM.

        :param rpm: revolution per minute ( 0 < rpm <= RPM_MAX)
        :raises ILS2TException: if RPM is out of range
        """

        if self._is_valid_rpm(rpm):
            self.DEFAULT_IO_SCANNING_CONTROL_VALUES['ref_16'] = rpm
            self.com.write_registers(
                self.RegAddr.RAMP_N_MAX.value, [0, rpm])
        else:
            raise ILS2TException('RPM out of range: {rpm} not in (0, {rpm_max}'.format(
                rpm=rpm,
                rpm_max=self.config.rpm_max_init,
            ))

    def set_ramp_type(self, ramp_type: int = -1) -> None:
        """
        Set the ramp type. There are two options available:
            0:  linear ramp
            -1: motor optimized ramp

        :param ramp_type: 0: linear ramp | -1: motor optimized ramp
        """

        self.com.write_registers(
            self.RegAddr.RAMP_TYPE.value, [0, ramp_type]
        )

    def set_max_acceleration(self, rpm_minute: int) -> None:
        """
        Set the maximum acceleration of the motor.

        :param rpm_minute: revolution per minute per minute
        """

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_32bit_uint(rpm_minute)
        values = builder.to_registers()
        self.com.write_registers(self.RegAddr.RAMP_ACC.value, values)

    def set_max_deceleration(self, rpm_minute: int) -> None:
        """
        Set the maximum deceleration of the motor.

        :param rpm_minute: revolution per minute per minute
        """

        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_32bit_uint(rpm_minute)
        values = builder.to_registers()
        self.com.write_registers(self.RegAddr.RAMP_DECEL.value,
                                 values)
