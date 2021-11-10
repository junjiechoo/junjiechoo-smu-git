# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.dialects.postgresql import INT4RANGE, TIME, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import JSON
from sqlalchemy.schema import FetchedValue
from app import db
import json

# Cheng Hong
class Course(db.Model):
    __tablename__ = 'Course'

    courseId = db.Column(String(8), primary_key=True)
    courseName = db.Column(String(144), nullable=False)
    prereq = db.Column(ARRAY(String(length=8)))
    retireStatus = db.Column(Boolean, nullable=False)

    def setCourseId(self, courseid):
        self.courseId=courseid
    def setCourseName(self, coursename):
        self.courseName = coursename
    def setPreReq(self,prereq):
        self.prereq=prereq
    def setRetire(self, status):
        self.retireStatus=status    

    def displayCourseId(self):
        return self.courseId

    def displayCourseName(self):
        return self.courseName

    def getPrerequisite(self):
        return self.prereq

    def getRetireStatus(self):
        return self.retireStatus

# Cheng Hong
class Employee(db.Model):
    __tablename__ = 'Employee'

    employeeId = db.Column(String(8), primary_key=True)
    email = db.Column(String(144))
    contactNo = db.Column(Integer)

    def setEID(self, id):
        self.employeeId = id
    
    def getEID(self):
        return self.employeeId

    def setEmail(self, email):
        self.email = email

    def getEmail(self):
        return self.email

    def setContact(self, no):
        self.contactNo = no

    def getContact(self):
        return self.contactNo



    def json(self):
        return {
            "employeeId": self.employeeId,
            "email": self.email,
            "contactNo": self.contactNo
        }


# Cheng Hong
class HumanResource(Employee):
    __tablename__ = 'HumanResource'

    HRId = db.Column(ForeignKey('Employee.employeeId', ondelete='CASCADE'), primary_key=True)
    HRName = db.Column(String(144), nullable=False)

    def getHrId(self):
        return self.HRId

    def getHrName(self):
        return self.HRName

    def setHrName(self, name):
        self.HRName = name

# Junjie
class Learner(Employee):
    __tablename__ = 'Learner'

    learnerId = db.Column(ForeignKey('Employee.employeeId', ondelete='CASCADE'), primary_key=True)
    learnerName = db.Column(String(144), nullable=False)
    coursesTaken = db.Column(ARRAY(String(length=144)))
    enrolledCourses = db.Column(ARRAY(String()))
    coursesApplied = db.Column(ARRAY(String()))

    def getLearnerName(self):
        return self.learnerName

    def getLearnerId(self):
        return self.learnerId

    def getLearnerName(self):
        return self.learnerName

    def getCoursesTaken(self):
        return self.coursesTaken

    def getEnrolledCourses(self):
        return self.enrolledCourses

    def getCoursesApplied(self):
        return self.coursesApplied

    def setLearnerID(self, id):
        self.learnerId = id

    def setCoursesTaken(self, coursesTaken):
        self.coursesTaken = coursesTaken

    def setLearnerName(self, name):
        self.learnerName = name

    def setEnrolledCourses(self, enrolledCourses):
        self.enrolledCourses = enrolledCourses

    def setCoursesApplied(self, coursesApplied):
        self.coursesApplied = coursesApplied

# Qi Long
class Trainer(db.Model):
    __tablename__ = 'Trainer'

    trainerId = db.Column(String(8), primary_key=True)
    trainerName = db.Column(String(144), nullable=False)
    coursesAssigned = db.Column(ARRAY(String(length=8)))

    def getTrainerId(self):
        return self.trainerId

    def getTrainerName(self):
        return self.trainerName

    def getCoursesAssigned(self):
        return self.coursesAssigned

    def setTrainerID(self, id):
        self.trainerId = id

    def setTrainerName(self, name):
        self.trainerName = name
    
    def setCoursesAssigned(self, courses):
        self.coursesAssigned = courses


class Class(db.Model):
    __tablename__ = 'Class'

    classId = db.Column(String(8), primary_key=True)
    className = db.Column(String(144), nullable=False)
    noStudents = db.Column(INT4RANGE)
    courseId = db.Column(ForeignKey('Course.courseId', ondelete='CASCADE'))
    trainerId = db.Column(ForeignKey('Trainer.trainerId', ondelete='CASCADE'), nullable=False)
    startDate = db.Column(Date, nullable=False)
    endDate = db.Column(Date, nullable=False)
    startTime = db.Column(TIME(True, 6), nullable=False)
    endTime = db.Column(TIME(True, 6), nullable=False)
    numAvailableSeats = db.Column(Integer, nullable=False)
    enrolmentStart = db.Column(DateTime(True))
    enrolmentEnd = db.Column(DateTime(True))
    lessonIdList = db.Column(ARRAY(String()))

    Course = relationship('Course')
    Trainer = relationship('Trainer')

    def __init__(self,classId,className,noStudents,courseId,trainerId,startDate,endDate,startTime,endTime,numAvailableSeats,enrolmentStart,enrolmentEnd,lessonIdList):
        self.classId = classId
        self.className = className
        self.noStudents = noStudents
        self.courseId = courseId
        self.trainerId = trainerId
        self.startDate = startDate
        self.endDate = endDate
        self.startTime = startTime
        self.endTime = endTime
        self.numAvailableSeats = numAvailableSeats
        self.enrolmentStart = enrolmentStart
        self.enrolmentEnd = enrolmentEnd
        self.lessonIdList = lessonIdList

    def getCourseId(self):
        return self.courseId
    
    def getStartendDate(self):
        return self.startDate, self.endDate


class Forum(db.Model):
    __tablename__ = 'Forum'

    threadId = db.Column(String(8), primary_key=True)
    employeeId = db.Column(ForeignKey('Employee.employeeId', ondelete='CASCADE'), nullable=False)

    Employee = relationship('Employee')

# Keith
class Enrolment(db.Model):
    __tablename__ = 'Enrolment'

    enrolmentId = db.Column(String(8), primary_key=True, server_default=FetchedValue())
    courseId = db.Column(ForeignKey('Course.courseId', ondelete='CASCADE'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId', ondelete='CASCADE'), nullable=False)
    approvalStatus = db.Column(String(144), nullable=False)
    completionStatus = db.Column(String(144), nullable=False)
    numLessonCompleted = db.Column(Integer)
    classId = db.Column(String(8), nullable=False)

    # Class = relationship('Class')
    Course = relationship('Course')
    Learner = relationship('Learner')

    def __init__(self, courseId, learnerId, approvalStatus, completionStatus, numLessonCompleted, classId):
        self.courseId = courseId
        self.learnerId = learnerId
        self.approvalStatus = approvalStatus
        self.completionStatus = completionStatus
        self.numLessonCompleted = numLessonCompleted
        self.classId = classId

    def getCourseId(self):
        return self.courseId

    def getLearnerId(self):
        return self.learnerId

    def getApprovalStatus(self):
        return self.approvalStatus

    def getCompletionStatus(self):
        return self.completionStatus

    def getNumLessonCompleted(self):
        return self.numLessonCompleted

    def getClassId(self):
        return self.classId

    def getCompletedCourses(self, learnerId):
        enrolment_records = Enrolment.query.filter_by(learnerId=learnerId)
        completed_courses = []
        for record in enrolment_records:
            if record.completionStatus == "completed":
                completed_courses.append(record.courseId)
        return completed_courses

    def getClassStartEndDate(self, classId):
        classTimings = Class.query.filter_by(classId=classId)
        return classTimings[0].getStartendDate()

# Keith
class Lesson(db.Model):
    __tablename__ = 'Lesson'

    lessonId = db.Column(String(144), primary_key=True)
    lessonNo = db.Column(Integer, nullable=False)
    lessonTitle = db.Column(String(144), nullable=False)
    courseId = db.Column(ForeignKey('Course.courseId', ondelete='CASCADE'), nullable=False)
    prereqLessonId = db.Column(ForeignKey('Lesson.lessonId', ondelete='CASCADE'))
    materialIdList = db.Column(ARRAY(String(144)))
    quizId = db.Column(ForeignKey('Quiz.quizId', ondelete='CASCADE'), nullable=False)

    Course = relationship('Course')
    parent = relationship('Lesson')
    Quiz = relationship('Quiz')

    def __init__(self, lessonId, lessonNo, lessonTitle, courseId, prereqLessonId, materialIdList, quizId):
        self.lessonId = lessonId
        self.lessonNo = lessonNo
        self.lessonTitle = lessonTitle
        self.courseId = courseId
        self.prereqLessonId = prereqLessonId
        self.materialIdList = materialIdList
        self.quizId = quizId

    def getLessonId(self):
        return self.lessonId

    def getLessonTitle(self):
        return self.lessonTitle

    def getPrereqLessonId(self):
        return self.prereqLessonId

    def getMaterialIdList(self):
        return self.materialIdList

# Junjie
class LessonStatus(db.Model):
    __tablename__ = 'LessonStatus'

    learnerId = db.Column(String(8), primary_key=True)
    lessonId = db.Column(String(144), primary_key=True)
    completionStatus = db.Column(Boolean, nullable=False)

    def getLessonId(self):
        return self.lessonId

    def getLearnerId(self):
        return self.learnerId

    def getCompletionStatus(self):
        return self.completionStatus

    def setCompletionStatus(self, status):
        self.completionStatus = status

    def setLessonId(self, lessonCode):
        self.lessonId = lessonCode

    def setCompletionStatus(self, status):
        self.completionStatus = status

# Junyi
class Material(db.Model):
    __tablename__ = 'Material'

    materialId = db.Column(String(144), primary_key=True)
    materialName = db.Column(String(144), nullable=False)
    materialType = db.Column(String(144), nullable=False)
    fileLink = db.Column(String(1000), nullable=False)
    lessonId = db.Column(ForeignKey('Lesson.lessonId', ondelete='CASCADE'), nullable=False)

    Lesson = relationship('Lesson')

    def __init__(self, materialId, materialName, materialType, fileLink, lessonId):
        self.materialId = materialId
        self.materialName = materialName
        self.materialType = materialType
        self.fileLink = fileLink
        self.lessonId = lessonId

    def getMaterialId(self):
        return self.materialId

    def getMaterialName(self):
        return self.materialName

    def getMaterialType(self):
        return self.materialType

    def getFileLink(self):
        return self.fileLink

    def getMaterialbyId(self, materialId):
        material_record = Material.query.filter_by(
            materialId=materialId).first()
        return material_record

class MaterialAccess(db.Model):
    __tablename__ = 'MaterialAccess'

    learnerId = db.Column(String(8), primary_key=True)
    materialId = db.Column(String(144), primary_key=True)
    accessStatus = db.Column(Boolean, nullable=False)

# Qi Long
class Quiz(db.Model):
    __tablename__ = 'Quiz'
    
    quizId = Column(String(16), primary_key=True)
    quizName = Column(String(144), nullable=False)
    graded = Column(Boolean, nullable=False)
    classId = Column(String(144), nullable=False)
    quizContent = Column(ARRAY(JSONB), nullable=True)
    

    def __init__(self, quizId, quizName, graded, classId, quizContent):
        self.quizId = quizId
        self.quizName = quizName
        self.graded = graded
        self.classId = classId
        self.quizContent = quizContent
        

    def getQuizId(self):
        return self.quizId

    def setQuizId(self, quizId):
        self.quizId = quizId

    def getQuizName(self):
        return self.quizName

    def setQuizName(self, quizName):
        self.quizName = quizName

    def getGraded(self):
        return self.graded

    def setGraded(self, graded):
        self.graded = graded
    
    def getClassId(self):
        return self.classId

    def setClassId(self, classId):
        self.classId = classId
    
    def getQuizContent(self):
        self.quizContent = json.dumps(self.quizContent)
        return self.quizContent

    def setQuizContent(self, quizContent):
        self.quizContent = quizContent

# Qi Long
class Score(db.Model):
    __tablename__ = 'Score'

    scoreId = db.Column(String(8), primary_key=True, server_default=FetchedValue())
    quizId = db.Column(ForeignKey('Quiz.quizId', ondelete='CASCADE'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId', ondelete='CASCADE'), nullable=False)
    completedStatus = Column(Boolean, nullable=False)
    scorePerc = db.Column(Integer, nullable=False)

    Learner = relationship('Learner')
    Quiz = relationship('Quiz')

    def __init__(self, quizId, learnerId, completedStatus, scorePerc):
        self.quizId = quizId
        self.learnerId = learnerId
        self.completedStatus = completedStatus
        self.scorePerc = scorePerc

    def getScoreId(self):
        return self.scoreId

    def getQuizId(self):
        return self.quizId

    def getLearnerId(self):
        return self.learnerId

    def getCompletedStatus(self):
        return self.completedStatus

    def getScorePerc(self):
        return self.scorePerc

    def setScoreId(self, scoreId):
        self.scoreId = scoreId

    def setQuizId(self, quizId):
        self.quizId = quizId

    def setLearnerId(self, learnerId):
        self.learnerId = learnerId

    def setCompletedStatus(self, completedStatus):
        self.completedStatus = completedStatus

    def setScorePerc(self, scorePerc):
        self.scorePerc = scorePerc
