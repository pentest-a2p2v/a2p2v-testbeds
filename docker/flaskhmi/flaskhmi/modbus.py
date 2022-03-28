#!/usr/bin/env python3

from pymodbus.client.sync import ModbusTcpClient

DEFAULT_IP_ADDRESS = '192.168.30.105'
DEFAULT_PORT = 502


class ModbusClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._client_connect()

    def _client_connect(self):
        self.client = ModbusTcpClient(self.ip, self.port)

    def _client_close(self):
        self.client.close()
        self.client = None

    def get_temperature(self):
        """Returns a tuple of the temperature and setting"""
        address = 0
        count = 4
        unit = 255

        result = self.client.read_holding_registers(
            address=address, count=count, unit=unit
        )

        return (result.registers[1], result.registers[2])

    def write_register(self, address=2, value=20, unit=255):
        """Write to a Modbus register"""
        _ = self.client.write_register(address=address, value=value, unit=unit)

    def raise_temperature_1c(self):
        """Raise the temperature by 1 degree celsius"""
        self.write_register(address=3, value=1, unit=255)

    def lower_temperature_1c(self):
        """Lower the temperature by 1 degree celsius"""
        self.write_register(address=3, value=0, unit=255)
