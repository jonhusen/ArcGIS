"""
Name: UStatsSysTbls.py
Description: Updates statistics on enterprise geodatabase  
system tables using an existing .sde file.

Author: Esri
"""

# Import system modules
import arcpy, os

# set workspace
workspace = arcpy.GetParameterAsText(0)

# set the workspace environment
arcpy.env.workspace = workspace

# Execute analyze datasets for system tables
arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", "", "","","")
print "Analyze Complete"
