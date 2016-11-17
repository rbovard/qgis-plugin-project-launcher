# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectLauncher
                                 A QGIS plugin
 Project Launcher
                              -------------------
        begin                : 2016-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Remi Bovard
        email                : remi.bovard@nyon.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
from qgissettingmanager import *

class MySettings(SettingManager):

    def __init__(self):

        SettingManager.__init__(self, u"ProjectLauncher")

        self.add_setting(String(
            "projects_list",
            Scope.Global,
            os.path.join(os.path.dirname(__file__), "projects.ini")
        ))
