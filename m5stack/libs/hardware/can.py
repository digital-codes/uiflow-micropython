# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import m5can
import sys

if sys.platform != "esp32":
    from typing import Literal


class CAN(m5can.CAN):
    _timing_table = {
        # prescaler, sjw, bs1, bs2, triple_sampling
        25000: (128, 3, 16, 8, False),
        50000: (80, 3, 15, 4, False),
        100000: (40, 3, 15, 4, False),
        125000: (32, 3, 15, 4, False),
        250000: (16, 3, 15, 4, False),
        500000: (8, 3, 15, 4, False),
        800000: (4, 3, 16, 8, False),
        1000000: (4, 3, 15, 4, False),
    }

    def __init__(
        self,
        id: Literal[0, 1],
        mode: int = m5can.CAN.NORMAL,
        tx: int = 0,
        rx: int = 0,
        *args,
    ):
        if len(args) == 1:
            (prescaler, sjw, bs1, bs2, triple_sampling) = self._timing_table.get(args[0])
        elif len(args) == 5:
            (prescaler, sjw, bs1, bs2, triple_sampling) = args

        super().__init__(
            0,
            mode,
            tx,
            rx,
            prescaler,
            sjw,
            bs1,
            bs2,
            triple_sampling,
        )
