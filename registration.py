import streamlit as st
import pandas as pd
import pymongo as db
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder

#implementing w/o streamlit, will encorporate streamlit later



#read all course data from a csv file
def readCSV(file_path, collection):

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
def keyWordSearch(collection):
    #STREAMLIT: textbox & enter
    keyWords = st.text_input(label="Keyword Search",placeholder="Enter three keywords")
    if keyWords != None:
        keyList = list(keyWords.split(" "))
    #vv csv data source file vv
        regex_patterns = [f".*{keyword}.*" for keyword in keyList]

        filter = {"KeyWords": {"$regex": "|".join(regex_patterns), "$options": "i"}}
        serached = list(collection.find(filter,{ "_id": 0, "Course Code": 1, "Class":1, "Title": 1, "Days" : 1, "Time": 1, "Instructor": 1}))
        return serached
    
    return list()
    #
    


def update_dataframe(picked_course, collection):
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
    collection.delete_many(filter)

def display_list(list):
    AGlist = pd.DataFrame(list)
    builder = GridOptionsBuilder.from_dataframe(AGlist)
    builder.configure_selection('multiple', use_checkbox=True)
    built = builder.build()
    # st.dataframe(AGlist)
    return_value = AgGrid(AGlist,built)
    #https://discuss.streamlit.io/t/how-to-keep-streamlit-ag-grid-selected-rows-after-page-update/38611/2
    if return_value['selected_rows']:
        temp = return_value['selected_rows']
        print(return_value['selected_rows'])
        # print(temp[0]['Course Code'])
        update_dataframe(temp[-1]['Course Code'], list)


def parseResults(collection):
    #STREAMLIT: clickable list &
    st.write('Results:')
    # AgGrid(collection)
    # df = pd.DataFrame(list(tweets.find()))
    #moemen
    kws = keyWordSearch(collection)
    if (kws == list()):
        display_list(list(collection.find({},{ "_id": 0, "Course Code": 1, "Class":1, "Title": 1, "Days" : 1, "Time": 1, "Instructor": 1})))
        #st.dataframe(list(collection.find({},{ "_id": 0, "Course Code": 1, "Class":1, "Title": 1, "Days" : 1, "Time": 1, "Instructor": 1})))
    else:
        display_list(kws)
    
    
    submit = st.button("Submit")
    if submit:
        print(".")
        
    #
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
    collection.delete_many({})

    readCSV("csdata.csv", collection)
    #keyWordSearch(collection)
    keyList = ["oral"]
    #vv csv data source file vv

    parseResults(collection)

    client.close()
main()