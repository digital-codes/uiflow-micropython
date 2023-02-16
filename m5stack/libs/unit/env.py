# -*- encoding: utf-8 -*-
# ENV I/II/III
from . import UnitError
from .pahub import PAHUB
from machine import I2C
from micropython import const
from driver.sht30 import SHT30
from driver.bmp280 import BMP280
from driver.qmp6988 import QMP6988
from driver.dht12 import DHT12

try:
    from typing import Union
    from typing_extensions import Literal
except ImportError:
    pass

ENV_I = const(1)
ENV_II = const(2)
ENV_III = const(3)


class ENV:
    _temp_humid = None
    _pressure = None

    def __init__(self, i2c: Union[I2C, PAHUB], type: Literal[1, 2, 3]) -> None:
        if type == ENV_I:
            self._temp_humid = DHT12(i2c=i2c)
            self._pressure = BMP280(i2c=i2c)
        elif type == ENV_II:
            self._temp_humid = SHT30(i2c=i2c)
            self._pressure = BMP280(i2c=i2c)
        elif type == ENV_III:
            self._temp_humid = SHT30(i2c=i2c)
            self._pressure = QMP6988(i2c=i2c)
        else:
            raise UnitError("Unknow ENV type")

    def read_temperature(self) -> float:
        return round(self._temp_humid.measure()[0], 2)

    def read_humidity(self) -> float:
        return round(self._temp_humid.measure()[1], 2)

    def read_pressure(self) -> float:
        return round(self._pressure.measure()[1], 2)
