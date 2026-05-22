# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import app_base
import asyncio
import M5
import time


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = app_base.AppSelector(self._apps)
        self._launcher = None

    def install_launcher(self, launcher: app_base.AppBase):
        self._launcher = launcher

    def install(self, app: app_base.AppBase):
        app.install()
        self._apps.append(app)

    def start(self):
        asyncio.run(self.run())

    async def run(self):
        if self._launcher:
            self._app_selector.select(self._launcher)
            self._launcher.start()

        last_touch_time = time.ticks_ms()
        while True:
            M5.update()
            if M5.BtnA.wasSingleClicked():
                M5.Speaker.tone(6000, 20)
                app = self._app_selector.current()
                app.stop()
                app = self._app_selector.prev()
                app.start()
            if M5.BtnB.wasSingleClicked():
                M5.Speaker.tone(7000, 20)
                app = self._app_selector.current()
                app.stop()
                app = self._app_selector.next()
                app.start()

            if M5.Touch.getCount() > 0:
                detail = M5.Touch.getDetail(0)
                cur_time = time.ticks_ms()
                if cur_time - last_touch_time > 150:
                    if not detail[9]:
                        M5.Speaker.tone(3500, 50)
                        x = M5.Touch.getX()
                        y = M5.Touch.getY()
                        app = self._app_selector.current()
                        if hasattr(app, "_click_event_handler"):
                            await app._click_event_handler(x, y, self)
                    last_touch_time = cur_time

            await asyncio.sleep_ms(10)
