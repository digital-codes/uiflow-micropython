# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.ir.nec import NEC, NEC_8
import M5
import machine


class IR:
    def __init__(self) -> None:
        _pin_map = {
            M5.BOARD.M5AtomS3: (None, 4),
            M5.BOARD.M5AtomS3Lite: (None, 4),
            M5.BOARD.M5AtomS3U: (None, 12),
            M5.BOARD.M5Capsule: (None, 4),
            M5.BOARD.M5Cardputer: (None, 44),
            M5.BOARD.M5StickCPlus: (None, 9),
            M5.BOARD.M5StickC: (None, 9),
            M5.BOARD.M5StickCPlus2: (None, 19),
            M5.BOARD.M5AtomU: (None, 12),
            M5.BOARD.M5Atom: (None, 12),
            M5.BOARD.M5AtomEcho: (None, 12),
            M5.BOARD.M5NanoC6: (None, 3),
        }
        (self._rx_pin, self._tx_pin) = _pin_map.get(M5.getBoard())
        if self._tx_pin:
            self._transmitter = NEC(machine.Pin(self._tx_pin, machine.Pin.OUT, value=0))
        self._receiver = None

    def tx(self, cmd, data):
        self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._rx_pin is None:
            raise NotImplementedError("IR receiver is not supported on this board")

        if self._receiver:
            self._receiver.close()

        self._receiver = NEC_8(machine.Pin(self._rx_pin, machine.Pin.IN), cb)
