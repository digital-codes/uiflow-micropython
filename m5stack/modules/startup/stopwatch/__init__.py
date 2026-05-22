# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup
import M5
from . import framework
from .apps.settings import SettingsApp, WiFiSetting
from .apps.dev import DevApp
import time
from . import res
from .layout import draw_image


class StopWatch_Startup:
    def __init__(self) -> None:
        self._wlan = Startup()

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
        self._wlan.connect_network(
            ssid, pswd, protocol=protocol, ip=ip, netmask=netmask, gateway=gateway, dns=dns
        )
        M5.Power.setExtOutput(False)
        M5.Speaker.setVolume(90)
        M5.Speaker.tone(4000, 50)

        draw_image(res.LOGO_IMG, 0, 0)
        time.sleep_ms(500)

        fw = framework.Framework()
        dev_app = DevApp(None, data=self._wlan)
        wifi_app = WiFiSetting(None, data=self._wlan)
        setting_app = SettingsApp(None, data=self._wlan)
        fw.install_launcher(dev_app)
        fw.install(dev_app)
        fw.install(wifi_app)
        fw.install(setting_app)
        fw.start()
