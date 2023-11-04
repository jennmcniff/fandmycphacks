import streamlit as st
import pandas as pd
import csv

#performs keyword search on dataset
def keyWordSearch():
    keyWords = str(input("Enter three keywords: "))
    keyList = list(keyWords.split(" "))
    #vv csv data source file vv

    courseOfferings = list() #= pd.read_csv("csdata.csv") #= list()
    with open("csdata.csv", "r") as f:
        reading = csv.reader(f,delimiter=",")
        for row in reading:
            courseOfferings.append(row)
    courseList = list()
    for each in keyList:
        print(each)
        for course in courseOfferings:
            print(course[2])
            #course[2] is course title
            #if current keyword is within course title and course isn't already in courseList
            #print(course[2].lower().find(each) != -1)
            #print(course not in courseList)
            if (each in course[2].lower()) and (course not in courseList):
                print("rel")
                #relevantData = [title, crn, course #, days, timeslot, prof]
                relevantData = list([course[2], course[0], course[1], course[5], course[6], course[8]])
                courseList.append(relevantData)
    print(courseList)
    return courseList



def main():
    print("starting out")
    potentialCourses = keyWordSearch()


main()