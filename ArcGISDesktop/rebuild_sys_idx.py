"""
Name: RSysIdx.py
Description: Rebuilds indexes on the states, state_lineages, 
and mv_tables_modified tables in an enterprise geodatabase 
using an existing .sde file.

Author: Esri
"""

# Import system modules
import os

import arcpy

# set workspace
workspace = arcpy.GetParameterAsText(0)

# set the workspace environment
arcpy.env.workspace = workspace

# Execute rebuild indexes
# Note: To use the "SYSTEM" option the workspace user must be an administrator.
arcpy.RebuildIndexes_management(workspace, "SYSTEM", "", "ALL")
print 'Rebuild Complete'