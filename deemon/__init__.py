#!/usr/bin/env python3

__title__ = 'Deemon Redux'
__pypi_name__ = 'deemon-redux'
__appdata_name__ = 'deemon-redux'
__version__ = '2.25'
__dbversion__ = '3.7'

from deemon.utils import startup

from deemon.core.common import map_track as new_map_track

import deezer.utils
deezer.utils.map_track = new_map_track

appdata = startup.get_appdata_dir()
startup.init_appdata_dir(appdata)
