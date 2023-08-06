#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file provides constants used throughout other modules."""

LOGGING_FILENAME = "./logs/{time}.log"
LOGGING_FORMAT = "{time} {level} {message}"

GRAPH_VISUALISATION_MAP_CONFIG_DEFAULT = {
    "graphml": None,  # input GraphML file
    "o": None,  # output folder for image files
    "o_formats": ("pdf", "svg"),  # output formats that will be created
    "degrees": None,  # output folder where node degree information is saved
    "types": None,  # types of visualization; may be "scatter", "cities", "degrees", and/or "map"
    "shapefile": "../data/shapefiles/DEU_adm1/DEU_adm1.shp",  # input shapefile
    "shapefile_color": "grey",  # shapefile color
    "degree_node_color": "black",  # color of nodes in degree images
    "coordinates": "../data/german_cities.csv",  # CSV file with coordinates information
    "coordinates_sep": ",",  # CSV separator in coordinates input file
    "keys_labels": ("id", "city"),  # ID and label column in coordinates GeoDataFrame
    "crs": "epsg:4326",  # Coordinate Reference System used
    "map_extent": "global",  # may be "global" or a list of 4 values
    "components": True,  # whether all components are used, otherwise only largest
    "all_nodes": True,  # whether also nodes without edges are used
    "graph_corpus": None,  # path to graph corpus, mandatory if all_nodes == True
    "singletons": False,  # if only nodes without edges are used; only used if all_nodes == True
    "name": None,  # identifier for a visualization run that is appended to output images filenames; mandatory
    "figsize": (55, 55),  # size of output figures
    "fontsize": 12,  # font size in figures
    "max_fontsize": 24,
    "edge_width": .25,
    "log": None,  # path to log file
    "log_level_std": "INFO",  # log severity level on standard output
    "log_level_file": "DEBUG",  # log severity level in log file
    "verbose": False,  # if additional information is shown during program execution
    "encoding": "utf-8",  # file encoding used
}
