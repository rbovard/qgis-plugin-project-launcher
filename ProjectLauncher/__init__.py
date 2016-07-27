# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectLauncher
                                 A QGIS plugin
 Project Launcher
                             -------------------
        begin                : 2016-07-27
        copyright            : (C) 2016 by Remi Bovard
        email                : remi.bovard@nyon.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ProjectLauncher class from file ProjectLauncher.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .project_launcher import ProjectLauncher
    return ProjectLauncher(iface)
