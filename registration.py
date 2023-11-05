import streamlit as st
import pandas as pd
import pymongo as db
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder
import draw_schedule

#implementing w/o streamlit, will encorporate streamlit later

selected = list()

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


def update_dataframe(picked_course, collection):
    filter = {'Course Code': picked_course}
    result = collection.find_one(filter)
    
    course_days = result["Days"]
    time_conflict_mapping = []
    if course_days == 'M W F' or course_days == 'M W':
        time_conflict_mapping = [
        [0], # MWF 08:00AM-08:50AM
        [1, 2], # MWF 09:00AM-09:50AM. Removed 3
        [2, 1, 4],# MW 09:00AM-10:15AM. Removed 3
        [3],# TR 09:30AM-10:45AM. Removed 1, 2, 4
        [4, 2],# MWF 10:00AM-10:50AM. Removed 3
        [5, 6], # MWF MW 11:00AM-12:15PM
        [6, 5], # W 12:00PM-12:50PM. Removed 7
        [7],# TR 12:30PM-01:45PM. Removed 6, 8
        [8], # MWF 01:00PM-01:50PM. Removed 7
        [9], # MWF 02:00PM-02:50PM
        [10] # TR 06:00PM-07:15PM
        ]
    else:
        time_conflict_mapping = [
        [0], # MWF 08:00AM-08:50AM
        [1, 2], # MWF 09:00AM-09:50AM. Removed 3
        [2, 1, 4],# MW 09:00AM-10:15AM. Removed 3
        [3],# TR 09:30AM-10:45AM. Removed 1, 2, 4
        [4, 2],# MWF 10:00AM-10:50AM. Removed 3
        [5], # TR 11:00AM-12:15PM. Removed 6
        [6], # W 12:00PM-12:50PM. Removed 5, 7
        [7],# TR 12:30PM-01:45PM. Removed 6, 8
        [8], # MWF 01:00PM-01:50PM. Removed 7
        [9], # MWF 02:00PM-02:50PM
        [10] # TR 06:00PM-07:15PM
        ]

    t_slot = result["TimeSlot"]

    time_slots_to_remove = time_conflict_mapping[t_slot]

    filter = {'TimeSlot': {'$in': time_slots_to_remove}}
    collection.delete_many(filter)



def display_list(list):
    AGlist = pd.DataFrame(list)
    builder = GridOptionsBuilder.from_dataframe(AGlist)
    builder.configure_selection('multiple',use_checkbox=True)
    built = builder.build()
    # st.dataframe(AGlist)
    
    return_value = AgGrid(AGlist,built)
    print(selected)
    #https://discuss.streamlit.io/t/how-to-keep-streamlit-ag-grid-selected-rows-after-page-update/38611/2
    if return_value['selected_rows']:
        #pickedOut.append(return_value['selected_rows'])
        temp = return_value['selected_rows']
        updateSelected(return_value['selected_rows'])
        print(return_value['selected_rows'])
        print(temp[0]['Course Code'])
        selected.append([temp[-1]['Course Code'], temp[-1]['Class'],temp[-1]['Title'],temp[-1]['Days'],temp[-1]['Time'],temp[-1]['Instructor']])
        print(selected)
        #print(selected)
        # print(temp[0]['Course Code'])
        update_dataframe(temp[-1]['Course Code'], list)


    courses = [["23140","CS101.102","Fund Comp Sci I","T R","09:30AM-10:45AM","KEC 119","Kambhampaty K",'12','1','01/25/24-05/09/24'], 
            ["23149","CS360.102","Analysis/Algorithms","M W F",'08:00AM-08:50AM',"KEC 119","Zeller D","12",'0','01/25/24-05/09/24'], 
            ["23145","CS320.102","Software Eng/Desgn","M W F",'01:00PM-01:50PM',"KEC 119","Hake D","10","2","01/25/24-05/09/24"], 
            ['23147','CS335.101','Cybersecurity Analy & Appl','T R','06:00PM-07:15PM','KEC 123','Zhelezov G','20','7','01/25/24-05/09/24']]
    submit = st.button("Submit")
    if submit:
        draw_schedule.draw(courses)
        st.image("Your_Course_Schedule.png")
        with open("Your_Course_Schedule.png", "rb") as file:
            dwnld = st.download_button(
                    label="Download schedule",
                    data=file,
                    file_name="Your_Course_Schedule.png",
                    mime="image/png"
                )

    if submit:
        for each in return_value['selected_rows']:
            print('.')
    #return selected

def updateSelected(lst):
    selectedList = pd.DataFrame(lst, columns=['Course Code','Class','Title','Days','Time','Instructor'])

    st.dataframe(selectedList)
    print('.')
    #return selected

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
    
    
        
    #
    #
    #user select course



def main():
    atlas_uri = "mongodb+srv://moemen:mongodb@ycp.2b6vs8k.mongodb.net/test?retryWrites=true&w=majority"
    client = db.MongoClient(atlas_uri)
    mydb = client['CW']
    collection = mydb['Courses_Keywords']
    collection.delete_many({})

    pickedOut = list()


    readCSV("csdata.csv", collection)
    #keyWordSearch(collection)
    keyList = ["oral"]
    #vv csv data source file vv

    parseResults(collection)

    client.close()
main()