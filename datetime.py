#!/usr/bin/env python3

import re

"""
Date object (comparable)
"""
class Date:

    # m[m]/d[d]/yy
    datePattern = re.compile(r"\d{1,2}/\d{1,2}/\d{1,2}")

    """ Constructor """
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    """
        Returns true if the string matches m[m]/d[d]/yy
    """
    def isValidDate(dateStr):
        return re.match(Date.datePattern, dateStr)

    """
        Returns the amount of days in the specified month
    """
    def getDaysInMonth(n):
        if n == 2:
            return 28
        elif n == 4 or n == 6 or n == 9 or n == 11:
            return 30
        else:
            return 31

    """
        Returns the day after the current one which may involve a day, month, or year change
    """
    def tomorrow(self):
        cm = self.month
        cd = self.day
        cy = self.year
        dim = Date.getDaysInMonth(cm)
        cd += 1
        if(cd > dim):
            cd = 1
            cm += 1
            if(cm > 12):
                cm = 1
                cy += 1
                if(cy > 99):
                    cy = 0
        return Date(cm,cd,cy)


    """ 'Equal To' an object """
    def __eq__(self, other):
        return self.month == other.month and self.day == other.day and self.year == other.year

    """ 'Not Equal To' an object """
    def __ne__(self, other):
        return not self.__eq__(other)

    """ 'Greater Than' an object """
    def __gt__(self, other):
        if(self.year > other.year):
            return True
        elif(self.year >= other.year and self.month > other.month):
            return True
        elif(self.year >= other.year and self.month >= other.month and self.day > other.day):
            return True
        else:
            return False

    """ 'Greater Than Equal To' object """
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    """ 'Less Than' object """
    def __lt__(self, other):
        if(self.year < other.year):
            return True
        elif(self.year <= other.year and self.month < other.month):
            return True
        elif(self.year <= other.year and self.month <= other.month and self.day < other.day):
            return True
        else:
            return False

    """ 'Less Than Equal To' object """
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    """ Parses date from string in format mm/dd/yy """
    def parse(rawDate):
        spl = rawDate.split('/')
        return Date(int(spl[0]), int(spl[1]), int(spl[2]))

    """ Converts to string in format mm/dd/yy """
    def __str__(self):
        return ("0" if self.month < 10 else "") + str(self.month) + "/" + ("0" if self.day < 10 else "") + str(self.day) + "/" + ("0" if self.year < 10 else "") + str(self.year)

"""
Time object (comparable)
"""
class Time:

    # h[h]:m[m]
    timePattern = re.compile(r"\d{1,2}:\d{1,2}")

    """ Constructor """
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    """ Parses time from string in format hh:mm """
    def parse(rawTime):
        spl = rawTime.split(':')
        return Time(int(spl[0]), int(spl[1]))

    """
        Returns true if the string matches h[h]:mm
    """
    def isValidTime(timeStr):
        return re.match(Time.timePattern, timeStr)

    """ 'Equal To' an object """
    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    """ 'Not Equal To' an object """
    def __ne__(self, other):
        return not self.__eq__(other)

    """ 'Greater Than' an object """
    def __gt__(self, other):
        if(self.hour > other.hour):
            return True
        if(self.hour >= other.hour and self.minute > other.minute):
            return True
        return False

    """ 'Greater Than Equal To' object """
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    """ 'Less Than' object """
    def __lt__(self, other):
        if(self.hour < other.hour):
            return True
        if(self.hour <= other.hour and self.minute < other.minute):
            return True
        return False

    """ 'Less Than Equal To' object """
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    """ Converts to string in format hh:mm """
    def __str__(self):
        return ("0" if self.hour < 10 else "") + str(self.hour) + ":" + ("0" if self.minute < 10 else "") + str(self.minute)

class DateTime:

    # m[m]/d[d]/yy,h[h]:mm
    # each number is a grouping
    # Group 1 = Full date
    # Group 2 = month MM
    # Group 3 = day DD
    # Group 4 = year YY
    # Group 5 = GARBAGE (comma and space)
    # Group 6 = Full Time
    # Group 7 = hour HH
    # Group 8 = minute MM
    dateTimePattern = re.compile(r"((\d{1,2})\/(\d{1,2})\/(\d{2}))(\,\s)((\d{1,2})\:(\d{2}))")

    def __init__(self, date, time):
        self.date = date
        self.time = time

    """
        Returns true if the string matches m[m]/d[d]/yy,h[h]:mm
    """
    def isValidDateTime(dtStr):
        return re.match(DateTime.dateTimePattern, dtStr)

    """
        Extracts date from a string via regex
        Returns the parsed date if successful
    """
    def extractDate(dtStr):
        res = re.search(DateTime.dateTimePattern, dtStr)
        rawDate = res.group(1)
        parsed = Date.parse(rawDate)
        return parsed

    """
        Extracts time from a string via regex
        Returns the parsed time is succesful
    """
    def extractTime(dtStr):
        res = re.search(DateTime.dateTimePattern, dtStr)
        rawTime = res.group(6)
        parsed = Time.parse(rawTime)
        return parsed

    """ 'Equal To' an object """
    def __eq__(self, other):
        return self.date == other.date and self.time == other.time

    """ 'Not Equal To' an object """
    def __ne__(self, other):
        return not self.__eq__(other)

    """ 'Greater Than' an object """
    def __gt__(self, other):
        if(self.date > other.date):
            return True
        elif(self.date >= other.date and self.time > other.time):
            return True
        else:
            return False

    """ 'Greater Than Equal To' object """
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    """ 'Less Than' object """
    def __lt__(self, other):
        if(self.date < other.date):
            return True
        elif(self.date <= other.date and self.time < other.time):
            return True
        else:
            return False

    """ 'Less Than Equal To' object """
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    """ Converts to string in format mm/dd/yy """
    def __str__(self):
        return str(self.date) + " " + str(self.time)

"""
Asks the user to input a begin/end date(s) for filtering
    Date string is in format mm/dd/yy
    Returns a tuple (string beginDate, string endDate)
"""
def askDateBounds():
    beginDate = None
    rawBeginDate = input("Enter begin date mm/dd/yy (or empty for oldest): ")
    endDate = None
    rawEndDate = input("Enter end date mm/dd/yy (or empty for newest): ")
    # check patterns
    if(Date.isValidDate(rawBeginDate)):
        beginDate = Date.parse(rawBeginDate)
    if(Date.isValidDate(rawEndDate)):
        endDate = Date.parse(rawEndDate)
    return (beginDate if beginDate else Date(1,1,00), endDate if endDate else Date(12,31,99))

"""
Asks the user to input a begin/end time(s) for filtering
    Time string is in format hh:mm
    Returns a tuple (string beginTime, string endTime)
"""
def askTimeBounds():
    beginTime = None
    rawBeginTime = input("Enter start time hh:mm (or empty for earliest): ")
    endTime = None
    rawEndTime = input("Enter end time hh:mm (or empty for latest): ")
    # check patterns
    if(Time.isValidTime(rawBeginTime)):
        beginTime = Time.parse(rawBeginTime)
    if(Time.isValidTime(rawEndTime)):
        endTime = Time.parse(rawEndTime)
    return (beginTime if beginTime else Time(0,0), endTime if endTime else Time(23,59))
