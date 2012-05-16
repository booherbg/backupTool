'''
Backup Tool (c) 2012 Clifton Labs, Inc.
Blaine Booher

A tool for managing rolling backup systems.

Saves N latest files, deletes the rest.

usage:
python backupTool.py <options> <directory>

options:
    -X  by default, this script does a dry-run. -X makes it real.
    -n NUM_FILES    how many files to keep? Default 4.
    
examples:

Run a dry-run on c:\backup with defaults:
python c:\backup\

Actually do it, save newest 10 files
python -X -n 10 c:\backup
'''

import os
from glob import glob
from sys import stderr, exit, argv
from datetime import datetime

N = 4
FileFilter = ("*.bak", "*.trn")
DryRun = True
directory = None
useModified = True
interactive = True

if __name__ == '__main__':
    if len(argv) == 1 or ("--help" in argv) or ("-h" in argv):
        print "backup tool (c) Clifton Labs 2012; Blaine Booher"
        print "usage: %s [options] /path/to/directory" % argv[0]
        print "--help shows this message"
        print ""
        print "by default, this tool does a dry-run (no deletions)"
        print "options: "
        print "  -X       no dry-run (actually delete old files)"
        print "  -y       disable interactive mode (use for scripting only)"
        print "  -n NUM   keep NUM most recent files, delete the rest (default=4)"
        exit(2)
        
    for i in xrange(len(argv)):
        if argv[i] == "-n":
            N = int(argv[i+1])
            if N < 0:
                stderr.write("Please choose n >= 0\n")
                exit(3)
            i = i + 1
            continue
        if argv[i] == "-X":
            DryRun = False
            continue
            
        if argv[i] == "-y":
            interactive = False
            continue
            
    # directory is the last argument
    directory = argv[-1]
    
    if (not os.path.exists(directory)) or (os.path.isdir(directory) == False):
        stderr.write("%s not valid directory\n" % directory)
        exit(1)
        
    # Get all files in filter list (supports multiple file types)
    files = []
    for f in FileFilter:
        files.extend(glob(os.path.join(directory, f)))
        
    # Grab a list of files in the directory
    #files = glob(os.path.join(directory, FileFilter))
    
    stderr.write("Keeping only %d newly modified files from %s\n" % (N, directory))
    if DryRun:
        stderr.write("Mode: Dry-Run (no deletions)\n")
    else:
        stderr.write("Mode: Delete Old Files\n")
    
    # Get the date of the file
    pending = []
    for f in files:
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f)
        timestamp = datetime.fromtimestamp(mtime)
#        print "%s modified " % f,
#        print timestamp
        pending.append((timestamp, f))
        
    # Sort from oldest to newest
    pending.sort()
    deleteList = pending[0:-N]
    keepList = pending[-N:]
    for t,f in deleteList:
        stderr.write("%s %s <-- Delete\n" % (f,repr(t.strftime("%A, %d. %B %Y %I:%M:%S%p"))))
    for t,f in keepList:
        stderr.write("%s %s <-- Keep\n" % (f,repr(t.strftime("%A, %d. %B %Y %I:%M:%S%p"))))
    
    # Remind of what mode it is
    if DryRun:
        stderr.write("Heads Up: You're in DRY-RUN mode. No files will be modified\n")
    else:
        stderr.write("Heads Up: You're in DELETION mode. Files marked for deletion will be toast\n")
    
    # Double Check
    if interactive:
        answer = raw_input("Would you like to continue? (y/n) ")
        if answer != "y":
            stderr.write("Aborted; no files affected\n")
            
    # Here we go...
    if DryRun:
        stderr.write("\nDry-Run Enabled. To ACTUALLY DELETE these files, use the -X argument.\n")
    else:
        stderr.write("\nDeletion Mode Enabled. Actually deleting the following files...\n")
        
    for t,f in deleteList:
        stderr.write("DELETE %s..." % (f))
        if DryRun:
            stderr.write("Dry-Run\n")
        else:
            os.unlink(f)
            stderr.write("SUCCESSFUL\n")
        
    stderr.write("finished successfully\n")
    stderr.flush()
    
