# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "stackchan/__init__.py",
        "stackchan/app_base.py",
        "stackchan/framework.py",
        "stackchan/apps/__init__.py",
        "stackchan/apps/app_list.py",
        "stackchan/apps/app_run.py",
        "stackchan/apps/dev.py",
        "stackchan/apps/ezdata.py",
        "stackchan/apps/settings.py",
        "stackchan/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)
