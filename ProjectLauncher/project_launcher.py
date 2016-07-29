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
import ConfigParser
from qgis.core import QgsProject
from qgis.gui import QgsMessageBar
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtCore import QFileInfo
from PyQt4.QtGui import QAction, QIcon, QMenu

# Initialize Qt resources from file resources.py
import resources

class ProjectLauncher:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            "i18n",
            "ProjectLauncher_{}.qm".format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u"&Project Launcher")

        self.menu_action = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        return QCoreApplication.translate("ProjectLauncher", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag = True,
        add_to_menu = True,
        add_to_toolbar = True,
        status_tip = None,
        whats_this = None,
        parent = None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ":/plugins/foo/bar.png") or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/ProjectLauncher/icon.png"
        self.add_action(
            icon_path,
            text = self.tr(u"Project Launcher"),
            callback = self.run,
            add_to_menu = False,
            add_to_toolbar = False,
            parent = self.iface.mainWindow())

        self.init_menu()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u"&Project Launcher"),
                action)
            self.iface.removeToolBarIcon(action)

        self.remove_menu()

    def run(self):
        """Run method that performs all the real work"""
        # Do something useful here - delete the line containing pass and
        # substitute with your code.
        self.open_project()

    def init_menu(self):

        config = ConfigParser.ConfigParser()
        config.read(os.path.join(self.plugin_dir, "projects.ini"))

        menu_name = config.get("General", "name").decode("utf-8")
        menu = self.add_menu(menu_name)

        for section in config.sections():
            if section != "General":
                submenu = self.add_submenu(section.decode("utf-8"), menu)

                for name, value in config.items(section):
                    self.add_menu_item(
                        name.decode("utf-8").capitalize(), value,
                        submenu
                    )

    def add_menu(self, menu):

        iface = self.iface

        menu_bar = iface.editMenu().parentWidget()
        menu = QMenu(menu, menu_bar)
        self.menu_action = menu_bar.addMenu(menu)

        return menu

    def remove_menu(self):

        iface = self.iface

        menu_bar = iface.editMenu().parentWidget()
        menu_bar.removeAction(self.menu_action)

    def add_submenu(self, submenu, menu):

        submenu = QMenu(submenu, menu)
        submenu.setIcon(QIcon(":/plugins/ProjectLauncher/icon_folder.png"))
        menu.addMenu(submenu)

        return submenu

    def add_menu_item(self, item, project, submenu):

        iface = self.iface

        action = QAction(item, iface.mainWindow())
        action.setIcon(QIcon(":/plugins/ProjectLauncher/icon_project.png"))
        submenu.addAction(action)

        helper = lambda _project: (lambda: self.open_project(_project))
        action.triggered.connect(helper(project))

    def open_project(self, project_path):

        iface = self.iface
        project = QgsProject.instance()

        # TODO: Need to handle this in a proper way
        if project.fileName() and project.isDirty():
            iface.messageBar().pushMessage(
                u"Projet modifié",
                u"Enregistrer ou fermer le projet courant.",
                QgsMessageBar.WARNING, 3
            )

        else:
            iface.addProject(project_path)
            project.setDirty(False)
