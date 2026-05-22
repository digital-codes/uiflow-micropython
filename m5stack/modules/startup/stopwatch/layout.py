# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Layout helpers for StopWatch (466x466). Assets are native 466 art; only
# coordinates are scaled from the original 240x240 design grid.

import M5
import network

SCREEN_W = 466
SCREEN_H = 466
DESIGN_W = 240
DESIGN_H = 240
POS_SCALE = SCREEN_W / DESIGN_W  # ~1.9417, layout only
_PAGE_BG_COLOR = 0xFEFEFE


def sx(v):
    return int(v * POS_SCALE)


def sy(v):
    return int(v * POS_SCALE)


def draw_image(src, x=0, y=0):
    """Draw asset at native resolution; x/y use the 240-based design grid."""
    M5.Lcd.drawImage(src, sx(x), sy(y))


def is_wifi_connected(wlan):
    """True when STA has an IP (handles StopWatch coprocessor STAT 1010)."""
    try:
        if wlan.network.isconnected():
            return True
        status = wlan.connect_status()
        return status in (network.STAT_GOT_IP, wlan.STAT_GOT_IP)
    except Exception:
        return False


def draw_page_bg(src):
    """Full-screen page background.

    Always clear the framebuffer first so switching apps cannot leave the
    previous page visible (drawImage alone may skip when the path repeats).
    """
    M5.Lcd.fillRect(0, 0, SCREEN_W, SCREEN_H, _PAGE_BG_COLOR)
    M5.Lcd.drawImage(src, 0, 0)


# Built-in font handles (no VLW file required)
FONT_BIG = M5.Lcd.FONTS.Montserrat40  # titles / hero text
FONT_SMALL = M5.Lcd.FONTS.Montserrat24  # body / input text
