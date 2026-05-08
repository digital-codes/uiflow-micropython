# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan


page0 = None
label_title = None
stackchan = None
tp = None
tp1 = None
last_time = None
tp2 = None
tp3 = None


def setup():
    global page0, label_title, stackchan, tp, tp1, last_time, tp2, tp3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "TP & RGB Strip Example",
        x=13,
        y=10,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    last_time = [0, 0, 0]
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)


def loop():
    global page0, label_title, stackchan, tp, tp1, last_time, tp2, tp3
    M5.update()
    tp = stackchan.get_touch()
    tp1 = tp[0]
    tp2 = tp[1]
    tp3 = tp[2]
    if tp1:
        last_time[0] = time.ticks_ms()
        stackchan.set_rgb_color(0, 0, 0x33CC00)
        stackchan.set_rgb_color(0, 1, 0x33CC00)
        stackchan.set_rgb_color(1, 0, 0x33CC00)
        stackchan.set_rgb_color(1, 1, 0x33CC00)
        Speaker.tone(700, 50)
    else:
        if (time.ticks_diff((time.ticks_ms()), (last_time[0]))) > 300:
            stackchan.set_rgb_color(0, 0, 0x000000)
            stackchan.set_rgb_color(0, 1, 0x000000)
            stackchan.set_rgb_color(1, 0, 0x000000)
            stackchan.set_rgb_color(1, 1, 0x000000)
    if tp2:
        last_time[1] = time.ticks_ms()
        stackchan.set_rgb_color(0, 2, 0x00CCCC)
        stackchan.set_rgb_color(0, 3, 0x00CCCC)
        stackchan.set_rgb_color(1, 2, 0x00CCCC)
        stackchan.set_rgb_color(1, 3, 0x00CCCC)
        Speaker.tone(900, 50)
    else:
        if (time.ticks_diff((time.ticks_ms()), (last_time[1]))) > 300:
            stackchan.set_rgb_color(0, 2, 0x000000)
            stackchan.set_rgb_color(0, 3, 0x000000)
            stackchan.set_rgb_color(1, 2, 0x000000)
            stackchan.set_rgb_color(1, 3, 0x000000)
    if tp3:
        last_time[2] = time.ticks_ms()
        stackchan.set_rgb_color(0, 4, 0x000099)
        stackchan.set_rgb_color(0, 5, 0x000099)
        stackchan.set_rgb_color(1, 4, 0x000099)
        stackchan.set_rgb_color(1, 5, 0x000099)
        Speaker.tone(1100, 50)
    else:
        if (time.ticks_diff((time.ticks_ms()), (last_time[2]))) > 300:
            stackchan.set_rgb_color(0, 4, 0x000000)
            stackchan.set_rgb_color(0, 5, 0x000000)
            stackchan.set_rgb_color(1, 4, 0x000000)
            stackchan.set_rgb_color(1, 5, 0x000000)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
