StamPLC IO
==========

.. include:: ../refs/stamplc.io.ref

``IOStamPLC`` controls the StamPLC IO extension board over I2C.

UiFlow2 Example
---------------

Voltage and current monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |stamplc_io_example.m5f2| project in UiFlow2.

This example sets the two output channels to PWM mode, then displays the voltage and current of channel 0 and channel 1.

UiFlow2 Code Block:

    |stamplc_io_example.png|

Example output:

    None

MicroPython Example
-------------------

Voltage and current monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example sets the two output channels to PWM mode, then displays the voltage and current of channel 0 and channel 1.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamplc/io/stamplc_io_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

IOStamPLC
^^^^^^^^^

.. class:: IOStamPLC(i2c=None, address=0x20)

    Create a StamPLC IO extension object.

    :param i2c: I2C interface. If omitted, the shared StamPLC I2C bus is used.
    :param int address: I2C address of the StamPLC IO extension.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from stamplc import IOStamPLC

            io = IOStamPLC(address=0x20)

    .. method:: get_voltage(channel)

        Get the voltage of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :returns: Voltage in mV.
        :rtype: int

        UiFlow2 Code Block:

            |get_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = io.get_voltage(0)

    .. method:: get_current(channel)

        Get the current of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :returns: Current in uA.
        :rtype: int

        UiFlow2 Code Block:

            |get_current.png|

        MicroPython Code Block:

            .. code-block:: python

                current = io.get_current(0)

    .. method:: get_io_control()

        Get the IO control register value.

        :returns: IO control register value.
        :rtype: int

    .. method:: set_io_control(value)

        Set the IO control register value.

        :param int value: IO control register value.

    .. method:: set_solid_relay(channel, state)

        Set the solid-state relay output of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :param bool state: ``True`` turns the output on, ``False`` turns it off.

        UiFlow2 Code Block:

            |set_solid_relay.png|

        MicroPython Code Block:

            .. code-block:: python

                io.set_solid_relay(0, True)

    .. method:: get_solid_relay(channel)

        Get the solid-state relay output state of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :returns: Output state.
        :rtype: bool

        UiFlow2 Code Block:

            |get_solid_relay.png|

    .. method:: set_ina226_pullup(channel, enable)

        Enable or disable the INA226 pull-up of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :param bool enable: ``True`` enables the pull-up, ``False`` disables it.

        UiFlow2 Code Block:

            |set_ina226_pullup.png|

    .. method:: get_ina226_pullup(channel)

        Get the INA226 pull-up state of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :returns: Pull-up state.
        :rtype: bool

        UiFlow2 Code Block:

            |get_ina226_pullup.png|

    .. method:: set_relay(state)

        Set the onboard relay output.

        :param bool state: ``True`` turns the relay on, ``False`` turns it off.

        UiFlow2 Code Block:

            |set_relay.png|

    .. method:: get_relay()

        Get the onboard relay output state.

        :returns: Relay state.
        :rtype: bool

        UiFlow2 Code Block:

            |get_relay.png|

    .. method:: set_output_mode(mode)

        Set the output mode.

        :param int mode: ``IOStamPLC.OUTPUT_IO_MODE`` or ``IOStamPLC.PWM_MODE``.

        UiFlow2 Code Block:

            |set_output_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                io.set_output_mode(IOStamPLC.PWM_MODE)

    .. method:: get_output_mode()

        Get the output mode.

        :returns: ``IOStamPLC.OUTPUT_IO_MODE`` or ``IOStamPLC.PWM_MODE``.
        :rtype: int

        UiFlow2 Code Block:

            |get_output_mode.png|

    .. method:: set_ina226_config(channel, value)

        Set the INA226 configuration register of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :param int value: Register value.

    .. method:: get_ina226_config(channel)

        Get the INA226 configuration register of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :returns: Register value.
        :rtype: int

    .. method:: set_pwm_config(channel, freq, duty)

        Set the PWM frequency and duty of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :param int freq: PWM frequency, ``1`` to ``100``.
        :param int duty: PWM duty, ``0`` to ``1000``.

        UiFlow2 Code Block:

            |set_pwm_config.png|

        MicroPython Code Block:

            .. code-block:: python

                io.set_pwm_config(0, 1, 100)

    .. method:: get_pwm_config(channel)

        Get the PWM frequency and duty of one channel.

        :param int channel: Channel index, ``0`` or ``1``.
        :returns: ``(freq, duty)``.
        :rtype: tuple

    .. method:: get_firmware_version()

        Get the firmware version.

        :returns: Firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                version = io.get_firmware_version()

    .. method:: get_i2c_address()

        Get the configured I2C address.

        :returns: I2C address.
        :rtype: int

        UiFlow2 Code Block:

            |get_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                address = io.get_i2c_address()

    .. method:: refresh_i2c_address()

        Refresh the active I2C address from the device.
