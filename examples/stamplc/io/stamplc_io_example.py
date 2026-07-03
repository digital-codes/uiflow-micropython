# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from stamplc import IOStamPLC
from stamplc import StamPLC


title0 = None
label0 = None
label1 = None
stamplc_0 = None
stamplc_io_0 = None


def setup():
    global title0, label0, label1, stamplc_0, stamplc_io_0

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("StamPLC IO Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18)
    label0 = Widgets.Label("label0", 1, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label1 = Widgets.Label("label1", 2, 71, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    stamplc_0 = StamPLC()
    stamplc_io_0 = IOStamPLC(address=0x20)
    stamplc_io_0.set_output_mode(IOStamPLC.PWM_MODE)
    stamplc_io_0.set_pwm_config(0, 1, 100)
    stamplc_io_0.set_pwm_config(1, 1, 100)


def loop():
    global title0, label0, label1, stamplc_0, stamplc_io_0
    M5.update()
    label0.setText(
        str(
            (
                str("ch0:")
                + str(
                    (
                        str((stamplc_io_0.get_voltage(0)))
                        + str(
                            (
                                str("mV")
                                + str(
                                    (
                                        str(", ")
                                        + str((str((stamplc_io_0.get_current(0))) + str("uA")))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    label1.setText(
        str(
            (
                str("ch1:")
                + str(
                    (
                        str((stamplc_io_0.get_voltage(1)))
                        + str(
                            (
                                str("mV")
                                + str(
                                    (
                                        str(", ")
                                        + str((str((stamplc_io_0.get_current(1))) + str("uA")))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
