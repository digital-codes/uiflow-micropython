import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time


page0 = None
label_title = None
label_usb = None
label_bat = None
label_grove = None
label_tip1 = None
label_tip2 = None


grove_en = None
charge_en = None
last_time = None


def btna_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time
    Speaker.tone(1000, 200)
    grove_en = not grove_en
    if grove_en:
        Power.setExtOutput(True)
        label_grove.set_text_color(0xFF0000, 255, 0)
    else:
        Power.setExtOutput(False)
        label_grove.set_text_color(0xFFFFFF, 255, 0)


def btnb_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time
    Speaker.tone(1000, 200)
    charge_en = not charge_en
    if charge_en:
        Power.setBatteryCharge(True)
    else:
        Power.setBatteryCharge(False)


def setup():
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Power test",
        x=123,
        y=40,
        text_c=0x10AACD,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_usb = m5ui.M5Label(
        "USB: --mV",
        x=170,
        y=135,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_bat = m5ui.M5Label(
        "Battery: --mV",
        x=151,
        y=170,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_grove = m5ui.M5Label(
        "Grove: --mV",
        x=160,
        y=205,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tip1 = m5ui.M5Label(
        "Botton A Control Grove",
        x=94,
        y=330,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tip2 = m5ui.M5Label(
        "Botton B Control Charge",
        x=82,
        y=366,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_click_event)

    page0.screen_load()
    Power.setBatteryCharge(True)
    Power.setExtOutput(False)
    grove_en = False
    charge_en = False
    Speaker.begin()
    Speaker.setVolumePercentage(0.8)


def loop():
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        label_usb.set_text(str((str("USB: ") + str((str((Power.getVBUSVoltage())) + str("mV"))))))
        label_usb.align_to(page0, lv.ALIGN.TOP_MID, 0, 135)
        label_bat.set_text(
            str((str("Battery: ") + str((str((Power.getBatteryVoltage())) + str("mV")))))
        )
        label_bat.align_to(page0, lv.ALIGN.TOP_MID, 0, 170)
        label_grove.set_text(
            str((str("Grove: ") + str((str((Power.getExtVoltage(M5.Power.PORT.A))) + str("mV")))))
        )
        label_grove.align_to(page0, lv.ALIGN.TOP_MID, 0, 205)
        if Power.isCharging():
            label_bat.set_text_color(0x33FF33, 255, 0)
        else:
            label_bat.set_text_color(0xFFFFFF, 255, 0)


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
