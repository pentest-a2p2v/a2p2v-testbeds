#!/usr/bin/env python3

"""
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------

This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::

from threading import Thread

thread = Thread(target=updating_writer, args=(context,))
thread.start()
"""
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.device import ModbusDeviceIdentification

# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
from pymodbus.server.asynchronous import StartTcpServer

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #

# Register numbers
REG_TAG = 0
REG_TEMP = 1
REG_SETTING = 2
REG_CONTROL = 3


def update_setting(a):
    """Update the temperature setting
    If the Control register is set to 0, lower the temperature.
    If the Control register is set to 1, raise the temperature.
    In both cases, reset the control register to 100.
    """
    context = a[0]
    register = 3
    slave_id = 0x00

    # Get the current setting value
    setting_value = context[slave_id].getValues(
        register, REG_SETTING, count=1
    )[0]
    # Get the current control value
    control_value = context[slave_id].getValues(
        register, REG_CONTROL, count=1
    )[0]

    # Update the setting based on the control value
    if control_value == 0:
        setting_value -= 1
        control_value = 100
    elif control_value == 1:
        setting_value += 1
        control_value = 100

    # Store the new setting and control values
    context[slave_id].setValues(register, REG_SETTING, [setting_value])
    context[slave_id].setValues(register, REG_CONTROL, [control_value])


def update_temperature(a):
    """Simulate a thermostat by raising/lowering the room temperature
    If the current temp is less than the setting, raise the temp.
    If the current temp is greater than the setting, lower the temp.
    """
    context = a[0]
    register = 3
    slave_id = 0x00
    # Get the current temperature value
    temp_value = context[slave_id].getValues(register, REG_TEMP, count=1)[0]
    # Get the current setting value
    setting_value = context[slave_id].getValues(
        register, REG_SETTING, count=1
    )[0]

    log.debug("temp_value: %d", temp_value)
    log.debug("setting_value: %d", setting_value)

    # Adjust the temperature by one degree each interval
    if temp_value < setting_value:
        temp_value += 1
    elif temp_value > setting_value:
        temp_value -= 1

    # Store the new temperature value
    context[slave_id].setValues(register, REG_TEMP, [temp_value])


def run_updating_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [10] * 100),
        co=ModbusSequentialDataBlock(0, [11] * 100),
        hr=ModbusSequentialDataBlock(
            0, [-1, 20, 20, 20, 100] + list(range(5, 100))
        ),
        ir=ModbusSequentialDataBlock(0, [13] * 100),
    )
    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = "pymodbus"
    identity.ProductCode = "PM"
    identity.VendorUrl = "http://github.com/bashwork/pymodbus/"
    identity.ProductName = "pymodbus Server"
    identity.ModelName = "pymodbus Server"
    identity.MajorMinorRevision = "2.3.0"

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    # Start the setting update thread
    setting_update_interval_seconds = 0.2  # 0.2 seconds delay
    setting_loop = LoopingCall(f=update_setting, a=(context,))
    setting_loop.start(interval=setting_update_interval_seconds, now=False)

    # Start the temperature update thread
    temperature_update_interval_seconds = 5.0  # 2.0 seconds delay
    temperature_loop = LoopingCall(f=update_temperature, a=(context,))
    temperature_loop.start(
        interval=temperature_update_interval_seconds, now=False
    )

    # Start the modbus server
    StartTcpServer(context, identity=identity, address=("", 502))


if __name__ == "__main__":
    run_updating_server()
