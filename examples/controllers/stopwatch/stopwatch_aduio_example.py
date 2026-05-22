import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from audio import Recorder
import time
from audio import Player


page0 = None
label_title = None
label_count = None
label_state = None
label_tip1 = None
label_tip2 = None
recorder = None
player = None


flag_record = None
flag_play = None
record_start_time = None
remaining = None
RECORD_TIME = None
record_file_path = None


def btna_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path
    flag_record = True


def btnb_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path
    if not (recorder.is_recording()):
        flag_play = True


def setup():
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Audio Test",
        x=128,
        y=40,
        text_c=0x10AACD,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_count = m5ui.M5Label(
        "5",
        x=218,
        y=205,
        text_c=0x10AACD,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_state = m5ui.M5Label(
        "Idle",
        x=194,
        y=116,
        text_c=0x10CD53,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_tip1 = m5ui.M5Label(
        "Button B Play",
        x=148,
        y=366,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tip2 = m5ui.M5Label(
        "Button A Record",
        x=131,
        y=330,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_click_event)

    page0.screen_load()
    Mic.end()
    Speaker.end()
    recorder = Recorder(8000, 16, True)
    player = Player(None)
    player.set_vol(80)
    RECORD_TIME = 5
    record_file_path = "rec1.amr"
    flag_record = False
    flag_play = False


def loop():
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path
    M5.update()
    if flag_record:
        if not (recorder.is_recording()):
            record_start_time = time.ticks_ms()
            label_state.set_text(str("Recording..."))
            label_state.set_text_color(0xFF0000, 255, 0)
            label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
            Speaker.setPA(False)
            recorder.record("file://flash/res/audio/" + str(record_file_path), RECORD_TIME, False)
        else:
            remaining = (
                RECORD_TIME - (time.ticks_diff((time.ticks_ms()), record_start_time)) / 1000
            )
            if remaining > 0:
                label_count.set_text(str(int(remaining)))
            else:
                label_count.set_text(str("0"))
                flag_record = False
                label_state.set_text(str("Idle"))
                label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
                label_state.set_text_color(0x33CC00, 255, 0)
    if not (recorder.is_recording()):
        if flag_play:
            flag_play = False
            label_count.set_text(str(""))
            label_state.set_text(str("Playing..."))
            label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
            label_state.set_text_color(0xFF0000, 255, 0)
            Speaker.setPA(True)
            player.play(
                "file://flash/res/audio/" + str(record_file_path), pos=0, volume=-1, sync=False
            )
        else:
            if not (player.pos()):
                label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
                label_count.set_text(str(RECORD_TIME))
                label_state.set_text(str("Idle"))
                label_state.set_text_color(0x33CC00, 255, 0)


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
