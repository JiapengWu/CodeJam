# -*- coding: utf-8 -*-
from data import Data
import operator
import copy

class Schedules():

    def __init__(self):
        self.classAvaiForStu=dict() #name of classes available for each student
        self.nbCoursesForStudents=dict()
        self.nbStudentsForCourses=dict() #number of students for each course
        self.CourseRegistration=dict()
        self.nbStudentForCourseOfStudenti=dict()
        self.conflictsDict=dict()
        self.CourseResgisteredForStudent=dict()
        self.studentSchedule=dict()

    def buildAvailabilities(self):
        for i, student in Data.students.items():

            self.classAvaiForStu[i] = []
            for avail, section in student[1].items():
                day=section["day"]
                start=section["start"]
                end=section["end"]
                #split the student's starting time in to Hour and Minute ,am or pm
                if not ":" in start:
                    continue
                else:
                    startH=float(start.split(':')[0])
                    if start.split(':')[1][2:] == 'pm' and startH != 12: #add 12h if pm
                        startH += 12
                    startH += float(start.split(':')[1][0:2]) / 60 #add the minutes * 1/60
                    #same thing for end
                    endH=float(end.split(':')[0])
                    if end.split(':')[1][2:] == 'pm' and endH != 12:
                        endH += 12
                    endH += float(end.split(':')[1][0:2]) / 60
                    for n, item in Data.classes.items():
                        for time, section in item["times"].items():
                            if section["day"]==day:
                                #courseStart is the hour the course begins
                                courseStart = section["start"]
                                courseStartH=float(courseStart.split(':')[0])
                                if courseStart.split(':')[1][2:] == 'pm' and courseStartH != 12:
                                    courseStartH += 12
                                courseStartH += float(courseStart.split(':')[1][0:2]) / 60
                                #couresEnd is the ending time of the course, splited into hour,minute and am/pm
                                courseEnd = section["end"]
                                courseEndH=float(courseEnd.split(':')[0])

                                if courseEnd.split(':')[1][2:] == 'pm' and courseEndH != 12:
                                    courseEndH += 12
                                courseEndH += float(courseEnd.split(':')[1][0:2]) / 60
                                #now check if course sections exist for this avaialability
                                if not (startH <= courseStartH and endH >= courseEndH):
                                    continue
                                else:
                                    self.classAvaiForStu[i].append((item["name"], time))
    

    def studentsForCourses(self):
        #count number of students that can attend each course
        for n, item in Data.classes.items():
            self.nbStudentsForCourses[(item["name"], "time1")] = 0
            self.nbStudentsForCourses[(item["name"], "time2")] = 0
        for i, courses in self.classAvaiForStu.items():
            for (course, time) in courses:
                self.nbStudentsForCourses[(course, time)] += 1
        
    def coursesForStudents(self):
        #count number of courses that each student can attend
        for i, student in self.classAvaiForStu.items():
            self.nbCoursesForStudents[i] = len(self.classAvaiForStu[i])
           
# 1. number of student
# 2. index 0 for name; index 1 for availabilities
# 3. number of availability
# 4. day, start or end




    def buildSolution(self):
        self.conflictsDict = {('Music', 'time1') : [('Music', 'time2'), ('History', 'time1')],
                          ('Biology', 'time2') : [('Biology', 'time1'), ('Music', 'time2'), ('History', 'time2')],
                          ('Programming', 'time2') : [('Programming', 'time1'), ('Sociology', 'time2')],
                          ('Chemistry', 'time2') : [('Chemistry', 'time1')],
                          ('Sociology', 'time1') : [('Sociology', 'time2')],
                          ('Programming', 'time1') : [('Programming', 'time2')],
                          ('History', 'time2') : [('History', 'time1'), ('Music', 'time2'), ('Biology', 'time2')],
                          ('English', 'time2') : [('English', 'time1'), ('Biology', 'time1')],
                          ('French', 'time1') : [('French', 'time2'), ('Mathematics', 'time1')],
                          ('Chemistry', 'time1') : [('Chemistry', 'time2')],
                          ('Mathematics', 'time1') : [('Mathematics', 'time2'), ('French', 'time1')],
                          ('Biology', 'time1') : [('Biology', 'time2'), ('Physics', 'time2'), ('English', 'time2')],
                          ('History', 'time1') : [('History', 'time2'), ('Music', 'time1')],
                          ('Mathematics', 'time2') : [('Mathematics', 'time1'), ('French', 'time2'), ('Physics', 'time1')],
                          ('Physics', 'time2') : [('Physics', 'time1'), ('Biology', 'time1')],
                          ('French', 'time2') : [('French', 'time1'), ('Mathematics', 'time2'), ('Physics', 'time1')],
                          ('Physics', 'time1') : [('Physics', 'time2'), ('Mathematics', 'time2'), ('French', 'time2')],
                          ('English', 'time1') : [('English', 'time2')],
                          ('Music', 'time2') : [('Music', 'time1'), ('Biology', 'time2'), ('History', 'time2')],
                          ('Sociology', 'time2') : [('Sociology', 'time1'), ('Programming', 'time2')]}
        
        self.CourseResgisteredForStudent=copy.deepcopy(self.nbCoursesForStudents)
        for n,m in self.CourseResgisteredForStudent.items():
            self.CourseResgisteredForStudent[n]=[]
        
        self.CourseRegistration=copy.deepcopy(self.nbStudentsForCourses)
        #print self.nbStudentsForCourses
        for n,m in self.CourseRegistration.items():
            self.CourseRegistration[n]=0

        #copy the course names and initialize each of the correspoding number to zero (CourseRegistration)
        sorted_nbCoursesForStudents=sorted(self.nbCoursesForStudents.items(), key=operator.itemgetter(1))
	#for student,number in sorted_nbCoursesForStudents 
	#now we are dealing with student i

        self.nbStudentForCourseOfStudenti=dict()

        count=0
        #for course in classAvaiForStu["student"]:# classAvaiForStu["student"] is a course list for student i

        for i,course in self.classAvaiForStu.items():
            for c in course:#c is different courses for student 30
                value1=self.CourseRegistration[c]
                value2=self.nbStudentsForCourses[c]#value is the number of student available for c


                if value1==20:
                    continue
                    #if the course is full, continue
                self.nbStudentForCourseOfStudenti[c]=[]
                self.nbStudentForCourseOfStudenti[c].append(value1)
                self.nbStudentForCourseOfStudenti[c].append(value2)
                #assign value to the student for course of student i

            sorted_nbStudentForCourseOfStudenti=sorted(self.nbStudentForCourseOfStudenti.items(), key=operator.itemgetter(1))

            self.nbStudentForCourseOfStudenti.clear()
            #get the sorted nbStudentForCourseOfStudenti



            for course0,number0 in sorted_nbStudentForCourseOfStudenti:

                if (course0,number0) not in sorted_nbStudentForCourseOfStudenti:continue
 
                for coursesToBeRomoved in self.conflictsDict[course0]:
                    
                    sorted_nbStudentForCourseOfStudenti = [(course1, nb) for (course1, nb) in sorted_nbStudentForCourseOfStudenti if course1 != coursesToBeRomoved]
                    #delete corresponding tuple to be modified

            #removing conflict
            count=0;
            for (course0,number0) in sorted_nbStudentForCourseOfStudenti:

                length=len(sorted_nbStudentForCourseOfStudenti)

                if count<min(5,length):
                    self.CourseRegistration[course0]+=1
                    self.nbStudentsForCourses[course0]-=1
                    self.CourseResgisteredForStudent[i].append(course0) 
                #add 0th-4th course of student, all together 5
                count+=1

        print self.CourseRegistration
        sumC=0
        for (i,course) in self.CourseResgisteredForStudent.items():
            length=len(course)
            sumC+=length

        self.studentSchedule=copy.deepcopy(Data.students)

        for student,another in self.studentSchedule.items():
            del another[0:]
            another = dict()
            another["name"]=Data.students[student][0]
            another["courses"]=[]
            #set the name for this student
            for courses in self.CourseResgisteredForStudent[student]:
                
                if True:
                    tup=list()
                    tup.append(courses[0])
                    

                    for n, item in Data.classes.items():
                        
                        if courses[0] is item["name"]:
                        #see if its Eng
                            for time, section in item["times"].items():

                                if courses[1] in time:
                                #check time1 or 2
                                    courseDay=section["day"]
                                    
                                    tup.append(courseDay)
#
#                                   #courseStart is the hour the course begins
                                    courseStart = section["start"]
                                    courseStartH=float(courseStart.split(':')[0])
                                    if courseStart.split(':')[1][2:] == 'pm' and courseStartH != 12:
                                        courseStartH += 12
                                    courseStartH += float(courseStart.split(':')[1][0:2]) / 60
                                    tup.append(courseStartH)

                                        #couresEnd is the ending time of the course, splited into hour,minute and am/pm
                                    courseEnd = section["end"]
                                    courseEndH=float(courseEnd.split(':')[0])
                                    if courseEnd.split(':')[1][2:] == 'pm' and courseEndH != 12:
                                        courseEndH += 12
                                    courseEndH += float(courseEnd.split(':')[1][0:2]) / 60

                                    tup.append(courseEndH)
                                
                    another["courses"].append(tup)
            self.studentSchedule[student]=another








sche = Schedules()
sche.buildAvailabilities()
sche.coursesForStudents()
sche.studentsForCourses()
sche.buildSolution()
