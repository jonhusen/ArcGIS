"""
Name: NightlyGDBMaintenance.py
Description: Reconciles and posts all versions owned by SDE with SDE.Default
Compresses, rebuilds indexes, and analyzes system tables
Recreates child versions
TODO:WIP
"""

# Import system modules
import arcpy, os

# Set workspace
workspace = r'c:\Temp\test_editpermissions_sa.sde'

# Set the workspace environment
arcpy.env.workspace = workspace

# Block new connections to the database.
arcpy.AcceptConnections(workspace, False)

# Wait 15 minutes
# time.sleep(900)

# Disconnect all users from the database.
arcpy.DisconnectUser(workspace, "ALL")

# Use a list comprehension to get a list of version names where the owner
# is the current user and make sure sde.default is not selected.
verList = [ver.name for ver in arcpy.da.ListVersions() if ver.isOwner == True and ver.name.lower() != 'sde.default']

# Reconcile and Post versions to sde.DEFAULT
arcpy.ReconcileVersions_management(workspace,
                                   "ALL_VERSIONS",
                                   "SDE.Default",
                                   verList,
                                   "LOCK_ACQUIRED",
                                   "NO_ABORT",
                                   "BY_OBJECT",
                                   "FAVOR_TARGET_VERSION",
                                   "POST",
                                   "DELETE_VERSION",
                                   "c:\Temp\RecLog.txt")
print 'Reconciling Complete'

# Compress database
arcpy.Compress_management(workspace)

print 'Database Compression Complete'

# Rebuild indexes
arcpy.RebuildIndexes_management(workspace,
                                "SYSTEM",
                                "ALL")
print 'Rebuild Indexes complete'

# Analyze the states and states_lineages system tables
arcpy.AnalyzeDatasets_management(workspace,
                                 "SYSTEM",
                                 "ANALYZE_BASE",
                                 "ANALYZE_DELTA",
                                 "ANALYZE_ARCHIVE")

print 'Analyze Datasets Complete'
# Recreate Child versions
# Set variables
parentVersion = "sde.DEFAULT"

# Execute create Child Versions
def CreateChildVersions(workspace, verList):
    parentVersion = "sde.DEFAULT"
    for version in verList:
        arcpy.createVersion_management(workspace,
                                       parentVersion,
                                       version,
                                       "Public")

print 'Child Versions Recreated'

# Allow the database to begin accepting connections again
arcpy.AcceptConnections(workspace, True)

print 'Database ready for editing.'