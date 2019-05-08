"""
Device class for controlling a MBW 973 SF6 Analyzer over a serial connection.

The MBW 973 is a gas analyzer designed for gas insulated switchgear and measures
humidity, SF6 purity and SO2 contamination in one go.
Manufacturer homepage: https://www.mbw.ch/products/sf6-gas-analysis/973-sf6-analyzer/
"""

import logging
from threading import Timer
from typing import Dict, Callable, Type

from serial import SerialException

from .base import SingleCommDevice
from ..comm import SerialCommunication, SerialCommunicationConfig
from ..configuration import configdataclass


class MBW973Error(Exception):
    """
    General error with the MBW973 dew point mirror device.
    """
    pass


class MBW973ControlRunningException(MBW973Error):
    """
    Error indicating there is still a measurement running, and a new one cannot be
    started.
    """
    pass


class MBW973PumpRunningException(MBW973Error):
    """
    Error indicating the pump of the dew point mirror is still recovering gas,
    unable to start a new measurement.
    """
    pass


@configdataclass
class MBW973SerialCommunicationConfig(SerialCommunicationConfig):
    #: Baudrate for MBW973 is 9600 baud
    baudrate: int = 9600

    #: MBW973 does not use parity
    parity: (str, SerialCommunicationConfig.Parity) = \
        SerialCommunicationConfig.Parity.NONE

    #: MBW973 does use one stop bit
    stopbits: (int, SerialCommunicationConfig.Stopbits) = \
        SerialCommunicationConfig.Stopbits.ONE

    #: One byte is eight bits long
    bytesize: (int, SerialCommunicationConfig.Bytesize) = \
        SerialCommunicationConfig.Bytesize.EIGHTBITS

    #: The terminator is only CR
    terminator: bytes = b'\r'

    #: use 3 seconds timeout as default
    timeout: (int, float) = 3


class MBW973SerialCommunication(SerialCommunication):
    """
    Specific communication protocol implementation for the MBW973 dew point mirror.
    Already predefines device-specific protocol parameters in config.
    """

    @staticmethod
    def config_cls():
        return MBW973SerialCommunicationConfig


@configdataclass
class MBW973Config:
    """
    Device configuration dataclass for MBW973.
    """

    #: Polling period for `is_done` status queries [in seconds].
    polling_interval: (int, float) = 2

    def clean_values(self):
        if self.polling_interval <= 0:
            raise ValueError('Polling interval needs to be positive.')


class MBW973(SingleCommDevice):
    """
    MBW 973 dew point mirror device class.
    """

    def __init__(self, com, dev_config=None):

        # Call superclass constructor
        super().__init__(com, dev_config)

        # polling timer thread
        self.polling_timer = Poller(self.config.polling_interval, self.is_done)

        # is done with dew point = True, new measurement sample required and
        # not ready yet = False
        self.is_done_with_measurements = True

        # dict telling what measurement options are selected
        self.measurement_options = {
            'dewpoint': True,
            'SF6_Vol': False,
        }

        self.last_measurement_values = {}

    @staticmethod
    def default_com_cls():
        return MBW973SerialCommunication

    @staticmethod
    def config_cls():
        return MBW973Config

    def start(self) -> None:
        """
        Start this device. Opens the communication protocol and retrieves the
        set measurement options from the device.
        """

        logging.info("Starting device " + str(self))

        # TODO: re-factor this error-handling to SerialCommunication.open()?
        try:
            self.com.open()
        except SerialException as exc:
            # only catch "port already open"
            if str(exc) != 'Port is already open.':
                raise MBW973Error from exc

        # check test options
        self.write('HumidityTest?')
        self.measurement_options['dewpoint'] = bool(self.read_int())

        self.write('SF6PurityTest?')
        self.measurement_options['SF6_Vol'] = bool(self.read_int())

    def stop(self) -> None:
        """
        Stop the device. Closes also the communication protocol.
        """

        logging.info("Stopping device " + str(self))
        self.com.close()

    def write(self, value) -> None:
        """
        Send `value` to `self.com`.

        :param value: Value to send, converted to `str`.
        """
        self.com.write_text(str(value))

    def read(self, cast_type: Type = str):
        """
        Read value from `self.com` and cast to `cast_type`.
        Raises `ValueError` if read text (`str`) is not convertible to `cast_type`,
        e.g. to `float` or to `int`.

        :return: Read value of `cast_type` type.
        """
        return cast_type(self.com.read_text())

    def read_float(self) -> float:
        """
        Convenience wrapper for `self.read()`, with typing hint for return value.

        :return: Read `float` value.
        """
        return self.read(float)

    def read_int(self) -> int:
        """
        Convenience wrapper for `self.read()`, with typing hint for return value.

        :return: Read `int` value.
        """
        return self.read(int)

    def is_done(self) -> bool:
        """
        Poll status of the dew point mirror and return True, if all
        measurements are done.

        :return: True, if all measurements are done; False otherwise.
        """

        # assume everything is done
        done = True

        if self.measurement_options['dewpoint']:
            # ask if done with DP
            self.write('DoneWithDP?')
            done = done and bool(self.read_int())

        if self.measurement_options['SF6_Vol']:
            # ask if done with SF6 volume measurement
            self.write('SF6VolHold?')
            done = done and bool(self.read_int())

        self.is_done_with_measurements = done

        if self.is_done_with_measurements:
            self.polling_timer.stop()
            self.read_measurements()

        return self.is_done_with_measurements

    def start_control(self) -> None:
        """
        Start dew point control to acquire a new value set.
        """

        # send control?
        self.write('control?')

        if self.read_float():
            raise MBW973ControlRunningException

        # send Pump.on? to check, whether gas is still being pumped back
        self.write('Pump.on?')

        if self.read_float():
            raise MBW973PumpRunningException

        # start control of device
        self.write('control=1')
        logging.info('Starting dew point control')
        self.is_done_with_measurements = False
        self.polling_timer.start()

    def read_measurements(self) -> Dict[str, float]:
        """
        Read out measurement values and return them as a dictionary.

        :return: Dictionary with values.
        """

        self.write('Fp?')
        frostpoint = self.read_float()

        self.write('Fp1?')
        frostpoint_ambient = self.read_float()

        self.write('Px?')
        pressure = self.read_float()

        self.write('PPMv?')
        ppmv = self.read_float()

        self.write('PPMw?')
        ppmw = self.read_float()

        self.write('SF6Vol?')
        sf6_vol = self.read_float()

        values = {
            'frostpoint': frostpoint,
            'frostpoint_ambient': frostpoint_ambient,
            'pressure': pressure,
            'ppmv': ppmv,
            'ppmw': ppmw,
            'sf6_vol': sf6_vol,
        }

        logging.info('Read out values')
        logging.info(values)

        self.last_measurement_values = values

        return values

    def set_measuring_options(self, humidity: bool = True,
                              sf6_purity: bool = False) -> None:
        """
        Send measuring options to the dew point mirror.

        :param humidity: Perform humidity test or not?
        :param sf6_purity: Perform SF6 purity test or not?
        """

        self.write('HumidityTest={}'.format(1 if humidity else 0))
        self.write('SF6PurityTest={}'.format(1 if sf6_purity else 0))

        self.measurement_options['dewpoint'] = humidity
        self.measurement_options['SF6_Vol'] = sf6_purity


class Poller:
    """
    Wrapper for the threading.Timer class to periodically poll data.
    """

    def __init__(self, period: float, callback: Callable) -> None:
        """
        Constructor for Poller.

        :param period: Period in seconds.
        :param callback: Callback function triggered every `period` seconds.
        """

        self.period = period
        self.callback = callback

        self.t = Timer(period, self.timer_callback)

        # status: False: stopped, True: runs
        self.status = False

    def timer_callback(self) -> None:
        """
        Callback method that is called every time the timer elapses. It calls
        the specified user callback function and
        restarts the timer.
        """

        # call external callback function
        logging.debug('Timer elapsed, call specified callback function: {}'
                      .format(self.callback))
        self.callback()

        logging.debug('Re-initialize timer')
        self.t = Timer(self.period, self.timer_callback)

        logging.debug('Re-start timer')
        if self.status:
            self.t.start()

    def start(self) -> None:
        """
        Start the polling timer.
        """

        logging.debug('Start polling timer')
        self.status = True
        self.t.start()

    def stop(self) -> None:
        """
        Stop the polling timer.
        """

        logging.debug('Stop polling timer')
        self.status = False
        self.t.cancel()
