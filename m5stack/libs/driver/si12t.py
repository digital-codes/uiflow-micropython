# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Si12T I2C configuration
SI12T_I2C_ADDR = 0x68  # 7-bit I2C address

# Si12T register addresses
SI12T_SENSITIVITY1_ADDR = 0x02
SI12T_SENSITIVITY2_ADDR = 0x03
SI12T_SENSITIVITY3_ADDR = 0x04
SI12T_SENSITIVITY4_ADDR = 0x05
SI12T_SENSITIVITY5_ADDR = 0x06
SI12T_SENSITIVITY6_ADDR = 0x07
SI12T_CTRL1_ADDR = 0x08
SI12T_CTRL2_ADDR = 0x09
SI12T_REF_RST1_ADDR = 0x0A
SI12T_REF_RST2_ADDR = 0x0B
SI12T_CH_HOLD1_ADDR = 0x0C
SI12T_CH_HOLD2_ADDR = 0x0D
SI12T_CAL_HOLD1_ADDR = 0x0E
SI12T_CAL_HOLD2_ADDR = 0x0F
SI12T_OUTPUT1_ADDR = 0x10
SI12T_OUTPUT2_ADDR = 0x11
SI12T_OUTPUT3_ADDR = 0x12

# touch type enumeration
OUTPUT_NONE = 0
OUTPUT_LOW = 1
OUTPUT_MID = 2
OUTPUT_HIGH = 3

# sensitivity type
SI12T_TYPE_LOW = 0
SI12T_TYPE_HIGH = 1

# sensitivity level
SI12T_SENSITIVITY_LEVEL_0 = 0
SI12T_SENSITIVITY_LEVEL_1 = 1
SI12T_SENSITIVITY_LEVEL_2 = 2
SI12T_SENSITIVITY_LEVEL_3 = 3
SI12T_SENSITIVITY_LEVEL_4 = 4
SI12T_SENSITIVITY_LEVEL_5 = 5
SI12T_SENSITIVITY_LEVEL_6 = 6
SI12T_SENSITIVITY_LEVEL_7 = 7


class Si12T:
    def __init__(
        self,
        i2c,
        addr=SI12T_I2C_ADDR,
        sens_type=SI12T_TYPE_LOW,
        sens_level=SI12T_SENSITIVITY_LEVEL_0,
    ):
        self.i2c = i2c
        self.addr = addr
        self.sens_type = sens_type
        self.sens_level = sens_level
        self.touch_result = 0
        self.point_type = [OUTPUT_NONE, OUTPUT_NONE, OUTPUT_NONE]
        self.enable_channel()
        self.set_ctrl2()
        self.set_ctrl1()
        self.set_sensitivity(self.sens_type, self.sens_level)

    def _write_register(self, reg_addr, value):
        try:
            self.i2c.writeto_mem(self.addr, reg_addr, bytes([value]))
            return True
        except:
            return False

    def _read_register(self, reg_addr):
        try:
            data = self.i2c.readfrom_mem(self.addr, reg_addr, 1)
            return data[0]
        except:
            return None

    def enable_channel(self):
        """使能通道"""
        # channel 1-8 enable reference calibration
        self._write_register(SI12T_REF_RST1_ADDR, 0x00)
        # channel 9 enable reference calibration
        self._write_register(SI12T_REF_RST2_ADDR, 0x00)

        # channel 1-8 enable
        self._write_register(SI12T_CH_HOLD1_ADDR, 0x00)
        # channel 9 enable
        self._write_register(SI12T_CH_HOLD2_ADDR, 0x00)

        # channel 1-8 enable reference calibration
        self._write_register(SI12T_CAL_HOLD1_ADDR, 0x00)
        # channel 9 enable reference calibration
        self._write_register(SI12T_CAL_HOLD2_ADDR, 0x00)

    def set_ctrl1(self):
        self._write_register(SI12T_CTRL1_ADDR, 0x22)

    def set_ctrl2(self):
        self._write_register(SI12T_CTRL2_ADDR, 0x0F)
        self._write_register(SI12T_CTRL2_ADDR, 0x07)

    def set_sens(self, value):
        self._write_register(SI12T_SENSITIVITY1_ADDR, value)
        self._write_register(SI12T_SENSITIVITY2_ADDR, value)
        self._write_register(SI12T_SENSITIVITY3_ADDR, value)
        self._write_register(SI12T_SENSITIVITY4_ADDR, value)
        self._write_register(SI12T_SENSITIVITY5_ADDR, value)

    def set_sensitivity(self, sens_type, sens_level):
        if sens_type < SI12T_TYPE_LOW or sens_type > SI12T_TYPE_HIGH:
            return -1
        if sens_level < 0 or sens_level > 7:
            return -1
        # calculate value based on type and level
        if sens_type == SI12T_TYPE_HIGH:
            value = 0x88 + (sens_level * 0x11)
        else:
            value = sens_level * 0x11
        self.set_sens(value)
        return 0

    def read_touch_result(self):
        value = self._read_register(SI12T_OUTPUT1_ADDR)
        if value is not None:
            self.touch_result = value
            return True
        return False

    def parse_touch_result(self):
        self.point_type = [OUTPUT_NONE, OUTPUT_NONE, OUTPUT_NONE]
        for i in range(3):
            # bit 0-1: point 0, bit 2-3: point 1, bit 4-5: point 2
            self.point_type[i] = (self.touch_result >> (i * 2)) & 0x03

    def get_touch_status(self):
        if self.read_touch_result():
            self.parse_touch_result()
            return self.point_type.copy()
        return None

    def sleep_enable(self):
        """enable sleep mode"""
        self._write_register(SI12T_CTRL2_ADDR, 0x07)

    def sleep_disable(self):
        """disable sleep mode"""
        self._write_register(SI12T_CTRL2_ADDR, 0x03)
