"""
Reconcile and posting versions at 10.0
TODO:WIP
"""

import arcpy, os, sys, string

#Populate parent and child versions in the following manner('Parent':'Child', etc).  DO NOT LIST DEFAULT
vTree = {'SDE.Parent':'SDE.Child','SDE.QA':'SDE.Edit'}

#Reconcile and post child versions with parent
def RecPostNonDefault(workspace,logWorkspace,logName):
    outLog = open(os.path.join(logWorkspace, logName), 'w')
    for key, val in vTree.iteritems():
        arcpy.ReconcileVersion_management(workspace, val, key,"BY_OBJECT", "FAVOR_TARGET_VERSION", "NO_LOCK_AQUIRED", "NO_ABORT", "POST")
        print "Reconciling and posting {0} to {1}".format(val, key)
        outLog.write("Reconciling and posting {0} to {1}".format(val, key))
        outLog.write("\n")
    outLog.close()
    del outLog, key, val

#Reconcile and post with parent          
def RecPostDefault(workspace,logWorkspace,logName2,defaultVersion):
    outLog = open(os.path.join(logWorkspace, logName2), 'w')
    #Reconcile and post parents with DEFAULT
    for key, val in vTree.iteritems():
        arcpy.ReconcileVersion_management(workspace, key, defaultVersion,"BY_OBJECT", "FAVOR_TARGET_VERSION", "NO_LOCK_AQUIRED", "NO_ABORT", "POST")
        print "Reconciling and posting {0} to DEFAULT".format(key)
        outLog.write("Reconciling and posting {0} to DEFAULT".format(key))
        outLog.write("\n")
    outLog.close()
    del outLog, key, val

def DeleteChildVersions(workspace):
    arcpy.ClearWorkspaceCache_management()
    for key, val in vTree.iteritems():
        arcpy.DeleteVersion_management(workspace, val)
        print "Deleted {0}".format(val)
    
        
def DeleteParentVersions(workspace):
    arcpy.ClearWorkspaceCache_management()
    for key, val in vTree.iteritems():
        arcpy.DeleteVersion_management(workspace, key)
        print "Deleted {0}".format(key)
  
#Compress database
def Compress(workspace,logWorkspace,logName3):
    arcpy.ClearWorkspaceCache_management()
    outLog = open(os.path.join(logWorkspace, logName3), 'w')
    arcpy.Compress_management(workspace)
    print ("Compressed database {0}".format(workspace))
    outLog.write("Compressed database {0}".format(workspace))
    outLog.close()

def RecreateVersions(workspace, defaultVersion):
    for key, val in vTree.iteritems():
        arcpy.CreateVersion_management(workspace,defaultVersion, key[4:], "PUBLIC")
        print "Created version {0}".format(key)
        arcpy.CreateVersion_management(workspace, key, val[4:], "PUBLIC")
        print "Created version {0}".format(val)
          
if __name__=="__main__":
    
    workspace = r"Database Connections\MXD2.sde"
    defaultVersion = "sde.DEFAULT"
    logName = "RecPostLog.txt"
    logName2 = "RecPostDefaultLog.txt"
    logName3 = "CompressLog.txt"
    logWorkspace = r"C:\temp"
    RecPostNonDefault(workspace,logWorkspace,logName)
    RecPostDefault(workspace,logWorkspace,logName2,defaultVersion)
    DeleteChildVersions(workspace)
    DeleteParentVersions(workspace)
    Compress(workspace,logWorkspace,logName3)
    RecreateVersions(workspace, defaultVersion)