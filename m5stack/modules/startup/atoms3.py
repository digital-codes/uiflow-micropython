# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# AtomS3 startup script
import M5
import time
import network
import machine
import binascii
from . import Startup

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

# AtomS3 startup menu


class AtomS3_Startup(Startup):
    _BLACK = 0x000000
    _WHITE = 0xF5F5F5
    _ONLINE = 0x26E66F
    _OFFLINE = 0xF6D340
    _UIFLOW_BLUE = 0x008FD7

    def __init__(self) -> None:
        super().__init__()

    def show_ssid(self, ssid: str) -> None:
        self._draw_wifi(ssid)

    def show_mac(self) -> None:
        mac = self._get_mac()
        self._draw_text_line("MAC:" + mac, 1, 41)

    def show_error(self, ssid: str, error: str) -> None:
        self.show_ssid(ssid)
        self.show_access_code("")
        self.show_status(False)
        self.show_mac()
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def show_nick_name(self, nick_name: str) -> None:
        self._draw_text_line("Nickname:", 1, 94)
        self._draw_value_line("  " + self._short_text(nick_name, 13), 1, 111)

    def show_access_code(self, access_code: str) -> None:
        self._draw_text_line("Accesscode:", 1, 58)
        self._draw_value_line("  " + self._short_text(access_code, 14), 1, 75)

    def show_status(self, is_online: bool) -> None:
        bg = self._ONLINE if is_online else self._OFFLINE
        state = "ON" if is_online else "OFF"
        M5.Lcd.fillRect(0, 0, 128, 24, self._BLACK)
        M5.Lcd.fillRect(2, 2, 124, 20, bg)
        M5.Lcd.drawRect(0, 0, 128, 24, self._UIFLOW_BLUE)
        M5.Lcd.drawRect(1, 1, 126, 22, self._UIFLOW_BLUE)
        self._set_text_color(self._BLACK, bg)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat12)
        M5.Lcd.drawString("UiFlow2", 13, 6)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat14)
        M5.Lcd.drawString(state, 92, 5)

    def show_layout(self, ssid: str) -> None:
        M5.Lcd.clear(self._BLACK)
        self.show_status(False)
        self._draw_wifi(ssid)
        self.show_mac()
        self.show_access_code("")
        self.show_nick_name("")

    def _draw_wifi(self, ssid: str) -> None:
        self._draw_text_line("WiFi:" + self._short_text(ssid, 12), 1, 26)

    def _draw_text_line(self, text: str, x: int, y: int) -> None:
        M5.Lcd.fillRect(x, y, 128 - x, 14, self._BLACK)
        self._set_text_color(self._WHITE, self._BLACK)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat12)
        M5.Lcd.drawString(text, x, y)

    def _draw_value_line(self, text: str, x: int, y: int) -> None:
        M5.Lcd.fillRect(x, y, 128 - x, 16, self._BLACK)
        self._set_text_color(self._WHITE, self._BLACK)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat14)
        M5.Lcd.drawString(text, x, y)

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
        self.show_layout(ssid)

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
            start = time.ticks_ms()
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
                    self.show_access_code("." * count)
                    count = count + 1
                    if count > 5:
                        count = 1
                status = super().connect_status()
                # connect to network timeout
                if time.ticks_diff(time.ticks_ms(), start) > timeout * 1000:
                    self.show_error(ssid, "TIMEOUT")
                    break

            if status is network.STAT_GOT_IP:
                print("Local IP: " + super().local_ip())
                self._wait_server(ssid, start, timeout)
        else:
            self.show_error("Not Found", "Use Burner setup")

    def _wait_server(self, ssid: str, start: int, timeout: int) -> None:
        count = 1
        while time.ticks_diff(time.ticks_ms(), start) <= timeout * 1000:
            access_code = self._get_access_code()
            if self._is_server_online() and access_code != "":
                nick_name = self._get_nick_name()
                self.show_access_code(access_code)
                self.show_nick_name(nick_name)
                self.show_status(True)
                print("=======================")
                print("Nick Name: " + nick_name)
                print("Access Code: " + access_code)
                print("=======================")
                return

            self.show_access_code("." * count)
            count = count + 1
            if count > 5:
                count = 1
            time.sleep_ms(1000)

        self.show_error(ssid, "TIMEOUT")
        if _HAS_SERVER:
            try:
                print("[MQTT]: " + self.m5things_status_str(M5Things.status()))
            except Exception:
                print("[MQTT]: UNKNOWN")
        else:
            print("[MQTT]: M5Things unavailable")

    @staticmethod
    def _get_mac() -> str:
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

    @staticmethod
    def _get_nick_name() -> str:
        if _HAS_SERVER:
            try:
                return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_access_code() -> str:
        if _HAS_SERVER:
            for name in ("accesscode", "paircode"):
                try:
                    func = getattr(M5Things, name)
                    code = func()
                    if code:
                        return code
                except Exception:
                    pass
        return ""

    @staticmethod
    def _is_server_online() -> bool:
        if _HAS_SERVER:
            try:
                return M5Things.status() == 2
            except Exception:
                pass
        return False

    @staticmethod
    def _short_text(text: str, max_len: int) -> str:
        if text is None:
            return ""
        text = str(text)
        return text if len(text) <= max_len else text[: max_len - 3] + "..."

    @staticmethod
    def _set_text_color(fg: int, bg: int) -> None:
        try:
            M5.Lcd.setTextColor(fg, bg)
        except TypeError:
            M5.Lcd.setTextColor(fg)
