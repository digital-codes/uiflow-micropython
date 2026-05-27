# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# StampS3 startup script
import M5
import time
import network
import machine
import binascii
import M5Things
from startup import Startup
from hardware import RGB


class NullRGB:
    def fill_color(self, color: int) -> None:
        pass

    def set_brightness(self, brightness: int) -> None:
        pass


# Headless startup menu
class Headless_Startup:
    COLOR_RED = 0xFF0000  # WiFi not connected
    COLOR_BLUE = 0x0000FF  # WiFi connected, server not connected
    COLOR_GREEN = 0x00FF00  # WiFi connected, server connected

    def __init__(self) -> None:
        has_rgb = M5.getBoard() not in [M5.BOARD.M5AtomS3R_CAM, M5.BOARD.M5AtomEchoS3R]
        self.rgb = RGB() if has_rgb else NullRGB()
        self.rgb.fill_color(self.COLOR_BLUE)
        self.rgb.set_brightness(50)

    def show_hits(self, hits: str) -> None:
        pass

    def show_msg(self, msg: str) -> None:
        pass

    def show_ssid(self, ssid: str) -> None:
        pass

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print("Mac: " + mac[0:6] + "_" + mac[6:])

    def show_error(self, ssid: str, error: str) -> None:
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def startup(
        self,
        net_mode: str = "WIFI",
        ssid: str = "",
        pswd: str = "",
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self.show_mac()
        self.rgb.set_brightness(100)

        self._net_if = Startup(network_type=net_mode)  # type: ignore
        if self._net_if.connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            print("Connecting to " + ssid + " ", end="")
            start = time.ticks_ms()
            success = False
            while time.ticks_diff(time.ticks_ms(), start) < timeout * 1000:
                status = self._net_if.connect_status()
                if status is network.STAT_GOT_IP:
                    access_code = M5Things.accesscode()
                    if access_code != "":
                        print(" ")
                        print("Local IP: " + self._net_if.local_ip())
                        print("=======================")
                        print("Nick Name: " + M5Things.nick_name())
                        print("Access Code: " + access_code)
                        print("=======================")
                        self.rgb.fill_color(self.COLOR_GREEN)
                        success = True
                        break
                    else:
                        print(".", end="")
                else:
                    print(".", end="")
                time.sleep(1)

            if not success:
                print(" ")
                self.rgb.fill_color(self.COLOR_RED)
                self.show_error(ssid, "TIMEOUT")
                print(
                    f"[NET]: {self._net_if.wifi_status_str(status)} | "
                    f"[MQTT]: {self._net_if.m5things_status_str(M5Things.status())}"
                )
        else:
            self.rgb.fill_color(self.COLOR_RED)
            self.show_error("Not Found", "Please use M5Burner setup :)")
