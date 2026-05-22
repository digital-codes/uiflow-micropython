# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# StopWatch UI assets live under /system/stopwatch/ (BOARD_TYPE=stopwatch in Makefile).

_attrs = {
    "LOGO_IMG": "/system/stopwatch/boot/boot_logo_1.jpg",
    "DEVELOP_ONLINE_IMG": "/system/stopwatch/page_develop/page_develop_oneline.jpg",
    "DEVELOP_OFFLINE_IMG": "/system/stopwatch/page_develop/page_develop_offline.jpg",
    "SETTING_COMMON_IMG": "/system/stopwatch/page_setting_common/page_setting_common.jpg",
    "BOOT_IMG": "/system/stopwatch/page_setting_common/boot_screen_label.jpg",
    "BOOT_NO_IMG": "/system/stopwatch/page_setting_common/boot_screen_no.jpg",
    "BOOT_YES_IMG": "/system/stopwatch/page_setting_common/boot_screen_yes.jpg",
    "COMX_IMG": "/system/stopwatch/page_setting_common/comx_label.jpg",
    "COMX_DISABLE_IMG": "/system/stopwatch/page_setting_common/comx_disable.jpg",
    "COMX_ENABLE_IMG": "/system/stopwatch/page_setting_common/comx_enable.jpg",
    "SCREEN_IMG": "/system/stopwatch/page_setting_common/screen_brightness.jpg",
    "SCREEN25_IMG": "/system/stopwatch/page_setting_common/screen_brightness_25.jpg",
    "SCREEN50_IMG": "/system/stopwatch/page_setting_common/screen_brightness_50.jpg",
    "SCREEN75_IMG": "/system/stopwatch/page_setting_common/screen_brightness_75.jpg",
    "SCREEN100_IMG": "/system/stopwatch/page_setting_common/screen_brightness_100.jpg",
    "SETTING_WIFI_IMG": "/system/stopwatch/page_setting_wifi/page_setting_wifi.jpg",
    "WIFI_DEFAULT_IMG": "/system/stopwatch/page_setting_wifi/wifiServer.jpg",
    "WIFI_SSID_IMG": "/system/stopwatch/page_setting_wifi/panel_ssid.jpg",
    "WIFI_PSK_IMG": "/system/stopwatch/page_setting_wifi/panel_pass.jpg",
    "WIFI_SERVER_IMG": "/system/stopwatch/page_setting_wifi/panel_server.jpg",
    "SERVER_EMPTY_IMG": "/system/stopwatch/cloud/server_empty.jpg",
    "SERVER_ERROR_IMG": "/system/stopwatch/cloud/server_error.jpg",
    "SERVER_GREEN_IMG": "/system/stopwatch/cloud/Server_Green.jpg",
    "WIFI_DISCONNECTED_IMG": "/system/stopwatch/wifi/wifi_disconnected.jpg",
    "WIFI_EMPTY_IMG": "/system/stopwatch/wifi/wifi_empty.jpg",
    "WIFI_GOOD_IMG": "/system/stopwatch/wifi/wifi_good.jpg",
    "WIFI_MID_IMG": "/system/stopwatch/wifi/wifi_mid.jpg",
    "WIFI_WORSE_IMG": "/system/stopwatch/wifi/wifi_worse.jpg",
    "AVATAR_IMG": "/system/common/img/avatar.jpg",
    "USER_AVATAR_PATH": "/system/common/img/",
}


def __getattr__(attr):
    value = _attrs.get(attr, None)
    if value is None:
        raise AttributeError(attr)
    globals()[attr] = value
    return value
