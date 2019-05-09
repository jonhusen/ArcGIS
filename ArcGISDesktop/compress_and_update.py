"""
Copied from ESRI documentation
"""

import arcpy, time, smtplib

# Set the workspace 
arcpy.env.workspace = 'Database Connections/admin.sde'

# Set a variable for the workspace
workspace = arcpy.env.workspace

# Get a list of connected users.
userList = arcpy.ListUsers("Database Connections/admin.sde")

# Get a list of user names of users currently connected and make email addresses
emailList = [u.Name + "@yourcompany.com" for user in arcpy.ListUsers("Database Connections/admin.sde")]

# Take the email list and use it to send an email to connected users.
SERVER = "mailserver.yourcompany.com"
FROM = "SDE Admin <python@yourcompany.com>"
TO = emailList
SUBJECT = "Maintenance is about to be performed"
MSG = "Auto generated Message.\n\rServer maintenance will be performed in 15 minutes. Please log off."

# Prepare actual message
MESSAGE = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MSG)

# Send the mail
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, MESSAGE)
server.quit()

# Block new connections to the database.
arcpy.AcceptConnections('Database Connections/admin.sde', False)

# Wait 15 minutes
time.sleep(900)

# Disconnect all users from the database.
arcpy.DisconnectUser('Database Connections/admin.sde', "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions('Database Connections/admin.sde')

# Execute the ReconcileVersions tool.
arcpy.ReconcileVersions_management('Database Connections/admin.sde', "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", "c:/temp/reconcilelog.txt")

# Run the compress tool. 
arcpy.Compress_management('Database Connections/admin.sde')

# Allow the database to begin accepting connections again
arcpy.AcceptConnections('Database Connections/admin.sde', True)

# Get a list of datasets owned by the admin user

# Rebuild indexes and analyze the states and states_lineages system tables
arcpy.RebuildIndexes_management(workspace, "SYSTEM", "ALL")

arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")