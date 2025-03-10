
Display Module
==============

.. include:: ../refs/module.display.ref

Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN GW1NR series FPGA chip to output display signals, and employing the LT8618S chip for signal output conditioning.

Support the following products:

|DisplayModule|

Micropython Example:

    .. literalinclude:: ../../../examples/module/display/cores3_display_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_display_example.m5f2|


class DisplayModule
-------------------

Constructors
------------

.. class:: DisplayModule(port: None, width: int = 1280, height: int = 720, refresh_rate: float = 60.0, output_width: int = 1280, output_height: int = 720, scale_w: int = 1, scale_h: int = 1, pixel_clock = 74250000)

    Initialize the Module Display

    :param tuple port: The port to which the Module Display is connected. port[0]: not used, port[1]: dac pin.
    :param int width: The width of the Module Display.
    :param int height: The height of the Module Display.
    :param int refresh_rate: The refresh rate of the Module Display.
    :param int output_width: The output width of the Module Display.
    :param int output_height: The output height of the Module Display.
    :param int scale_w: The scale width of the Module Display.
    :param int scale_h: The scale height of the Module Display.
    :param int pixel_clock: The pixel clock of the Module Display.

    UIFLOW2:

        |init.png|
