# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "stopwatch/__init__.py",
        "stopwatch/app_base.py",
        "stopwatch/framework.py",
        "stopwatch/layout.py",
        "stopwatch/res.py",
        "stopwatch/apps/__init__.py",
        "stopwatch/apps/dev.py",
        "stopwatch/apps/settings.py",
        "stopwatch/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)
