# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class RCAModule:
    """! Module RCA is a female jack terminal block for transmitting composite video.

    @en Module RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).
    @cn Module RCA是一个1.3英寸RCA扩展屏单元。采用SH1107驱动，分辨率为128*64，单色显示。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/RCA
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/RCA/img-9420bb3d-22b8-4f80-b7fe-e708088f1e51.webp
    @category module

    @example
                from module import RCAModule
                rca = RCAModule()
                rca.display.fill(0)

    """

    NTSC = 0
    NTSC_J = 1
    PAL = 2
    PAL_M = 3
    PAL_N = 4

    def __new__(
        cls,
        port: int = 26,
        width: int = 216,
        height: int = 144,
        output_width: int = 216,
        output_height: int = 144,
        signal_type: int = NTSC,
        use_psram: int = 0,
        output_level: int = 0,
    ) -> None:
        """! Initialize the Module RCA

        @param port The port to which the Module RCA is connected. port[0]: not used, port[1]: dac pin.
        @param width The width of the RCA display.
        @param height The height of the RCA display.
        @param output_width The width of the output of the RCA display.
        @param output_height The height of the output of the RCA display.
        @param signal_type The signal type of the RCA display. NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4.
        @param use_psram The use of psram of the RCA display.
        @param output_level The output level of the RCA display.

        """
        return M5.addDisplay(
            None,
            0,
            {
                "module_rca": {
                    "enabled": True,
                    # see to M5ModuleRCA::config_t
                    "width": width,
                    "height": height,
                    "output_width": output_width,
                    "output_height": output_height,
                    "signal_type": signal_type,
                    "use_psram": use_psram,
                    "pin_dac": port,
                    "output_level": output_level,
                }
            },
        )
