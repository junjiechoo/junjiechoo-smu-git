# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import INT4RANGE, TIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db


class Course(db.Model):
    __tablename__ = 'Course'

    courseId = db.Column(String(8), primary_key=True)
    courseName = db.Column(String(144), nullable=False)
    prereq = db.Column(ARRAY(String(length=8)))
    retireStatus = db.Column(Boolean, nullable=False)

    def displayCourseId(self):
        return self.courseId

    def displayCourseName(self):
        return self.courseName

    def getPrerequisite(self):
        return self.prereq


class Employee(db.Model):
    __tablename__ = 'Employee'

    employeeId = db.Column(String(8), primary_key=True)
    email = db.Column(String(144))
    contactNo = db.Column(Integer)

    def json(self):
        return {
            "employeeId": self.employeeId,
            "email": self.email,
            "contactNo": self.contactNo
        }


class HumanResource(Employee):
    __tablename__ = 'HumanResource'

    HRId = db.Column(ForeignKey('Employee.employeeId'), primary_key=True)
    HRName = db.Column(String(144), nullable=False)

    def getHrId(self):
        return self.HRId
    
    def getHrName(self):
        return self.HRName


class Learner(Employee):
    __tablename__ = 'Learner'

    learnerId = db.Column(ForeignKey('Employee.employeeId'), primary_key=True)
    learnerName = db.Column(String(144), nullable=False)
    coursesTaken = db.Column(ARRAY(String(length=144)))
    enrolledCourses = db.Column(ARRAY(String()))
    coursesApplied = db.Column(ARRAY(String()))

    def getLearnerId(self):
        return self.learnerId
    
    def getLearnerName(self):
        return self.learnerName

    def getCoursesTaken(self):
        return self.coursesTaken


class Material(db.Model):
    __tablename__ = 'Material'

    MaterialId = db.Column(String(144), primary_key=True)
    MaterialName = db.Column(String(144), nullable=False)
    File = db.Column(LargeBinary)


class Trainer(db.Model):
    __tablename__ = 'Trainer'

    trainerId = db.Column(String(8), primary_key=True)
    trainerName = db.Column(String(144), nullable=False)
    coursesAssigned = db.Column(ARRAY(String(length=8)))

    def getTrainerId(self):
        return self.trainerId
    
    def trainerName(self):
        return self.trainerName

    def getCoursesAssigned(self):
        return self.coursesAssigned


class Class(db.Model):
    __tablename__ = 'Class'

    classId = db.Column(String(8), primary_key=True)
    className = db.Column(String(144), nullable=False)
    noStudents = db.Column(INT4RANGE)
    courseId = db.Column(ForeignKey('Course.courseId'))
    trainerId = db.Column(ForeignKey('Trainer.trainerId'), nullable=False)
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


class Forum(db.Model):
    __tablename__ = 'Forum'

    threadId = db.Column(String(8), primary_key=True)
    employeeId = db.Column(ForeignKey('Employee.employeeId'), nullable=False)

    Employee = relationship('Employee')


class Enrolment(db.Model):
    __tablename__ = 'Enrolment'

    enrolmentId = db.Column(String(8), primary_key=True)
    courseId = db.Column(ForeignKey('Course.courseId'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId'), nullable=False)
    approvalStatus = db.Column(String(144), nullable=False)
    completionStatus = db.Column(String(144), nullable=False)
    numLessonCompleted = db.Column(Integer)

    Course = relationship('Course')
    Learner = relationship('Learner')

    def getCompletedCourses(self, learnerId):
        enrolment_records = Enrolment.query.filter_by(learnerId=learnerId)
        completed_courses = []
        for record in enrolment_records:
            if record.completionStatus == "completed":
                completed_courses.append(record.courseId)
        return completed_courses
    
    def getApprovalStatus(self, enrolmentId):
        enrolment_record = Enrolment.query.filter_by(enrolmentId=enrolmentId).first()
        return enrolment_record.approvalStatus


class Lesson(db.Model):
    __tablename__ = 'Lesson'

    lessonId = db.Column(String(144), primary_key=True)
    chapterNo = db.Column(Integer, nullable=False)
    lessonTitle = db.Column(String(144), nullable=False)
    completionStatus = db.Column(Boolean, nullable=False)
    courseId = db.Column(ForeignKey('Course.courseId'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId'), nullable=False)
    prereqLessonId = db.Column(ForeignKey('Lesson.lessonId'))
    courseMaterialId = db.Column(ForeignKey(
        'Material.MaterialId'), nullable=False)

    Course = relationship('Course')
    Material = relationship('Material')
    Learner = relationship('Learner')
    parent = relationship('Lesson', remote_side=[lessonId])


class Quiz(db.Model):
    __tablename__ = 'Quiz'

    quizId = db.Column(String(16), primary_key=True)
    lessonId = db.Column(ForeignKey('Lesson.lessonId'), nullable=False)
    quizName = db.Column(String(144), nullable=False)
    graded = db.Column(Boolean, nullable=False)

    Lesson = relationship('Lesson')


class Score(db.Model):
    __tablename__ = 'Score'

    scoreId = db.Column(String(8), primary_key=True)
    quizId = db.Column(ForeignKey('Quiz.quizId'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId'), nullable=False)
    score = db.Column(INT4RANGE, nullable=False)

    Learner = relationship('Learner')
    Quiz = relationship('Quiz')
