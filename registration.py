import streamlit as st
import pandas as pd
import csv

#implementing w/o streamlit, will encorporate streamlit later

#performs keyword search on dataset
def keyWordSearch():
    #STREAMLIT: textbox
    keyWords = str(input("Enter three keywords: "))
    #
    keyList = list(keyWords.split(" "))
    #vv csv data source file vv
    courseOfferings = list()
    with open("csdata.csv", "r") as f:
        reading = csv.reader(f,delimiter=",")
        for row in reading:
            courseOfferings.append(row)
    courseList = list()
    for each in keyList:
        print(each)
        for course in courseOfferings:
            print(course[2])
            #if current keyword is within course title and course isn't already in courseList
            if (each in course[2].lower()) and (course not in courseList):
                #relevantData = [title, crn, course #, days, timeslot, prof]
                relevantData = list([course[2], course[0], course[1], course[5], course[6], course[8]])
                courseList.append(relevantData)
    #print(courseList)
    return courseList

def parseResults(potentialCourses):
    #STREAMLIT
    print("select a potential course")
    for each in potentialCourses:
        print(each)
    #
    #user select course


def main():
    potentialCourses = keyWordSearch()
    parseResults(potentialCourses)


main()