# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# UnitC6L startup script
import M5
import time
import network
import machine
import binascii
import asyncio
from . import Startup

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


_FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01111", "10000", "10000", "10000", "01111"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11100", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "10110", "11001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    "q": ("00000", "00000", "01111", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10001", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "10000", "11110", "00001", "00001", "11110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
}


def _measure_text(text):
    return 0 if not text else len(text) * 6 - 1


def _draw_bitmap_text(text, x, y, fg_color, bg_color):
    for ch in text:
        rows = _FONT.get(ch, _FONT["?"])
        M5.Lcd.fillRect(x, y, 5, 7, bg_color)
        for yy in range(7):
            row = rows[yy]
            for xx in range(5):
                if row[xx] == "1":
                    M5.Lcd.fillRect(x + xx, y + yy, 1, 1, fg_color)
        x += 6


def _draw_textbox(x, y, w, h, r, text, invert=False, is_title=False):
    text = "" if text is None else str(text)
    max_chars = 8
    if len(text) > max_chars:
        if is_title:
            text = text[:3] + "..." + text[-3:]
        else:
            text = text[:3] + ".." + text[-3:]
    text_w = _measure_text(text)
    cursor_x = x + (w - text_w) // 2
    cursor_y = y + (6 if is_title else 4)
    if invert:
        M5.Lcd.fillRoundRect(x, y, w, h, r, M5.Lcd.COLOR.WHITE)
        fg_color = M5.Lcd.COLOR.BLACK
        bg_color = M5.Lcd.COLOR.WHITE
    else:
        M5.Lcd.fillRoundRect(x, y, w, h, r, M5.Lcd.COLOR.BLACK)
        M5.Lcd.drawRoundRect(x, y, w, h, r, M5.Lcd.COLOR.WHITE)
        fg_color = M5.Lcd.COLOR.WHITE
        bg_color = M5.Lcd.COLOR.BLACK
    _draw_bitmap_text(text, cursor_x, cursor_y, fg_color, bg_color)


def title_set_text(text, invert=False):
    _draw_textbox(0, -3, 64, 18, 4, text, invert, is_title=True)


def label1_set_text(text, invert=False):
    _draw_textbox(3, 16, 58, 15, 4, text, invert, is_title=False)


def label2_set_text(text, invert=False):
    _draw_textbox(3, 32, 58, 15, 4, text, invert, is_title=False)


class InfoPages:
    def __init__(self, wifi, ssid) -> None:
        self._wifi = wifi
        self._ssid = ssid
        self._page = 0
        self._last_state = None
        self._last_pair_code = None
        self._last_nick_name = None
        self._last_refresh_ms = 0

    async def start(self):
        self._draw_current_page()
        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                try:
                    M5.Speaker.tone(666, 100)
                except Exception:
                    pass
                self._page = (self._page + 1) % 3
                self._draw_current_page()
            else:
                self._refresh_current_page()
            await asyncio.sleep_ms(100)

    def _draw_current_page(self):
        if self._page == 0:
            self._draw_wifi_page()
        elif self._page == 1:
            self._draw_access_code_page()
        else:
            self._draw_nickname_page()

    def _refresh_current_page(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_refresh_ms) < 1500:
            return
        self._last_refresh_ms = now
        if self._page == 0:
            state = self._wifi.connect_status()
            if state != self._last_state:
                self._draw_wifi_page()
        elif self._page == 1:
            pair_code = self._get_pair_code() or "None"
            if pair_code != self._last_pair_code:
                self._draw_access_code_page()
        else:
            nick_name = self._get_nick_name() or "None"
            if nick_name != self._last_nick_name:
                self._draw_nickname_page()

    def _draw_wifi_page(self):
        self._last_state = self._wifi.connect_status()
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        title_set_text("WiFi", False)
        label1_set_text(str(self._ssid) if self._ssid else "None", False)
        label2_set_text(self._get_wifi_status_text(), False)

    def _draw_access_code_page(self):
        self._last_pair_code = self._get_pair_code() or "None"
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        title_set_text("Access", False)
        label1_set_text("Code", False)
        label2_set_text(self._last_pair_code, False)

    def _draw_nickname_page(self):
        self._last_nick_name = self._get_nick_name() or "None"
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        title_set_text("Nickname", False)
        label1_set_text(self._last_nick_name, False)
        label2_set_text("", False)

    def _get_wifi_status_text(self):
        return {
            network.STAT_GOT_IP: "ONLINE",
            network.STAT_CONNECTING: "CONNECT",
            network.STAT_NO_AP_FOUND: "NO AP",
            network.STAT_WRONG_PASSWORD: "WRONG",
            network.STAT_HANDSHAKE_TIMEOUT: "TIMEOUT",
        }.get(self._wifi.connect_status(), "OFFLINE")

    @staticmethod
    def _get_pair_code():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_nick_name():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""


# UnitC6L startup menu
class UnitC6L_Startup(Startup):
    def __init__(self) -> None:
        super().__init__()

    def show_hits(self, hits: str) -> None:
        print(hits)

    def show_msg(self, msg: str) -> None:
        print(msg)

    def show_ssid(self, ssid: str) -> None:
        if len(ssid) > 9:
            self.show_msg(ssid[:7] + "...")
        else:
            self.show_msg(ssid)

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print(mac[0:6] + "_" + mac[6:])

    def show_error(self, ssid: str, error: str) -> None:
        self.show_ssid(ssid)
        self.show_hits(error)
        self.show_mac()
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        M5.Speaker.begin()
        M5.Speaker.setVolumePercentage(1)
        # 显示启动画面
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        M5.Lcd.fillRect(0, 0, 64, 15, M5.Lcd.COLOR.WHITE)
        _draw_bitmap_text(
            "UiFlow2",
            (64 - _measure_text("UiFlow2")) // 2,
            7,
            M5.Lcd.COLOR.BLACK,
            M5.Lcd.COLOR.WHITE,
        )
        _draw_bitmap_text(
            "Unit C6L",
            (64 - _measure_text("Unit C6L")) // 2,
            29,
            M5.Lcd.COLOR.WHITE,
            M5.Lcd.COLOR.BLACK,
        )
        M5.Speaker.tone(888, 200)
        self.show_mac()
        # 连接网络
        if super().connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            self.show_ssid(ssid)
            count = 1
            status = super().connect_status()
            start = time.time()
            while status is not network.STAT_GOT_IP:
                time.sleep_ms(300)
                if status is network.STAT_NO_AP_FOUND:
                    self.show_error(ssid, "NO AP FOUND")
                    break
                elif status is network.STAT_WRONG_PASSWORD:
                    self.show_error(ssid, "WRONG PASSWORD")
                    break
                elif status is network.STAT_HANDSHAKE_TIMEOUT:
                    self.show_error(ssid, "HANDSHAKE ERR")
                    break
                elif status is network.STAT_CONNECTING:
                    self.show_hits("." * count)
                    count = count + 1
                    if count > 5:
                        count = 1
                status = super().connect_status()
                # connect to network timeout
                if (time.time() - start) > timeout:
                    self.show_error(ssid, "TIMEOUT")
                    break

            if status is network.STAT_GOT_IP:
                self.show_hits(super().local_ip())
                print("Local IP: " + super().local_ip())
        else:
            self.show_error("Not Found", "Use Burner setup")
        self._start_menu_system(ssid)

    def _start_menu_system(self, ssid):
        """Start the simple info page switcher."""
        try:
            pages = InfoPages(self, ssid)
            asyncio.run(pages.start())
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Info page error: {e}")
