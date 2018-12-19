#!/usr/bin/env python3

import json
import re

from datetime import DateTime


courseTitlePattern = re.compile(r"Course:\s[A-Za-z\\040]+")


class MoodleUser:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.moodle_id = ""
        self.netid = ""
        self.email = self.netid + "@plattsburgh.edu"
        self.quizzes = []
        self.course_total = 0.00
        
    def getFullName(self):
        return self.first_name + " " + self.last_name


"""
Log Entry object
    Represents a single entry in a moodle log
    Serves only as read-only
    Valid as of [July 23rd 2018]
"""
class LogEntry:

    """ Constructor """
    def __init__(self, rawData):
        # "07\/24\/18, 20:40"
        # "Michael Gates"
        # -"
        # "Course: GEO Academy"
        # "Logs"
        # "Log report viewed"
        # "The user with id '169105' viewed the log report for the course with id '16632'."
        # "web"
        # "68.191.10.94"

        # ARRAY POSITION 0: Date and Time
        rawDateTime = rawData[0]
        if(DateTime.isValidDateTime(rawDateTime)):
            self.date = DateTime.extractDate(rawDateTime)
            self.time = DateTime.extractTime(rawDateTime)
        # ARRAY POSITION 1: User full name
        self.fullName = rawData[1]
        # ARRAY POSITION 2: Affected user or -
        self.affectedFullName = rawData[2]
        # ARRAY POSITION 3: Event context (Course name)
        self.eventContext = rawData[3]
        # ARRAY POSITION 4: Component (Thing)
        self.component = rawData[4]
        # ARRAY POSITION 5: Event Name (What they did)
        self.eventName = rawData[5]
        # ARRAY POSITION 6: Description
        self.description = rawData[6]
        # ARRAY POSITION 7: Origin (web, console, etc.)
        self.origin = rawData[7]
        # ARRAY POSITION 8: IP Address
        self.ip = rawData[8]


"""
"""
def parseLogEntries(fileName):
    entries = []
    with open(fileName) as f:
        data = json.load(f)
        dataArr = data[0]
        total = 0
        for i in reversed(range(0, len(dataArr))):
            entry = LogEntry(data[0][i])
            entries.append(entry)
            total += 1
        print("Parsed " + str(total) + " log entries")
    return entries

"""
Allows you to get the earliest log entry
Optional to get for a specific user
    Returns the earliest log entry
"""
def getEarliestLogEntry(entries, name = None, filterCourseTitle = False):
    earliest = None
    for e in entries:
        if(filterCourseTitle and re.match(courseTitlePattern, e.eventContext)):
            continue
        if(name and name != e.fullName):
            continue
        tempdt = DateTime(e.date,e.time)
        if(not earliest or tempdt < DateTime(earliest.date,earliest.time)):
            earliest = e
    return earliest

"""
Allows you to get the latest log entry
Optional to get for a specific user
    Returns the latest log entry
"""
def getLatestLogEntry(entries, name = None, filterCourseTitle = False):
    latest = None
    for e in entries:
        if(filterCourseTitle and re.match(courseTitlePattern, e.eventContext)):
            continue
        if(name and name != e.fullName):
            continue
        tempdt = DateTime(e.date,e.time)
        if(not latest or tempdt > DateTime(latest.date,latest.time)):
            latest = e
    return latest


"""
Gets the most popular first activities that users click on
"""
def getMostPopularFirstActivities(entries, users):
    activities = {}
    for u in users:
        ele = getEarliestLogEntry(entries, u.getFullName(), True)
        if not ele:
            continue
        val = ele.eventContext
        if val in activities:
            activities[val] += 1
        else:
            activities[val] = 1
    return activities


"""
Gets the most popular activities that users click on
"""
def getMostPopularActivities(entries):
    activities = {}
    for e in entries:
        activity = e.eventContext
        if(len(activity) < 1 or 'Label' in activity):
            continue
        if activity in activities:
            activities[activity] += 1
        else:
            activities[activity] = 1
    # print('\n'.join(['{1} {0}'.format(k, v) for k,v in dict.items()]))
    return activities





"""
def getUniqueUsersBetween(entries, users, beginDate, endDate, beginTime, endTime):
    unique_users = []
    for entry in self.entries:
        name = entry.fullName
        if name in unique_users or name == "-":
            continue
        if(beginDate and entry.date < beginDate):
            continue
        if(endDate and entry.date > endDate):
            continue
        if(beginTime and entry.time < beginTime):
            continue
        if(endTime and entry.time > endTime):
            continue
        unique_users.append(name)
    return unique_users

def getUniqueDailyUsers(users, startDate, endDate):
    alreadyRecorded = [] # overall users
    currentDate = startDate
    while(currentDate <= endDate):
        rawList = self.fetchUniqueUsersBetween(currentDate, currentDate, None, None)
        loopList = []
        for item in rawList:
            if item not in alreadyRecorded:
                loopList.append(item)
                alreadyRecorded.append(item)
        fio.saveListToFile(io.simplifyFileName(str(currentDate)) + ".txt", loopList, '\n', False, "output/all-daily-unique-users")
        currentDate = currentDate.tomorrow()
"""