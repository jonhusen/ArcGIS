"""
Name: UStatsSysSqlServer.py
Description: Updates statistics on system tables in an enterprise geodatabase in SQL Server.

Author: Esri
"""

# Import system modules
import sys
import arcpy
import os

# Provide connection information
server = srvr-sql-esri10
service = "5151 | sde:srvr-sql-esri:sqlserver_instance"
database = database_name
account_authentication = OPERATING_SYSTEM_AUTH | DATABASE_AUTH
#Leave username and password blank if using OPERATING_SYSTEM_AUTH
username = gdb_admin_user_name
password = gdb_admin_password
version = sde.DEFAULT


# Set local variables
if os.name.lower() == "nt":
   slashsyntax = "\\"
   if os.environ.get("TEMP") == None:
      temp = "c:\\temp"
   else:
      temp = os.environ.get("TEMP")
else:
   slashsyntax = "/"
   if os.environ.get("TMP") == None:
      temp = "/usr/tmp"
   else:
      temp = os.environ.get("TMP")

Connection_File_Name = temp + slashsyntax + "connection.sde"

# Check for the .sde file and delete it if present
if os.path.exists(Connection_File_Name):
   os.remove(Connection_File_Name)

#Variable defined within the script; other variable options commented out at the end of the line
saveUserInfo = "SAVE_USERNAME" #DO_NOT_SAVE_USERNAME
saveVersionInfo = "SAVE_VERSION" #DO_NOT_SAVE_VERSION

print "Creating ArcSDE Connection File..."
# Create ArcSDE Connection File
# Usage: out_folder_path, out_name, server, service, database, account_authentication, username, password, save_username_password
arcpy.CreateArcSDEConnectionFile_management(temp, "connection.sde", server, service, database, account_authentication, username, password, saveUserInfo, version, saveVersionInfo)

# Update statistics on system tables
arcpy.AnalyzeDatasets_management(Connection_File_Name, "SYSTEM","","","","")
print "Analyze Complete"
