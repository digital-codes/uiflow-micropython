
CO2L Unit
=========
.. sku:U104
.. include:: ../refs/unit.co2l.ref

UNIT CO2L is a digital air CO2 concentration detection unit with a single-measurement low-power mode, built-in Sensirion's SCD41 sensor and power buck circuitry, and I2C communication. The unit is suitable for the measurement of air ambient conditions with a typical accuracy of ± (40 ppm + 5 % reading) for CO2 measurements over a measuring range of 400 ppm – 5000 ppm while measuring ambient temperature and humidity.

Support the following products:

|CO2LUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/co2l/co2l_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |co2l_cores3_example.m5f2|


class CO2LUnit
--------------

Constructors
------------

.. class:: CO2LUnit(i2c, address)

    Initialize the CO2LUnit with the I2C interface and address.

    :param  i2c: I2C interface or PAHUBUnit instance for communication.
    :param int address: I2C address of the CO2 sensor, default is 0x62.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: CO2LUnit.available()

    Check if the CO2 unit is available on the I2C bus.


.. method:: CO2LUnit.set_start_periodic_measurement()

    Set the sensor into working mode, which takes about 5 seconds per measurement.


    UIFLOW2:

        |set_start_periodic_measurement.png|

.. method:: CO2LUnit.set_stop_periodic_measurement()

    Stop the measurement mode for the sensor.


    UIFLOW2:

        |set_stop_periodic_measurement.png|

.. method:: CO2LUnit.get_sensor_measurement()

    Get temperature, humidity, and CO2 concentration from the sensor.


.. method:: CO2LUnit.is_data_ready()

    Check if the data (temperature, humidity, CO2) is ready from the sensor.


    UIFLOW2:

        |is_data_ready.png|

.. method:: CO2LUnit.get_temperature_offset()

    Get the temperature offset to be added to the reported measurements.


    UIFLOW2:

        |get_temperature_offset.png|

.. method:: CO2LUnit.set_temperature_offset(offset)

    Set the maximum value of 374°C temperature offset.

    :param int offset: The temperature offset to set, default is 0.

    UIFLOW2:

        |set_temperature_offset.png|

.. method:: CO2LUnit.get_sensor_altitude()

    Get the altitude value of the measurement location in meters above sea level.


    UIFLOW2:

        |get_sensor_altitude.png|

.. method:: CO2LUnit.set_sensor_altitude(height)

    Set the altitude value of the measurement location in meters above sea level.

    :param int height: The altitude in meters to set. Must be between 0 and 65535 meters.

    UIFLOW2:

        |set_sensor_altitude.png|

.. method:: CO2LUnit.set_ambient_pressure(ambient_pressure)

    Set the ambient pressure in hPa at any time to adjust CO2 calculations.

    :param int ambient_pressure: The ambient pressure in hPa, constrained to the range [0, 65535].

    UIFLOW2:

        |set_ambient_pressure.png|

.. method:: CO2LUnit.set_force_calibration(target_co2)

    Force the sensor to recalibrate with a given current CO2 level.

    :param int target_co2: The current CO2 concentration to be used for recalibration.

    UIFLOW2:

        |set_force_calibration.png|

.. method:: CO2LUnit.get_calibration_enabled()

    Get whether automatic self-calibration (ASC) is enabled or disabled.


    UIFLOW2:

        |get_calibration_enabled.png|

.. method:: CO2LUnit.set_calibration_enabled(enabled)

    Enable or disable automatic self-calibration (ASC).

    :param bool enabled: Set to True to enable ASC, or False to disable it.

    UIFLOW2:

        |set_calibration_enabled.png|

.. method:: CO2LUnit.set_start_low_periodic_measurement()

    Set the sensor into low power working mode, with about 30 seconds per measurement.


    UIFLOW2:

        |set_start_low_periodic_measurement.png|

.. method:: CO2LUnit.data_isready()

    Check if new data is available from the sensor.

.. method:: CO2LUnit.save_to_eeprom()

    Save temperature offset, altitude offset, and self-calibration enable settings to EEPROM.


    UIFLOW2:

        |save_to_eeprom.png|

.. method:: CO2LUnit.get_serial_number()

    Get a unique serial number for this sensor.


    UIFLOW2:

        |get_serial_number.png|

.. method:: CO2LUnit.set_self_test()

    Perform a self-test, which can take up to 10 seconds.


    UIFLOW2:

        |set_self_test.png|

.. method:: CO2LUnit.set_factory_reset()

    Reset all configuration settings stored in the EEPROM and erase the FRC and ASC algorithm history.


    UIFLOW2:

        |set_factory_reset.png|

.. method:: CO2LUnit.reinit()

    Reinitialize the sensor by reloading user settings from EEPROM.


    UIFLOW2:

        |reinit.png|

.. method:: CO2LUnit.set_single_shot_measurement_all()

    Set the sensor to perform a single-shot measurement for CO2, humidity, and temperature.

.. method:: CO2LUnit.set_single_shot_measurement_ht()

    Set the sensor to perform a single-shot measurement for humidity and temperature.

.. method:: CO2LUnit.set_sleep_mode()

    Put the sensor into sleep mode to reduce current consumption.

.. method:: CO2LUnit.set_wake_up()

    Wake up the sensor from sleep mode into idle mode.

.. method:: CO2LUnit.write_cmd(cmd_wr, value)

    Write a command to the sensor.

    :param int cmd_wr: The command to write to the sensor.
    :param int value: The value to send with the command, if any.

.. method:: CO2LUnit.read_response(num)

    Read the sensor's response.

    :param int num: The number of bytes to read from the sensor.

.. method:: CO2LUnit.check_crc(buf)

    Check the CRC of the received data to ensure it is correct.

    :param bytearray buf: The buffer of bytes to check the CRC.

.. method:: CO2LUnit.crc8(buffer)

    Calculate the CRC-8 checksum for a given buffer.

    :param bytearray buffer: The buffer of bytes to calculate the CRC for.



