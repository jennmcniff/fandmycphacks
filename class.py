import pandas as pd
import pymongo as db



def main():
    client = db.MongoClient('mongodb://localhost:27017/')

    mydb = client['CW']

    collection = mydb['Courses_Keywords']
    
    file_path = "csdata.csv"

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
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    data = df.to_dict(orient='records')
    collection.insert_many(data)


    keyList = ["Dynamic", "fund"] 
    #vv csv data source file vv
    regex_patterns = [f".*{keyword}.*" for keyword in keyList]

    filter = {"KeyWords": {"$regex": "|".join(regex_patterns), "$options": "i"}}
    serached = collection.find(filter)


    for document in serached:
        print(document)

    print("OOps")

    collection.delete_many({})
    client.close()



    
    #df.to_json('data.json', orient='records', lines=True, date_format='iso', default_handler=str)



    









main()