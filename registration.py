import streamlit as st
import pandas as pd

#performs keyword search on dataset
#adds 
def keyWordSearch():
    keyWords = str(input("Enter three keywords: "))
    keyList = list(keyWords.split(" "))
    #vv csv data source file vv
    courseOfferings = list()
    courseList = list()
    for each in keyList:
        for course in courseOfferings:
            #course[3] should be course title
            #if current keyword is within course title and course isn't already in courseList
            if (each in course[3]) and (course not in courseList):
                #relevantData = [title, crn, course #, days, timeslot, prof]
                relevantData = list(course[3], course[0], course[1], course[5], course[6], course[8])
                courseList.append(relevantData)
    return courseList



def main():
    print("starting out")
    potentialCourses = keyWordSearch()


main()