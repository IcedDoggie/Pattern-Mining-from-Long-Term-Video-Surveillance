# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:18:04 2017

@author: Ice
"""

def calendarFunction(currentYear, currentMonth, currentDay, pointerMonth, pointerDay):
    if (pointerMonth == 3) or (pointerMonth == 5) or (pointerMonth == 8) or (pointerMonth == 10):
        if currentDay == '30':
            currentDay = dayArray[0]
            pointerMonth += 1
            currentMonth = monthArray[pointerMonth]
            pointerDay = 0
        else:
            pointerDay += 1
            currentDay = dayArray[pointerDay]
            
    elif pointerMonth == 1:
        if (currentYear%4 == 0) and (currentDay == '28'):#leapyear
            pointerDay += 1
            currentDay = dayArray[pointerDay]
        elif (currentYear%4 == 0) and (currentDay == '29'):#reset to 01 if day ends for the month
            currentDay = dayArray[0]
            pointerDay = 0
            pointerMonth += 1
            currentMonth = monthArray[pointerMonth]
        elif (currentYear%4 != 0) and (currentDay == '28'): #Non Leap year
            currentDay = dayArray[0]
            pointerDay = 0
            pointerMonth += 1
            currentMonth = monthArray[pointerMonth]
        else:
            pointerDay += 1
            currentDay = dayArray[pointerDay]
    else: #for 31 days month
        if currentDay == '30':
            pointerDay += 1
            currentDay = dayArray[pointerDay]
        elif currentDay == '31':
            currentDay = dayArray[0]
            pointerDay = 0
            pointerMonth += 1
            currentMonth = monthArray[pointerMonth]
        else:
            pointerDay += 1
            currentDay = dayArray[pointerDay]

    #if year ends?
    if (pointerMonth == 11) and (pointerDay == 30):
        currentYear += 1
        pointerMonth = 0
        pointerDay = 0
        currentMonth = monthArray[pointerMonth]
        currentDay = dayArray[pointerDay]
    return currentYear, currentMonth, currentDay, pointerMonth, pointerDay
    