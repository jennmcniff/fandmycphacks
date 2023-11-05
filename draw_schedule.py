from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import EventStyles

def draw(courses):
    config = data.CalendarConfig(
        lang='en',
        title='Your Course Schedule',
        dates='Mo - Fr',
        hours='8 - 22',
        mode=None,
        show_date=False,
        show_year=False,
        legend=False,
    )

    color_list = [EventStyles.RED, EventStyles.BLUE, EventStyles.YELLOW, EventStyles.PINK, EventStyles.GRAY]

    calendar = Calendar.build(config)

    for i in range (len(courses)):
        days = courses[i][3].split()
        times = courses[i][4].split('-')
        course_title = courses[i][1] + " (" + courses[i][0] + ")"
        course_name = courses[i][2]
        for j in range(2):
            if ("PM" in times[j]) and ("12:" not in times[j]):
                time_list = times[j].split(':')
                mil_hour = int(time_list[0])
                times[j] = str(mil_hour + 12) + ':' + time_list[1]
                
        for day in days:
            if day == 'M':
                day = 0
            if day == 'T':
                day = 1
            if day == 'W':
                day = 2
            if day == 'R':
                day = 3
            if day == 'F':
                day = 4
            calendar.add_event(day_of_week= day, start=times[0][:5], end=times[1][:5], title=course_title,notes = course_name, style=color_list[i])
            
    calendar.save("Your_Course_Schedule.png")


    #Test_schedule selections:
courses = [["23140","CS101.102","Fund Comp Sci I","T R","09:30AM-10:45AM","KEC 119","Kambhampaty K",'12','1','01/25/24-05/09/24'], 
            ["23149","CS360.102","Analysis/Algorithms","M W F",'08:00AM-08:50AM',"KEC 119","Zeller D","12",'0','01/25/24-05/09/24'], 
            ["23145","CS320.102","Software Eng/Desgn","M W F",'01:00PM-01:50PM',"KEC 119","Hake D","10","2","01/25/24-05/09/24"], 
            ['23147','CS335.101','Cybersecurity Analy & Appl','T R','06:00PM-07:15PM','KEC 123','Zhelezov G','20','7','01/25/24-05/09/24']]
    
draw(courses)