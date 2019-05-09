"""
Registers datasets, feature classes, and tables as versioned

Input: sde connection file as string
returns: no output

todo: error handling around already versioned objects
    output for success/failure
"""

import os

import arcpy

# Set variables
connection_file = raw_input('Enter SDE connection filename: ')

# Set the workspace
arcpy.env.workspace = 'Database Connections/' + connection_file

# Enumerate Database elements
version_items = arcpy.ListDatasets() + arcpy.ListFeatureClasses() + arcpy.ListTables()

for item in version_items:
    arcpy.RegisterAsVersioned_management(in_dataset=item,
                                         edit_to_base="NO_EDITS_TO_BASE")
