/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#define MICROPY_HW_BOARD_NAME "M5STACK AtomS3R-CAM"
#define MICROPY_HW_MCU_NAME   "ESP32-S3-PICO-1"

#define MICROPY_PY_MACHINE_DAC (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
#define MICROPY_HW_ENABLE_UART_REPL (1)

#define MICROPY_HW_I2C0_SCL (0)
#define MICROPY_HW_I2C0_SDA (45)

#define MICROPY_HW_USB_CDC_INTERFACE_STRING "M5Stack AtomS3R-CAM(UiFlow2)"

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
