# -*- coding: utf-8 -*-
import schedules
from Tkinter import (Button, Entry, Frame, IntVar, Label, 
                     Menu, Menubutton, StringVar, Tk)

class Interface(Frame):
    def __init__(self, root):
        Frame.__init__(self, root, width=500)
        student = Button(self, text="Student", command=self.addStudentOptions)
        student.grid(row=0, column=0, padx=5, sticky="ew")
        teacher = Button(self, text="Teacher", command=self.addTeacherOptions)
        teacher.grid(row=0, column=1, padx=5, sticky="ew")
        principal = Button(self, text="Principal", command=self.addPrincipalOptions)
        principal.grid(row=0, column=2, padx=3, pady=2, sticky="ew")
        empty = Label(self, width=30, height=10)
        empty.grid(row=3, column=0, columnspan=3)
        self.pack()
        
    def addStudentOptions(self):
        identity = ["Student"]        
        studentID = IntVar()        
        label = Label(self, text="Student ID: ")
        label.grid(row=1, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")
        entry = Entry(self, textvariable=studentID, width=3)
        entry.grid(row=1, column=2, padx=1, pady=1, sticky="nsew")
        def callback(event):
            try:
                i = studentID.get()
                assert i > 0 and i <= 80
            except (ValueError, AssertionError):
                invalidID = Label(self, text="Invalid ID.")
                invalidID.grid(row=2, column=0, columnspan=3, padx=1, pady=1)
            else:
                identity.append(i)                
                self.display(*identity)
        entry.bind("<Return>", callback)
    
    def addTeacherOptions(self):
        identity = ["Teacher"]
        subject = StringVar()
        label = Label(self, text="Course: ")
        label.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        entry = Entry(self, textvariable = subject, width=20)
        entry.grid(row=1, column=1, columnspan=2, padx=1, pady=1, sticky="nsew")
        def callback(event):
            try:
                course = subject.get()
                courses = ["Mathematics", "French", "Physics", "Biology",
                           "Sociology", "Programming", "Chemistry", "Music",
                           "English", "History"]
                assert course in courses
            except AssertionError:
                invalidCourse = Label(self, text="Invalid course.")
                invalidCourse.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            else:
                identity.append(course)
                self.display(*identity)
        entry.bind("<Return>", callback)
    
    def addPrincipalOptions(self):
        identity = ["Principal"]
        def viewSchedule():
            identity.append("Schedule")
            identity.append(studentID.get())
            self.display(*identity)
        def viewSection():
            identity.append("Section")
            print(subject.get())
            identity.append(subject.get())
            self.display(*identity)
        schMb = Menubutton(self, text="View Schedules")
        schMb.menu = Menu(schMb)
        schMb["menu"] = schMb.menu
        studentID = IntVar()
        for n, student in studentSchedules.items():
            schMb.menu.add_radiobutton(label=student["name"], value=int(n),
                                    variable=studentID, command=viewSchedule)
        schMb.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        secMb = Menubutton(self, text="View Course Sections")
        secMb.menu = Menu(secMb)
        secMb["menu"] = secMb.menu
        subject = StringVar()
        for course, sections in courseSections.items():
            secMb.menu.add_radiobutton(label=course, value=course,
                                    variable=subject, command=viewSection)
        secMb.grid(row=1, column=1, columnspan=2, padx=1, pady=1, sticky="nsew")
        
    def display(self, *identity):
        self.destroy()
        Frame.__init__(self, root, background="black")
        #different behaviour for identity of user
        if identity[0] == "Principal":
            if identity[1] == "Schedule":
                self.displayScheduleForPrincipal(identity[2])
            elif identity[1] == "Section":
                self.displaySectionForPrincipal(identity[2])
        elif identity[0] == "Teacher":
            self.displayForTeacher(identity[1])
        elif identity[0] == "Student":
            self.displayForStudent(identity[1])
        self.pack()
    
    def displayScheduleForPrincipal(self, i):
        rows = 21
        columns = 6
        for row in range(rows):
            for column in range(columns):
                empty = Label(self)
                empty.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")        
        identity = Label(self, text=i)
        identity.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        name = Label(self, text=studentSchedules[str(i)]["name"])  #to be modified
        name.grid(row=0, column=1, columnspan=5, padx=1, pady=1, sticky="nsew")
        def changeStudent():
            #name = Label(self, text=studentSchedules[studentID.get()]["name"])#to be modified
            #name.grid(row=0, column=1, columnspan=5, padx=1, pady=1, sticky="nsew")
            bigEmpty = Label(self, background="black")
            bigEmpty.grid(row=2, column=1, rowspan=20, columnspan=5)
            for row in range(rows):
                for column in range(columns):
                    if row > 1 and column > 0:
                        empty = Label(self)
                        empty.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")
            self.displayCourses(studentID.get())
        schMb = Menubutton(self, text="View Schedules")
        schMb.menu = Menu(schMb)
        schMb["menu"] = schMb.menu
        studentID = IntVar()
        for n, student in studentSchedules.items():
            schMb.menu.add_radiobutton(label=student["name"], value=int(n),
                                    variable=studentID, command=changeStudent)
        schMb.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        self.displayTimes()
        self.displayCourses(i)
        
    def displaySectionForPrincipal(self, subject):
        self.course = subject
        rows = 24
        columns = 3
        for row in range(rows):
            for column in range(columns):
                empty = Label(self)
                empty.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")        
        label = Label(self, text=subject)
        label.grid(row=0, column=0, columnspan=3, padx=1, pady=1, sticky="nsew")
        self.sections = courseSections[subject].keys()
        self.noSection = IntVar()
        mb = Menubutton(self, text="Change Section")
        mb.menu = Menu(mb)
        mb["menu"] = mb.menu
        mb.menu.add_radiobutton(label=self.sections[0], value=0, 
                                variable=self.noSection, command=self.displaySection)
        mb.menu.add_radiobutton(label=self.sections[1], value=1, 
                                variable=self.noSection, command=self.displaySection)
        mb.grid(row=2, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")
        def viewSection():
            self.displaySectionForPrincipal(subject.get())
        subject = StringVar()        
        subMb = Menubutton(self, text="Change Subject")
        subMb.menu=Menu(subMb)
        subMb["menu"] = subMb.menu
        for course, sections in courseSections.items():
            subMb.menu.add_radiobutton(label=course, value=course,
                                    variable=subject, command=viewSection)
        subMb.grid(row=2, column=2, padx=1, pady=1, sticky="nsew")
        self.displaySection()
            
    def displayForStudent(self, i):
        #put the table with id and name        
        rows = 20
        columns = 6
        for row in range(rows):
            for column in range(columns):
                empty = Label(self)
                empty.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")        
        identity = Label(self, text=i)
        identity.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        name = Label(self, text=studentSchedules[str(i)]["name"])  #to be modified
        name.grid(row=0, column=1, columnspan=5, padx=1, pady=1, sticky="nsew")
        self.displayTimes()
        self.displayCourses(i)
        
    def displayForTeacher(self, course):
        self.course = course
        rows = 24
        columns = 3
        for row in range(rows):
            for column in range(columns):
                empty = Label(self)
                empty.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")        
        label = Label(self, text=course)
        label.grid(row=0, column=0, columnspan=3, padx=1, pady=1, sticky="nsew")
        self.sections = courseSections[course].keys()
        self.noSection = IntVar()
        mb = Menubutton(self, text="Change Section")
        mb.menu = Menu(mb)
        mb["menu"] = mb.menu
        mb.menu.add_radiobutton(label=self.sections[0], value=0, 
                                variable=self.noSection, command=self.displaySection)
        mb.menu.add_radiobutton(label=self.sections[1], value=1, 
                                variable=self.noSection, command=self.displaySection)
        mb.grid(row=2, column=0, columnspan=3, padx=1, pady=1, sticky="nsew")
        self.displaySection()
        
    def displaySection(self):
        section = self.sections[self.noSection.get()]       
        sectionLabel = Label(self, text=section)
        sectionLabel.grid(row=1, column=0, columnspan=3, padx=1, pady=1, sticky="nsew")
        nbLabel = Label(self, text="No.", width=10)
        nbLabel.grid(row=3, column=0, padx=1, pady=1, sticky="nsew")
        idLabel = Label(self, text="Student ID", width=10)
        idLabel.grid(row=3, column=1, padx=1, pady=1, sticky="nsew")
        nameLabel = Label(self, text="Name", width=30)
        nameLabel.grid(row=3, column=2, padx=1, pady=1, sticky="nsew")
        row = 4
        for item in courseSections[self.course][section]:
            nb = Label(self, text=(row - 3))
            studentID = Label(self, text=item["id"])
            studentName = Label(self, text=item["name"])
            nb.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")
            studentID.grid(row=row, column=1, padx=1, pady=1, sticky="nsew")
            studentName.grid(row=row, column=2, padx=1, pady=1, sticky="nsew")
            row += 1
        
    def displayTimes(self):
        #basic schedule format with times and days   
        time1 = Label(self, text="8:00-8:30", width=12)
        time1.grid(row=2, column=0, padx=1, pady=1, sticky="nsew")
        time2 = Label(self, text="8:30-9:00")
        time2.grid(row=3, column=0, padx=1, pady=1, sticky="nsew")
        time3 = Label(self, text="9:00-9:30")
        time3.grid(row=4, column=0, padx=1, pady=1, sticky="nsew")
        time4 = Label(self, text="9:30-10:00")
        time4.grid(row=5, column=0, padx=1, pady=1, sticky="nsew")
        time5 = Label(self, text="10:00-10:30")
        time5.grid(row=6, column=0, padx=1, pady=1, sticky="nsew")
        time6 = Label(self, text="10:30-11:00")
        time6.grid(row=7, column=0, padx=1, pady=1, sticky="nsew")
        time7 = Label(self, text="11:00-11:30")
        time7.grid(row=8, column=0, padx=1, pady=1, sticky="nsew")
        time8 = Label(self, text="11:30-12:00")
        time8.grid(row=9, column=0, padx=1, pady=1, sticky="nsew")
        time9 = Label(self, text="12:00-12:30")
        time9.grid(row=10, column=0, padx=1, pady=1, sticky="nsew")
        time10 = Label(self, text="12:30-13:00")
        time10.grid(row=11, column=0, padx=1, pady=1, sticky="nsew")
        time11 = Label(self, text="13:00-13:30")
        time11.grid(row=12, column=0, padx=1, pady=1, sticky="nsew")
        time12 = Label(self, text="13:30-14:00")
        time12.grid(row=13, column=0, padx=1, pady=1, sticky="nsew")
        time13 = Label(self, text="14:00-14:30")
        time13.grid(row=14, column=0, padx=1, pady=1, sticky="nsew")
        time14 = Label(self, text="14:30-15:00")
        time14.grid(row=15, column=0, padx=1, pady=1, sticky="nsew")
        time15 = Label(self, text="15:00-15:30")
        time15.grid(row=16, column=0, padx=1, pady=1, sticky="nsew")
        time16 = Label(self, text="15:30-16:00")
        time16.grid(row=17, column=0, padx=1, pady=1, sticky="nsew")
        time17 = Label(self, text="16:00-16:30")
        time17.grid(row=18, column=0, padx=1, pady=1, sticky="nsew")
        time18 = Label(self, text="16:30-17:00")
        time18.grid(row=19, column=0, padx=1, pady=1, sticky="nsew")
        day1 = Label(self, text="Monday", width=15)
        day1.grid(row=1, column=1, padx=1, pady=1, sticky="nsew")
        day2 = Label(self, text="Tuesday", width=15)
        day2.grid(row=1, column=2, padx=1, pady=1, sticky="nsew")
        day3 = Label(self, text="Wednesday", width=15)
        day3.grid(row=1, column=3, padx=1, pady=1, sticky="nsew")
        day4 = Label(self, text="Thursday", width=15)
        day4.grid(row=1, column=4, padx=1, pady=1, sticky="nsew")
        day5 = Label(self, text="Friday", width=15)
        day5.grid(row=1, column=5, padx=1, pady=1, sticky="nsew")
        
    def displayCourses(self, i):
        #show the appropriate courses in the student schedule
        for (subject, day, start, end) in studentSchedules[str(i)]["courses"]:
            row = int((start - 7) * 2)
            rowspan = int((end - 7) * 2) - row
            colors = {"Mathematics" : "light blue", 
                      "Chemistry" : "lime green", 
                      "Biology" : "red", 
                      "Sociology" : "steel blue", 
                      "Music" : "dark violet", 
                      "French" : "coral", 
                      "Physics" : "light salmon",
                      "English" : "dodger blue",
                      "Programming" : "dark olive green",
                      "History" : "yellow"}            
            columns = {"Monday" : 1, 
                       "Tuesday" : 2, 
                       "Wednesday" : 3,
                       "Thursday" : 4,
                       "Friday" : 5}
            label = Label(self, text=subject, background=colors[subject])
            label.grid(row=row, rowspan=rowspan, column=columns[day], padx=1, pady=1, sticky="nsew")
        
#studentSchedules = sche.studentSchedules
#courseSections = sche.courseSections

studentSchedules = {'58': {'courses': [['Programming', 'Wednesday', 15.0, 17.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Friday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0]], 'name': 'BLANCA, BAHENA'}, '30': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Music', 'Thursday', 8.5, 11.0], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'LAZARO, ALTAMIRANO'}, '28': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'TIMOTHY, ALLEN'}, '29': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Friday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0]], 'name': 'SCOTT, AHERN'}, '60': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'RONALD, BADAMI'}, '61': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0]], 'name': 'DAVID, ANDREWS'}, '62': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Friday', 13.0, 15.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'CAMUHOO, AITKEN'}, '63': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['History', 'Friday', 8.0, 10.5], ['Music', 'Thursday', 8.5, 11.0], ['Biology', 'Wednesday', 8.5, 10.5]], 'name': 'LUTHER, ANDERSON'}, '64': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Sociology', 'Friday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['French', 'Monday', 8.5, 10.5]], 'name': 'EVA, AVINA'}, '65': {'courses': [['History', 'Friday', 8.0, 10.5], ['Music', 'Thursday', 8.5, 11.0], ['Biology', 'Wednesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'DAVID, ALPERS'}, '66': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0]], 'name': 'NANCY, ARROYO-FREGOSO'}, '67': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'BAHLEBBY, AMDEMICHAEL'}, '68': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['French', 'Monday', 8.5, 10.5], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'NIKOS, APOSTOLOPOALOS'}, '69': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['Biology', 'Wednesday', 8.5, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'MICHELLE, ASHFORD'}, '80': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Friday', 13.0, 15.0], ['French', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'BILAL, ALI'}, '34': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Friday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['Music', 'Thursday', 8.5, 11.0]], 'name': 'JASON, ARELLANO'}, '24': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['History', 'Friday', 8.0, 10.5], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'TIMOTHY, BAILEY'}, '25': {'courses': [['Programming', 'Wednesday', 15.0, 17.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Sociology', 'Friday', 13.0, 15.0], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'ISABEL, ARENAS'}, '26': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0]], 'name': 'CHRISTOPHER, AKINES'}, '27': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'LOUIS, AGUILAR'}, '20': {'courses': [['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'VINCENT, BALDASSANO'}, '21': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'RAY, AGUILAR'}, '48': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'ROBERT, AMSTADT'}, '49': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'CARRIE, AUSTIN'}, '46': {'courses': [['History', 'Friday', 8.0, 10.5], ['Programming', 'Friday', 13.0, 15.0], ['Chemistry', 'Tuesday', 14.0, 15.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'RONALDO, ANGELES'}, '23': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['History', 'Friday', 8.0, 10.5], ['Programming', 'Friday', 13.0, 15.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0]], 'name': 'MOHAMMED, ABUBAKER'}, '44': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Programming', 'Friday', 13.0, 15.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'JEFFREY, ADAMOW'}, '45': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0]], 'name': 'ALEJANDRO, ALMAZAN'}, '42': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Wednesday', 13.0, 15.0], ['History', 'Friday', 8.0, 10.5], ['Programming', 'Friday', 13.0, 15.0], ['Mathematics', 'Tuesday', 8.0, 10.0]], 'name': 'MARIO, ALONSO'}, '43': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0]], 'name': 'CARA, BADER'}, '40': {'courses': [['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['Sociology', 'Friday', 13.0, 15.0]], 'name': 'BRUCE, ASKEW'}, '41': {'courses': [['Physics', 'Wednesday', 8.0, 10.0], ['Sociology', 'Wednesday', 13.0, 15.0], ['Mathematics', 'Tuesday', 8.0, 10.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'CAROLYN, ALLAIN'}, '1': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Mathematics', 'Tuesday', 8.0, 10.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'CANDELARIO, AQUINO'}, '35': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['History', 'Friday', 8.0, 10.5], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5]], 'name': 'GRACE ANN, ARMOUR'}, '3': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['Music', 'Thursday', 8.5, 11.0], ['French', 'Monday', 8.5, 10.5], ['Biology', 'Wednesday', 8.5, 10.5]], 'name': 'ALEX, ANDERSON'}, '2': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['French', 'Monday', 8.5, 10.5], ['Biology', 'Friday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0]], 'name': 'THERON, AVERETT'}, '5': {'courses': [['Sociology', 'Wednesday', 13.0, 15.0], ['Programming', 'Wednesday', 15.0, 17.0], ['French', 'Monday', 8.5, 10.5], ['Biology', 'Wednesday', 8.5, 10.5], ['History', 'Thursday', 8.5, 11.0]], 'name': 'TERRY, ALLEN'}, '4': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'DANIEL, ANDUJAR'}, '7': {'courses': [['Programming', 'Wednesday', 15.0, 17.0], ['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0]], 'name': 'TIMOTHY, ALLEN'}, '6': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'J, ALDANA'}, '9': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'MARSHALL, ANDREWS JR'}, '8': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'ROSS, ALEXANDER'}, '32': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5]], 'name': 'PATRICK, ASHE'}, '18': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['French', 'Tuesday', 8.0, 10.0], ['Biology', 'Wednesday', 8.5, 10.5], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5]], 'name': 'JOHN, BAJIC'}, '13': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5]], 'name': 'LESTER, BAILEY'}, '77': {'courses': [['French', 'Tuesday', 8.0, 10.0], ['Biology', 'Wednesday', 8.5, 10.5], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'FABIAN, ALBARRAN'}, '76': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'ROCCO, BALESTRI'}, '75': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'CHRIS, ANDERSEN'}, '12': {'courses': [['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'WILLIAM, ABBRUZZESE'}, '73': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'ELIZABETH, ALCANTARA'}, '72': {'courses': [['History', 'Thursday', 8.5, 11.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Mathematics', 'Monday', 8.5, 10.5], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'EARL, ALEXANDER'}, '71': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'DEBRA, ANTHONY SANDERS'}, '70': {'courses': [['Programming', 'Friday', 13.0, 15.0], ['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'MICHAEL, BAILEY'}, '15': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['History', 'Thursday', 8.5, 11.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Mathematics', 'Monday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'GRACE, AKINLEMIBOLA'}, '79': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['Mathematics', 'Monday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'BAHLEBBY, AMDEMICHAEL'}, '78': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'MIGUEL, BAHENA'}, '11': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Sociology', 'Friday', 13.0, 15.0], ['Mathematics', 'Monday', 8.5, 10.5]], 'name': 'CHRISTOPHER, AKINES'}, '10': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['History', 'Thursday', 8.5, 11.0], ['Sociology', 'Friday', 13.0, 15.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'MARK, ANDERSEN'}, '39': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['Sociology', 'Friday', 13.0, 15.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5]], 'name': 'MARY, ACCURSO'}, '38': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['Sociology', 'Friday', 13.0, 15.0], ['History', 'Thursday', 8.5, 11.0], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'CLARISSA, ACEVEDO'}, '59': {'courses': [['Biology', 'Friday', 8.0, 10.0], ['French', 'Tuesday', 8.0, 10.0], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Tuesday', 14.0, 15.5]], 'name': 'LESTER, ANDERSON'}, '22': {'courses': [['History', 'Thursday', 8.5, 11.0], ['Mathematics', 'Monday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Chemistry', 'Tuesday', 14.0, 15.5], ['Physics', 'Tuesday', 8.5, 10.5]], 'name': 'ABEL, AZUL'}, '14': {'courses': [['French', 'Tuesday', 8.0, 10.0], ['Mathematics', 'Monday', 8.5, 10.5], ['English', 'Wednesday', 10.0, 11.5], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'JAIME, ALVARADO'}, '16': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Mathematics', 'Monday', 8.5, 10.5], ['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'BLAIR, ALTENBACH'}, '19': {'courses': [['French', 'Tuesday', 8.0, 10.0], ['Sociology', 'Friday', 13.0, 15.0], ['Music', 'Friday', 8.0, 10.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'EDWARD, ANNUNZIO'}, '54': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'HASSAN, ABOUELKHEIR'}, '31': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'CHRISTOPHER, ALONZO'}, '56': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'JAMES, ALLEN'}, '51': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'MARIE, ALLEN'}, '36': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0]], 'name': 'DAVID, ADAMS'}, '53': {'courses': [['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'JUANITA, AGUILAR'}, '52': {'courses': [['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'ALESIA, ARELLANO'}, '33': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'MAJED, ASSAF'}, '55': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'JOSE, ALVAREZ'}, '74': {'courses': [['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'MICHAEL, AUSTIN'}, '37': {'courses': [['Biology', 'Wednesday', 8.5, 10.5], ['Music', 'Friday', 8.0, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'CONSTANTINE, ARGIRIS'}, '47': {'courses': [['Sociology', 'Friday', 13.0, 15.0], ['Biology', 'Wednesday', 8.5, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'SANDRA, ALLEN'}, '17': {'courses': [['Biology', 'Wednesday', 8.5, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'SAMUEL, ALEGADO'}, '57': {'courses': [['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'RAGINA, BAGGETTE'}, '50': {'courses': [['Biology', 'Wednesday', 8.5, 10.5], ['Physics', 'Tuesday', 8.5, 10.5], ['English', 'Tuesday', 10.5, 12.0], ['Chemistry', 'Monday', 10.5, 12.0]], 'name': 'HIRAM, ARAGONES'}}

courseSections = {
        "Mathematics": {"Monday 8:30am - 10:30am": 
            [{"id": 1, "name": "CANDELARIO, AQUINO"},
             {"id": 10, "name": "MARK, ANDERSEN"},
             {"id": 11, "name": "CHRISTOPHER, AKINES"},
             {"id": 12, "name": "WILLIAM, ABBRUZZESE"},
             {"id": 1, "name": "CANDELARIO, AQUINO"},
             {"id": 10, "name": "MARK, ANDERSEN"},
             {"id": 11, "name": "CHRISTOPHER, AKINES"},
             {"id": 12, "name": "WILLIAM, ABBRUZZESE"},
             {"id": 1, "name": "CANDELARIO, AQUINO"},
             {"id": 10, "name": "MARK, ANDERSEN"},
             {"id": 11, "name": "CHRISTOPHER, AKINES"},
             {"id": 12, "name": "WILLIAM, ABBRUZZESE"},
             {"id": 1, "name": "CANDELARIO, AQUINO"},
             {"id": 10, "name": "MARK, ANDERSEN"},
             {"id": 11, "name": "CHRISTOPHER, AKINES"},
             {"id": 12, "name": "WILLIAM, ABBRUZZESE"},
             {"id": 1, "name": "CANDELARIO, AQUINO"},
             {"id": 10, "name": "MARK, ANDERSEN"},
             {"id": 11, "name": "CHRISTOPHER, AKINES"},
             {"id": 12, "name": "WILLIAM, ABBRUZZESE"}],
        "Tuesday 8:00am - 10:00am":
            [{"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"},
             {"id": 19, "name": "EDWARD, ANNUNZIO"}]}}



if __name__ == "__main__":
    root = Tk()    
    app = Interface(root)
    app.mainloop()
        #table.redrawTable()