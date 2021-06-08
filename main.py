# Simple Backup script
# Creates Backups of files in defined source directory when run
# Backups are saved to defined destination directory

# Imports
import csv
import shutil
import os
import time

# Time data used
timestr_date = time.strftime("%Y%m%d")
timestr_onlytime = time.strftime("%H%M%S")
timestr_weekday = time.strftime("%A")

# Source and Destination files containing the source and destination folder paths
with open('/Users/nle/Desktop/Backup Python/srcfile', 'r') as srcfile:
    source = ''.join(srcfile.readlines())
with open('/Users/nle/Desktop/Backup Python/destfile', 'r') as destfile:
    destination = ''.join(destfile.readlines())


# Checks if source and destination are empty
# If there is no string in source or destination, the script will ask for user input
# If there is a string in source or destination, the script will ask if the user wants to change the source/destination
def check_srcdest():
    global source
    global destination
    if not source:
        change_src()
    if not destination:
        change_dest()
    else:
        print("Source: " + source)
        print("Destination: " + destination)
        change = input("Do you want to change source or destination? y/n\n")
        if change == "y":
            srcordest = input("Change source (1) or destination (2)\n")
            if srcordest == '1':
                change_src()
                alsodest = input("Do you also want to change the destination? y/n\n")
                if alsodest == 'y':
                    change_dest()
            if srcordest == '2':
                change_dest()
                alsosrc = input("Do you also want to change the source? y/n\n")
                if alsosrc == 'y':
                    change_dest()
        if change == "n":
            print("No changes made to source or destination folder\n")


# Change source folder if called
# Asks for user input - writes the input to a file
def change_src():
    global source
    source = input("Input the full path to the source folder to backup :\n")
    sourcefile = open('/Users/nle/Desktop/Backup Python/srcfile', 'w')
    sourcefile.writelines(source)
    print("New source: " + source)


# Change destination folder if called
# Asks for user input - writes the input to a file
def change_dest():
    global destination
    destination = input("Input the full path to the destination folder for your backup :\n")
    destinationfile = open('/Users/nle/Desktop/Backup Python/destfile', 'w')
    destinationfile.writelines(destination)
    print("New destination: " + destination)


# **************
# Backup methods
# **************

# Full backup
# Loops through files in source directory and copies them to destination directory
# Creates CSV file to log changes
def full():
    with open('/Users/nle/Desktop/Backup Python/Backup.csv', 'w') as csvWritefile:
        writer = csv.writer(csvWritefile, delimiter=';')
        print("Backing up files...")
        src = os.listdir(source)
        headings = ["Filename", "File Size", "Date backed up"]
        writer.writerow(headings)
        for files in src:
            if not files.startswith('.' or '~'):
                row = [files]
                filesize = os.stat(source + files).st_size
                row.append(filesize)
                row.append(timestr_date)
                # row.append(timestr_onlytime)
                shutil.copy2(source + files, destination)
                writer.writerow(row)
        print("Files backed up")
        logfile = open(destination + 'backuplog', 'a')
        log = ("\nFull backup created date " + timestr_date + " at " + timestr_onlytime)
        logfile.writelines(log)


# "Incremental Backup"
# Creates CSV file to compare files currently backed up, to files in the source folder
# If the CSV files are not the same, a backup will be started
def incremental():
    # Create new CSV to be able to compare file size
    with open('/Users/nle/Desktop/Backup Python/CSVnew.csv', 'w') as csvWritefile:
        writer = csv.writer(csvWritefile, delimiter=';')
        src = os.listdir(source)
        headings = ["Filename", "File Size", "Date backed up"]
        writer.writerow(headings)
        for files in src:
            if not files.startswith('.' or '~$'):
                row = [files]
                filesize = os.stat(source + files).st_size
                row.append(filesize)
                row.append(timestr_date)
                # row.append(timestr_onlytime)
                writer.writerow(row)

    # Read lines in CSV files
    with open('/Users/nle/Desktop/Backup Python/Backup.csv', 'r') as csv_old:
        file1 = csv_old.readlines()
    with open('/Users/nle/Desktop/Backup Python/CSVnew.csv') as csv_new:
        file2 = csv_new.readlines()

    # Compare CSV files
    count = 0
    changes = 0
    for i in file1:
        if i != file2[count]:
            changes += 1
        count += 1
    print("Number of files changed:")
    print(changes)

    # If changes are found, copy files again
    if changes != 0:
        print("Number of files changed:")
        print(changes)
        copy_files()

    # Delete CSV file created
    os.remove("/Users/nle/Desktop/Backup Python/CSVnew.csv")


# Method to copy files
def copy_files():
    with open('/Users/nle/Desktop/Backup Python/Backup.csv', 'w') as csvWritefile:
        writer = csv.writer(csvWritefile, delimiter=';')
        print("Backing up files...")
        src = os.listdir(source)
        headings = ["Filename", "File Size", "Date backed up"]
        writer.writerow(headings)
        for files in src:
            if not files.startswith('.' or '~$'):
                row = [files]
                filesize = os.stat(source + files).st_size
                row.append(filesize)
                row.append(timestr_date)
                # row.append(timestr_onlytime)
                shutil.copy2(source + files, destination)
                writer.writerow(row)
        print("Files backed up")
        logfile = open(destination + 'backuplog', 'a')
        log = ("\nIncremental backup created date " + timestr_date + " at " + timestr_onlytime)
        logfile.writelines(log)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # First run check if source and destination are set
    check_srcdest()

    # Check if destination folder is empty
    # If the folder is empty, start a full backup
    hiddenfiles = os.listdir(destination)
    if '.DS_Store' in hiddenfiles:
        hiddenfiles.remove('.DS_Store')
    if not hiddenfiles:
        print("Destination folder empty - starting full backup")
        full()

    # Run a full backup on Sundays
    # If it is not Sunday - only run a backup if files have changed
    if timestr_weekday == "Sunday":
        full()
    else:
        incremental()