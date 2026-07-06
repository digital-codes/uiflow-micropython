# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
from micropython import const
from module.mbus import i2c1


BASEX_ADDR = const(0x22)

REG_SERVO1_ANGLE = const(0x00)
REG_SERVO2_ANGLE = const(0x01)
REG_SERVO1_PULSE = const(0x10)
REG_SERVO2_PULSE = const(0x12)

REG_MOTOR1_PWM_DUTY = const(0x20)
REG_MOTOR2_PWM_DUTY = const(0x21)
REG_MOTOR3_PWM_DUTY = const(0x22)
REG_MOTOR4_PWM_DUTY = const(0x23)

REG_MOTOR1_ENCODER = const(0x30)
REG_MOTOR2_ENCODER = const(0x34)
REG_MOTOR3_ENCODER = const(0x38)
REG_MOTOR4_ENCODER = const(0x3C)

REG_MOTOR1_SPEED_20MS = const(0x40)
REG_MOTOR2_SPEED_20MS = const(0x41)
REG_MOTOR3_SPEED_20MS = const(0x42)
REG_MOTOR4_SPEED_20MS = const(0x43)

REG_MOTOR1_CONFIG = const(0x50)
REG_MOTOR2_CONFIG = const(0x60)
REG_MOTOR3_CONFIG = const(0x70)
REG_MOTOR4_CONFIG = const(0x80)

MOTOR_COUNT = const(4)
SERVO_COUNT = const(2)


class ModuleBaseX:
    """Create an ModuleBaseX object.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import ModuleBaseX

            basex_0 = ModuleBaseX()
    """

    MOTOR_MODE_NORMAL = const(0x00)
    MOTOR_MODE_POSITION = const(0x01)
    MOTOR_MODE_SPEED = const(0x02)

    _SERVO_ANGLE_REG = (REG_SERVO1_ANGLE, REG_SERVO2_ANGLE)
    _SERVO_PULSE_REG = (REG_SERVO1_PULSE, REG_SERVO2_PULSE)
    _MOTOR_PWM_DUTY_REG = (
        REG_MOTOR1_PWM_DUTY,
        REG_MOTOR2_PWM_DUTY,
        REG_MOTOR3_PWM_DUTY,
        REG_MOTOR4_PWM_DUTY,
    )
    _MOTOR_ENCODER_REG = (
        REG_MOTOR1_ENCODER,
        REG_MOTOR2_ENCODER,
        REG_MOTOR3_ENCODER,
        REG_MOTOR4_ENCODER,
    )
    _MOTOR_SPEED_20MS_REG = (
        REG_MOTOR1_SPEED_20MS,
        REG_MOTOR2_SPEED_20MS,
        REG_MOTOR3_SPEED_20MS,
        REG_MOTOR4_SPEED_20MS,
    )
    _MOTOR_CONFIG_REG = (
        REG_MOTOR1_CONFIG,
        REG_MOTOR2_CONFIG,
        REG_MOTOR3_CONFIG,
        REG_MOTOR4_CONFIG,
    )

    def __init__(self) -> None:
        self.i2c = i2c1
        self.basex_addr = BASEX_ADDR
        if self.basex_addr not in self.i2c.scan():
            raise RuntimeError("BaseX Module not found")

    def _get_motor_index(self, channel: int) -> int:
        if not 1 <= channel <= MOTOR_COUNT:
            raise ValueError("motor channel must be 1~4")
        return channel - 1

    def _get_servo_index(self, channel: int) -> int:
        if not 1 <= channel <= SERVO_COUNT:
            raise ValueError("servo channel must be 1~2")
        return channel - 1

    def _check_range(self, value: int, min_value: int, max_value: int, name: str) -> None:
        if not min_value <= value <= max_value:
            raise ValueError("%s must be in range %d~%d" % (name, min_value, max_value))

    def _write_int8(self, reg: int, value: int) -> None:
        self.i2c.writeto_mem(self.basex_addr, reg, struct.pack("b", value))

    def set_servo_angle(self, channel: int, angle: int) -> None:
        """Set servo angle.

        :param int channel: Servo channel. Range: 1 ~ 2.
        :param int angle: Servo angle. Range: 0 ~ 180.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_servo_angle(1, 90)
        """
        index = self._get_servo_index(channel)
        self._check_range(angle, 0, 180, "angle")
        self.i2c.writeto_mem(self.basex_addr, self._SERVO_ANGLE_REG[index], bytes([angle]))

    def set_servo_pulse(self, channel: int, pulse_us: int) -> None:
        """Set servo pulse width.

        :param int channel: Servo channel. Range: 1 ~ 2.
        :param int pulse_us: Pulse width in microseconds. Range: 500 ~ 2500.

        The servo PWM frequency is 50Hz, with a period of 20ms.
        The pulse range 500 ~ 2500us corresponds to about 2.5% ~ 12.5% duty.

        UiFlow2 Code Block:

            |set_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_servo_pulse(1, 1500)
        """
        index = self._get_servo_index(channel)
        self._check_range(pulse_us, 500, 2500, "pulse_us")
        self.i2c.writeto_mem(
            self.basex_addr,
            self._SERVO_PULSE_REG[index],
            struct.pack(">H", pulse_us),
        )

    def set_motor_pwm(self, channel: int, duty: int) -> None:
        """Set motor PWM duty.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int duty: Motor PWM duty. Range: -127 ~ 127.

        The sign indicates direction. ``abs(duty)`` 0 ~ 127 maps to 0% ~ 100% duty.

        UiFlow2 Code Block:

            |set_motor_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_pwm(1, 80)
        """
        index = self._get_motor_index(channel)
        self._check_range(duty, -127, 127, "duty")
        self._write_int8(self._MOTOR_PWM_DUTY_REG[index], duty)

    def get_motor_speed_20ms(self, channel: int) -> int:
        """Get motor speed feedback over 20ms.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :returns: Encoder delta over 20ms.
        :rtype: int

        UiFlow2 Code Block:

            None

        MicroPython Code Block:

            .. code-block:: python

                basex_0.get_motor_speed_20ms(1)
        """
        index = self._get_motor_index(channel)
        data = self.i2c.readfrom_mem(self.basex_addr, self._MOTOR_SPEED_20MS_REG[index], 1)
        return struct.unpack("b", data)[0]

    def get_motor_encoder(self, channel: int) -> int:
        """Get motor encoder value.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :returns: Encoder count as signed 32-bit integer.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_encoder.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.get_motor_encoder(1)
        """
        index = self._get_motor_index(channel)
        data = self.i2c.readfrom_mem(self.basex_addr, self._MOTOR_ENCODER_REG[index], 4)
        return struct.unpack(">i", data)[0]

    def set_motor_encoder(self, channel: int, value: int) -> None:
        """Set motor encoder value.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int value: Encoder count as signed 32-bit integer.

        UiFlow2 Code Block:

            |set_motor_encoder.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_encoder(1, 0)
        """
        index = self._get_motor_index(channel)
        self._check_range(value, -2147483648, 2147483647, "value")
        self.i2c.writeto_mem(
            self.basex_addr,
            self._MOTOR_ENCODER_REG[index],
            struct.pack(">i", value),
        )

    def set_motor_mode(self, channel: int, mode: int) -> None:
        """Set motor control mode.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int mode: Motor mode. ``MOTOR_MODE_NORMAL``, ``MOTOR_MODE_POSITION``
            or ``MOTOR_MODE_SPEED``.

        UiFlow2 Code Block:

            |set_motor_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
        """
        if mode not in (self.MOTOR_MODE_NORMAL, self.MOTOR_MODE_POSITION, self.MOTOR_MODE_SPEED):
            raise ValueError("invalid motor mode")
        self._write_motor_config(channel, 0, bytes([mode]))

    def set_motor_position_pid(self, channel: int, p: int = 3, i: int = 1, d: int = 15) -> None:
        """Set motor position mode PID parameters.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int p: Position P parameter. Default is 3.
        :param int i: Position I parameter. Default is 1.
        :param int d: Position D parameter. Default is 15.

        UiFlow2 Code Block:

            |set_motor_position_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_position_pid(1)
        """
        self._write_motor_config(channel, 1, bytes([p & 0xFF]))
        self._write_motor_config(channel, 2, bytes([i & 0xFF]))
        self._write_motor_config(channel, 3, bytes([d & 0xFF]))

    def set_motor_position_target(self, channel: int, position: int) -> None:
        """Set motor position mode target.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int position: Position target as signed 32-bit integer.

        UiFlow2 Code Block:

            |set_motor_position_target.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_position_target(1, 720)
        """
        self._write_motor_config(channel, 4, struct.pack("<i", position))

    def set_motor_position_max_speed(self, channel: int, speed: int) -> None:
        """Set motor position mode max speed.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int speed: Max speed. Range: -127 ~ 127.

        The sign indicates direction.

        UiFlow2 Code Block:

            |set_motor_position_max_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_position_max_speed(1, 80)
        """
        self._check_range(speed, -127, 127, "speed")
        self._write_motor_config(channel, 8, struct.pack("b", speed))

    def set_motor_speed_pid(self, channel: int, p: int = 3, i: int = 1, d: int = 15) -> None:
        """Set motor speed mode PID parameters.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int p: Speed P parameter. Default is 3.
        :param int i: Speed I parameter. Default is 1.
        :param int d: Speed D parameter. Default is 15.

        UiFlow2 Code Block:

            |set_motor_speed_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_speed_pid(1)
        """
        self._write_motor_config(channel, 9, bytes([p & 0xFF]))
        self._write_motor_config(channel, 10, bytes([i & 0xFF]))
        self._write_motor_config(channel, 11, bytes([d & 0xFF]))

    def set_motor_speed_target(self, channel: int, speed: int) -> None:
        """Set motor speed mode target.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int speed: Speed target. Range: -20 ~ 20.

        The sign indicates direction. The target controls the feedback value returned
        by :meth:`get_motor_speed_20ms`.

        UiFlow2 Code Block:

            |set_motor_speed_target.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_speed_target(1, 20)
        """
        self._check_range(speed, -20, 20, "speed")
        self._write_motor_config(channel, 12, struct.pack("b", speed))

    def _write_motor_config(self, channel: int, bit: int, data: bytes) -> None:
        if not 0 <= bit <= 12:
            raise ValueError("config bit must be 0~12")
        index = self._get_motor_index(channel)
        self.i2c.writeto_mem(self.basex_addr, self._MOTOR_CONFIG_REG[index] + bit, data)
