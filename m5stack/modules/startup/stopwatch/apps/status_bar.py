# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
from ..layout import SCREEN_W, sx, sy, FONT_SMALL, draw_image, is_wifi_connected
import widgets
import time
import asyncio


try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class NetworkStatus:
    INIT = 0
    RSSI_GOOD = 1
    RSSI_MID = 2
    RSSI_WORSE = 3
    DISCONNECTED = 4


class CloudStatus:
    INIT = 0
    CONNECTED = 1
    DISCONNECTED = 2


_WIFI_STATUS_ICO = {
    NetworkStatus.INIT: res.WIFI_EMPTY_IMG,
    NetworkStatus.RSSI_GOOD: res.WIFI_GOOD_IMG,
    NetworkStatus.RSSI_MID: res.WIFI_MID_IMG,
    NetworkStatus.RSSI_WORSE: res.WIFI_WORSE_IMG,
    NetworkStatus.DISCONNECTED: res.WIFI_DISCONNECTED_IMG,
}

_CLOUD_STATUS_ICOS = {
    CloudStatus.INIT: res.SERVER_EMPTY_IMG,
    CloudStatus.CONNECTED: res.SERVER_GREEN_IMG,
    CloudStatus.DISCONNECTED: res.SERVER_ERROR_IMG,
}


class StatusBarApp(app_base.AppBase):
    def __init__(self, icos: dict, wifi, time_y=None) -> None:
        self._wifi = wifi
        self._time_y = sy(31) if time_y is None else time_y

    def on_launch(self):
        self._time_text = self._get_local_time_text()
        self._network_status = self._get_network_status()
        self._cloud_status = self._get_cloud_status()

    def on_view(self):
        # Compact clock centered at the top, on the header grey band
        self._time_label = widgets.Label(
            "12:23",
            SCREEN_W // 2,
            self._time_y,
            w=SCREEN_W,
            h=40,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xEEEEEF,
            font=FONT_SMALL,
        )
        self._time_label.set_text(self._time_text)

        self._draw_network_icon()
        self._draw_server_icon()

    def _draw_network_icon(self):
        draw_image(_WIFI_STATUS_ICO[self._network_status], 46, 29)

    def _draw_server_icon(self):
        draw_image(_CLOUD_STATUS_ICOS[self._cloud_status], 179, 29)

    async def on_run(self):
        while True:
            t = self._get_local_time_text()
            if t != self._time_text:
                self._time_label.set_text(t)
                self._time_text = t

            t = self._get_network_status()
            if t != self._network_status:
                self._network_status = t
                self._draw_network_icon()

            t = self._get_cloud_status()
            if t != self._cloud_status:
                self._cloud_status = t
                self._draw_server_icon()

            await asyncio.sleep_ms(5000)

    def _update_time(self, struct_time):
        self._time_label.set_text("{:02d}:{:02d}".format(struct_time[3], struct_time[4]))

    def _update_wifi(self, status):
        self._network_status = status
        self._draw_network_icon()

    def _update_server(self, status):
        self._cloud_status = status
        self._draw_server_icon()

    @staticmethod
    def _get_local_time_text():
        struct_time = time.localtime()
        return "{:02d}:{:02d}".format(struct_time[3], struct_time[4])

    def _get_network_status(self):
        if not is_wifi_connected(self._wifi):
            return NetworkStatus.DISCONNECTED
        rssi = self._wifi.get_rssi()
        if rssi <= -80:
            return NetworkStatus.RSSI_WORSE
        if rssi <= -60:
            return NetworkStatus.RSSI_MID
        return NetworkStatus.RSSI_GOOD

    @staticmethod
    def _get_cloud_status():
        if _HAS_SERVER is True:
            status = M5Things.status()
            return {
                -2: CloudStatus.DISCONNECTED,
                -1: CloudStatus.DISCONNECTED,
                0: CloudStatus.INIT,
                1: CloudStatus.INIT,
                2: CloudStatus.CONNECTED,
                3: CloudStatus.DISCONNECTED,
            }[status]
        else:
            return CloudStatus.DISCONNECTED
