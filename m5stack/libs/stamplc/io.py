# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct


class IOStamPLC:
    STAMPLCIO_I2C_ADDRESS = 0x20

    OUTPUT_IO_MODE = 0
    PWM_MODE = 1

    _VOLTAGE_REG = 0x00
    _CURRENT_REG = 0x02
    _IO_CONTROL_REG = 0x10
    _INA226_CONFIG_REG = 0x20
    _PWM_FREQ_REG = 0x30
    _PWM_DUTY_REG = 0x31
    _SYS_STATUS_REG = 0xFB
    _FIRMWARE_VERSION_REG = 0xFE
    _I2C_ADDRESS_REG = 0xFF

    def __init__(self, i2c=None, address: int = STAMPLCIO_I2C_ADDRESS):
        """
        note:
            en: Initialize the StamPLC-IO with a specified I2C address.

        params:
            i2c:
                note: The I2C interface instance for communication.
            address:
                note: The I2C address of the StamPLC-IO, default is 0x20.
        """
        if i2c is None:
            plcio = __import__("stamplc.plc", None, None, True, 0)
            i2c = plcio._get_i2c()
        self.i2c = i2c
        self.address = address

    def _read_u16(self, reg: int) -> int:
        data = self.i2c.readfrom_mem(self.address, reg, 2)
        return data[0] | (data[1] << 8)

    def _read_i32(self, reg: int) -> int:
        data = self.i2c.readfrom_mem(self.address, reg, 4)
        return struct.unpack("<i", data)[0]

    def _write_u16(self, reg: int, value: int) -> None:
        self.i2c.writeto_mem(self.address, reg, bytes([value & 0xFF, (value >> 8) & 0xFF]))

    def _check_ina226_status(self, channel: int) -> None:
        if self.i2c.readfrom_mem(self.address, self._SYS_STATUS_REG, 1)[0] & (1 << channel):
            raise RuntimeError("INA226 channel init error")

    def _check_channel(self, channel: int) -> None:
        if channel not in (0, 1):
            raise ValueError("channel must be 0 or 1")

    def _modify_io_control(self, mask: int, enable: bool) -> None:
        value = self.get_io_control()
        value = value | mask if enable else value & ~mask
        self.set_io_control(value)

    def get_voltage(self, channel: int) -> int:
        """
        note:
            en: Get the voltage of channel 0 or 1 in mV.
        """
        self._check_channel(channel)
        self._check_ina226_status(channel)
        return self._read_u16(self._VOLTAGE_REG + channel * 6)

    def get_current(self, channel: int) -> int:
        """
        note:
            en: Get the current of channel 0 or 1 in uA.
        """
        self._check_channel(channel)
        self._check_ina226_status(channel)
        return self._read_i32(self._CURRENT_REG + channel * 6)

    def get_io_control(self) -> int:
        return self.i2c.readfrom_mem(self.address, self._IO_CONTROL_REG, 1)[0]

    def set_io_control(self, value: int) -> None:
        self.i2c.writeto_mem(self.address, self._IO_CONTROL_REG, bytes([value]))

    def set_solid_relay(self, channel: int, state: bool) -> None:
        self._check_channel(channel)
        self._modify_io_control(1 << channel, state)

    def get_solid_relay(self, channel: int) -> bool:
        self._check_channel(channel)
        return bool(self.get_io_control() & (1 << channel))

    def set_ina226_pullup(self, channel: int, enable: bool) -> None:
        self._check_channel(channel)
        self._modify_io_control(1 << (channel + 2), enable)

    def get_ina226_pullup(self, channel: int) -> bool:
        self._check_channel(channel)
        return bool(self.get_io_control() & (1 << (channel + 2)))

    def set_relay(self, state: bool) -> None:
        self._modify_io_control(0x10, state)

    def get_relay(self) -> bool:
        return bool(self.get_io_control() & 0x10)

    def set_output_mode(self, mode: int) -> None:
        self._modify_io_control(0x20, mode == self.PWM_MODE)

    def get_output_mode(self) -> int:
        return self.PWM_MODE if self.get_io_control() & 0x20 else self.OUTPUT_IO_MODE

    def get_ina226_config(self, channel: int) -> int:
        self._check_channel(channel)
        return self._read_u16(self._INA226_CONFIG_REG + channel * 2)

    def set_ina226_config(self, channel: int, value: int) -> None:
        self._check_channel(channel)
        self._write_u16(self._INA226_CONFIG_REG + channel * 2, value)

    def set_pwm_config(self, channel: int, freq: int, duty: int) -> None:
        self._check_channel(channel)
        if freq < 1 or freq > 100:
            raise ValueError("freq must be 1~100")
        if duty < 0 or duty > 1000:
            raise ValueError("duty must be 0~1000")
        self.i2c.writeto_mem(self.address, self._PWM_FREQ_REG, bytes([freq]))
        self._write_u16(self._PWM_DUTY_REG + channel * 2, duty)

    def get_pwm_config(self, channel: int) -> tuple:
        self._check_channel(channel)
        freq = self.i2c.readfrom_mem(self.address, self._PWM_FREQ_REG, 1)[0]
        duty = self._read_u16(self._PWM_DUTY_REG + channel * 2)
        return freq, duty

    def get_firmware_version(self) -> int:
        return self.i2c.readfrom_mem(self.address, self._FIRMWARE_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> int:
        return self.i2c.readfrom_mem(self.address, self._I2C_ADDRESS_REG, 1)[0] & 0x7F

    def refresh_i2c_address(self) -> None:
        address = self.get_i2c_address()
        self.i2c.writeto_mem(self.address, self._I2C_ADDRESS_REG, bytes([address | 0x80]))
        self.address = address
