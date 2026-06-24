# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class DisplayOut:
    """Initialize the Display Output.

    :param int width: The logical width of the Display Output. Default is 1280px.
    :param int height: The logical height of the Display Output. Default is 720px.
    :param int refresh_rate: The refresh rate of the Display Output. Default is 60Hz.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from AddOn import DisplayOut
            display = DisplayOut(1280, 720, 60)
    """

    def __new__(
        cls,
        width: int = 1280,
        height: int = 720,
        refresh_rate: int = 60,
    ) -> None:
        return M5.addDisplay(
            None,
            0,
            {
                "unit_poep4_hdmi": {
                    "enabled": True,
                    # see to unit_poep4_hdmi::config_t
                    "width": width,
                    "height": height,
                    "refresh_rate": refresh_rate,
                }
            },
        )
