import streamlit as st
import pandas as pd
import csv

#implementing w/o streamlit, will encorporate streamlit later

#read all course data from a csv file
def readCSV(file_path):

    time_slot_mapping = [
    ["08:00AM-08:50AM", 0],
    ["09:00AM-09:50AM" , 1],
    ["09:00AM-10:15AM", 2],
    ["09:30AM-10:45AM", 3],
    ["10:00AM-10:50AM", 4],
    ["11:00AM-12:15PM", 5],
    ["12:00PM-12:50PM", 6],
    ["12:30PM-01:45PM", 7],
    ["01:00PM-01:50PM", 8],
    ["02:00PM-02:50PM", 9],
    ["06:00PM-07:15PM", 10],
    ]

    time_slot_dict = dict(time_slot_mapping)

    df = pd.read_csv(file_path)
    
    def map_time_to_number(time_str):
        return time_slot_dict.get(time_str, -1)
    

    df['TimeSlot'] = df['Time'].apply(map_time_to_number)

    return df

#performs keyword search on dataset
def keyWordSearch():
    #STREAMLIT: textbox & enter
    keyWords = st.text_input(label="Keyword Search",placeholder="Enter three keywords")
    #keyWords = str(input("Enter three keywords: "))
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
    #STREAMLIT: clickable list &
    print("select a potential course")
    #
    for each in potentialCourses:
        print(each)
    #
    #user select course

def buildDisplay():
    #STREAMLIT: calendar display
    print('.')


def main():
    readCSV("csdata.csv")
    potentialCourses = keyWordSearch()
    parseResults(potentialCourses)


main()