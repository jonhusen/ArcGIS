import os

import arcpy

# Set variables
connection_file = raw_input('Enter SDE connection filename: ')
user = raw_input('Enter username or group [SPECTRUM\GIS_Admin]: ') \
       or 'SPECTRUM\GIS_Admin'
view_rights = 'GRANT'
edit_rights = 'GRANT'

# Set workspace
arcpy.env.workspace = "Database Connections/" + connection_file

# Enumerate Database elements
db_items = arcpy.ListDatasets() \
           + arcpy.ListFeatureClasses() \
           + arcpy.ListTables()

arcpy.ChangePrivileges_management(in_dataset=db_items, 
                                  user=user, 
                                  View=view_rights, 
                                  Edit=edit_rights)
