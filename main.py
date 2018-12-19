#!/usr/bin/env python3

import os
import sys
import optparse
import json

import fileio as fio
import datetime as dt

from moodle import MoodleUser
import moodle

class Main:

    def __init__(self):
        self.users = []
        self.entries = []

    """ Main method """
    def start(self):

        # Make sure all arguments are valid
        if(not self.checkArgs()):
            print("Invalid program usage! Proper:\n./main.py <logFile> <gradesFile> [-b <blacklistFile.ext>]")
            return

        # Load users
        self.loadUsers()

        # Parse log file
        self.entries = moodle.parseLogEntries(self.logFile)


        print("\n")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

        print("~~USERS~~")
        print("Total # of users: " + str(len(self.users)))
        print("Total # of real (student) users: " + str(len(self.getWhitelistedUsers())))


        print("~~LOGS~~")
        print("Total # of log entries: " + str(len(self.entries)))

        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("\n")

        # First time users accessed the course
        self.writeFirstAccessTimeAndDate()
        # Write who never accessed
        self.writeNeverAccessed()
        # Last time users accessed the course
        self.writeLastAccessTimeAndDate()
        # Write most popular first activities
        self.writeMostPopularFirstActivities()
        # Write most popular activities
        self.writeMostPopularActivities()


    """
    Checks to make sure the required arguments are present
    Returns true if all arguments are present and valid
    """
    def checkArgs(self):
        # Log file parameter
        self.logFile = sys.argv[1] if len(sys.argv) >= 2 else None
        self.gradesFile = sys.argv[2] if len(sys.argv) >= 3 else None
        if(self.logFile is None or self.gradesFile is None):
            return False
        # optional parameters
        parser = optparse.OptionParser()
        parser.add_option('-b', action="store", dest="blacklistFile", default="")
        options, args = parser.parse_args()
        # Blacklist file parameter
        blacklist = None
        blacklistFile = options.blacklistFile
        if blacklistFile:
            blacklist = fio.loadListFromFile(blacklistFile, '\n')
            self.blacklist = blacklist
            print("Loaded " + str(len(blacklist)) + " entries from the blacklist file (" + blacklistFile + ")")
        return True


    """
    Loads users from the grades file
    """
    def loadUsers(self):
        if(not self.gradesFile):
            print("Can't load users without the grades file!")
            return
        with open(self.gradesFile) as f:
            data = json.load(f)

            for i in range(0, len(data)):
                user = MoodleUser()
                user.first_name = data[i]['First name']
                user.last_name = data[i]['Last name']
                user.moodle_id = data[i]['Moodle ID']
                user.email = data[i]['Email address']
                user.netid = user.email.replace('@plattsburgh.edu', '')
                
                user.quizzes = {} # TODO 

                rawCT = data[i]['Course Total'].replace(' ','').replace('%','').replace('-','0')
                user.course_total = float(rawCT)
                self.users.append(user)
        print("Loaded " + str(len(self.users)) + " users")


    """
    Writes first access time & date for users to a file
    """
    def writeFirstAccessTimeAndDate(self, whitelistedOnly = True):
        first_access = []
        for u in self.getWhitelistedUsers() if whitelistedOnly else self.users:
            ele = moodle.getEarliestLogEntry(self.entries, u.getFullName())
            if(not ele):
                continue
            s = ele.fullName + "\t" + str(ele.date) + "\t" + str(ele.time)
            first_access.append(s)
        fio.saveListToFile("first-access.txt", first_access, '\n', False, "output")
    
    """
    Writes the list of users who have never accessed the course
    """
    def writeNeverAccessed(self, whitelistedOnly = True):
        never_accessed = []
        for u in self.getWhitelistedUsers() if whitelistedOnly else self.users:
            ele = moodle.getEarliestLogEntry(self.entries, u.getFullName())
            if(not ele):
                never_accessed.append(u.getFullName())
        fio.saveListToFile("never-accessed.txt", never_accessed, '\n', False, "output")


    """
    Writes first access time & date for users to a file
    """
    def writeLastAccessTimeAndDate(self, whitelistedOnly = True):
        last_access = []
        for u in self.getWhitelistedUsers() if whitelistedOnly else self.users:
            ele = moodle.getLatestLogEntry(self.entries, u.getFullName())
            if(not ele):
                continue
            s = ele.fullName + "\t" + str(ele.date) + "\t" + str(ele.time)
            last_access.append(s)
        fio.saveListToFile("last-access.txt", last_access, '\n', False, "output")

    """
    Writes the most popular first activities of users
    """
    def writeMostPopularFirstActivities(self, whitelistedOnly = True):
        activities = moodle.getMostPopularFirstActivities(self.entries, self.getWhitelistedUsers() if whitelistedOnly else self.users)
        fio.saveDictToFile("most-popular-first-activities.txt", activities, '\n', False, "output")

    """
    Writes the most popular activities
    """
    def writeMostPopularActivities(self):
        activities = moodle.getMostPopularActivities(self.entries)
        fio.saveDictToFile("most-popular-activities.txt", activities, '\n', False, "output")





    

    """
    Filters out the blacklisted users from the total users
    Returns the filtered list
    """
    def getWhitelistedUsers(self):
        result = []
        for u in self.users:
            if(not (u.first_name + " " + u.last_name) in self.blacklist):
                result.append(u)
        return result



"""Root method called by Python"""
if __name__ == "__main__":
    try:
        main = Main()
        main.start()
    except KeyboardInterrupt:
        print('')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
