Joystick Hat
============

.. include:: ../refs/hat.joystick.ref

The following products are supported:

    |JoystickHat|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/joystick/stickc_plus2_joystick_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_joystick_example.m5f2|


class JoystickHat
-----------------

Constructors
------------

.. class:: JoystickHat(i2c, address: int | list | tuple = 0x38)

    Create a new instance of the JoystickHat class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: JoystickHat.get_x_raw() -> int

    Get the raw x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x_raw.png|


.. method:: JoystickHat.get_y_raw() -> int

    Get the raw y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y_raw.png|


.. method:: JoystickHat.get_x() -> int

    Get the x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x.png|


.. method:: JoystickHat.get_y() -> int

    Get the y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y.png|


.. method:: JoystickHat.swap_x(swap: bool = True) -> None

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_x.png|


.. method:: JoystickHat.swap_y(swap: bool = True) -> None

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_y.png|

.. method:: JoystickHat.get_button_status() -> bool

    Get the button status.

    :return: True or False

    UIFLOW2:

        |get_button_status.png|
