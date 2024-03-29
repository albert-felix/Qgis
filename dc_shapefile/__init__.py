# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DC_Shapefile
                                 A QGIS plugin
 Creates all DC shapefiles
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-01-17
        copyright            : (C) 2020 by Albert Felix
        email                : albertfelixleo@gmail.com
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
    """Load DC_Shapefile class from file DC_Shapefile.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .DC_Shapefile import DC_Shapefile
    return DC_Shapefile(iface)
