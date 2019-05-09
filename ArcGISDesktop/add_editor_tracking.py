"""Enable editor tracking on gdb objects.

This script enables editor tracking on feature classes, tables, and Rasters.
Feature classes within feature datasets will also be parsed and editor
tracking enabled.

Scripts prompts for sde connection file located in the default 
'Database Connections/' location which is in %appData%\Esri\Desktop10.6\ArcCatalog.
Enter as <file>.sde

TODO: Accept connection file as command line argument

"""

import os

import arcpy

# Set variables
connection_file = raw_input('Enter SDE connection filename: ')

# Set the workspace
arcpy.env.workspace = 'Database Connections/' + connection_file

# Set a variable for the workspace
workspace = arcpy.env.workspace

# Enumerate Database elements
datasets = arcpy.ListDatasets(wild_card=None,
                              feature_type=None)

edit_items = arcpy.ListFeatureClasses() \
             + arcpy.ListTables() \
             + arcpy.ListRasters()

# Add features from inside datasets to edit_items list
for dataset in datasets:
    edit_items += arcpy.ListFeatureClasses(wild_card=None,
                                           feature_type=None,
                                           feature_dataset=dataset)

for item in edit_items:
    arcpy.EnableEditorTracking_management(in_dataset=item,
                                          creator_field="created_user",
                                          creation_date_field="created_date",
                                          last_editor_field="last_edited_user",
                                          last_edit_date_field="last_edited_date",
                                          add_fields="ADD_FIELDS",
                                          record_dates_in="UTC")
