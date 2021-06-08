# Backup
Python Backup script

Can only backup files from a single source folder to a single destination folder.

Script does the following:
+ Check if Source and Destination folders are set
    - If they are not set, it lets you set the folder paths
    - If the folder paths are set, it will ask if you want to change them
+ Checks if the destination folder is empty
    - If the folder is empty, it will start a full backup
+ Checks what day of the week it is
    - If it is a Sunday, it will start a full backup
    - If it is not a Sunday, it will start an "Incremental Backup"
+ "Incremental" Backup" will check if any file names or file sizes have changed
    - If any files have changed it will start an "Incremental Backup"

When a full or incremental backup is run, the script will write to a log file.
It only writes the following:
[Type of backup] + [Date] + [Time]

Note: Incremental backup copies all files in the source folder when changes are made, it does not only copy the files that have changed
