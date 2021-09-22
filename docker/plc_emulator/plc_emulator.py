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


def updating_writer(a):
    """A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    context = a[0]
    register = 3
    slave_id = 0x00
    # address = 0  # 0x10
    # tag_value = context[slave_id].getValues(register, REG_TAG, count=1)[0]
    temp_value = context[slave_id].getValues(register, REG_TEMP, count=1)[0]
    setting_value = context[slave_id].getValues(
        register, REG_SETTING, count=1
    )[0]
    control_value = context[slave_id].getValues(
        register, REG_CONTROL, count=1
    )[0]

    # log.debug("tag_value: %d", tag_value)
    log.debug("temp_value: %d", temp_value)
    log.debug("setting_value: %d", setting_value)
    # log.debug("control_value: %d", control_value)

    if control_value == 0:
        setting_value -= 1
        control_value = 100
    elif control_value == 1:
        setting_value += 1
        control_value = 100

    if temp_value < setting_value:
        temp_value += 1
    elif temp_value > setting_value:
        temp_value -= 1

    context[slave_id].setValues(register, REG_TEMP, [temp_value])
    context[slave_id].setValues(register, REG_SETTING, [setting_value])
    context[slave_id].setValues(register, REG_CONTROL, [control_value])

    # values = context[slave_id].getValues(register, address, count=5)
    # values = [v + 1 for v in values]
    # log.debug("new values: " + str(values))
    # context[slave_id].setValues(register, address, values)


def run_updating_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [10] * 100),
        co=ModbusSequentialDataBlock(0, [11] * 100),
        # hr=ModbusSequentialDataBlock(0, list(range(0,100))),
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
    time = 5  # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False)  # initially delay by time
    StartTcpServer(context, identity=identity, address=("", 502))


if __name__ == "__main__":
    run_updating_server()
