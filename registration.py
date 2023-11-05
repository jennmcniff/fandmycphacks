import streamlit as st
import pandas as pd
import pymongo as db

#implementing w/o streamlit, will encorporate streamlit later

client = db.MongoClient('mongodb://localhost:27017/')

mydb = client['CW']

collection = mydb['Courses_Keywords']

#read all course data from a csv file
def readCSV(file_path, collection):
    collection.delete_many({})

    df = pd.read_csv(file_path)

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
    def map_time_to_number(time_str):
        return time_slot_dict.get(time_str, -1)
    df['TimeSlot'] = df['Time'].apply(map_time_to_number)

    data = df.to_dict(orient='records')
    collection.insert_many(data)

#performs keyword search on dataset
def keyWordSearch():
    #STREAMLIT: textbox & enter
    keyWords = st.text_input(label="Keyword Search",placeholder="Enter three keywords")
    #
    keyList = list(keyWords.split(" "))
    #vv csv data source file vv
    filtered_df = df[~df['KeyWords'].isin(keyList)]
    filtered_df = filtered_df.reset_index(drop=True)

    #print(courseList)
    return filtered_df

def update_dataframe(picked_course):
    time_conflict_mapping = [
    [0],
    [1, 2, 3],
    [2, 1, 3, 4],
    [3, 1, 2, 4],
    [4, 2, 3],
    [5, 6],
    [6, 5, 7],
    [7, 6, 8],
    [8, 7],
    [9],
    [10]
    ]
        
    filter = {'Course Code': picked_course}
    result = collection.find_one(filter)

    t_slot = result["TimeSlot"]

    time_slots_to_remove = time_conflict_mapping[t_slot]

    filter = {'TimeSlot': {'$in': time_slots_to_remove}}
    update = {'$set': {'hidden': True}}
    collection.update_many(filter, update)



def parseResults(potentialCourses):
    #STREAMLIT: clickable list &
    st.write('Results:')
    st.dataframe(potentialCourses)
    
    #
    for each in potentialCourses:
        print(each)
    #
    #user select course

def buildDisplay():
    #STREAMLIT: calendar display
    print('.')


def main():
    atlas_uri = "mongodb+srv://moemen:mongodb@ycp.2b6vs8k.mongodb.net/test?retryWrites=true&w=majority"
    client = db.MongoClient(atlas_uri)
    mydb = client['CW']
    collection = mydb['Courses_Keywords']

    readCSV("csdata.csv", collection)
    keyWordSearch(collection)
    #parseResults()


main()