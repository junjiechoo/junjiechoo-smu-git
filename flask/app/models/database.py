# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, MetaData, String, Time
from sqlalchemy.dialects.postgresql.ranges import INT4RANGE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from app import db


Base = declarative_base()
metadata = Base.metadata


class Class(db.Model):
    __tablename__ = 'Class'

    classId = db.Column(String(8), primary_key=True)
    className = db.Column(String(144), nullable=False)
    noStudents = db.Column(INT4RANGE)
    courseId = db.Column(ForeignKey('Course.courseId'))
    trainerId = db.Column(ForeignKey('Trainer.trainerId'), nullable=False)
    startDate = db.Column(Date, nullable=False)
    endDate = db.Column(Date, nullable=False)
    startTime = db.Column(Time(True), nullable=False)
    endTime = db.Column(Time(True), nullable=False)
    numAvailableSeats = db.Column(Integer, nullable=False)
    enrolmentStart = db.Column(DateTime(True))
    enrolmentEnd = db.Column(DateTime(True))
    lessonIdList = db.Column(ARRAY(String()))

    Course = relationship(
        'Course', primaryjoin='Class.courseId == Course.courseId', backref='class')
    Trainer = relationship(
        'Trainer', primaryjoin='Class.trainerId == Trainer.trainerId', backref='class')

    def json(self):
        return {"employeeId": self.employeeId, 
        "className": self.className, 
        "noStudents": self.contactNo, 
        "contactNo": self.contactNo, 
        "contactNo": self.contactNo, 
        "contactNo": self.contactNo, 
        "contactNo": self.contactNo}


class Course(db.Model):
    __tablename__ = 'Course'

    courseId = db.Column(String(8), primary_key=True)
    courseName = db.Column(String(144), nullable=False)
    prereq = db.Column(ARRAY(String(length=8)))
    retireStatus = db.Column(Boolean, nullable=False)


class Employee(db.Model):
    __tablename__ = 'Employee'

    employeeId = db.Column(String(8), primary_key=True)
    email = db.Column(String(144))
    contactNo = db.Column(Integer)

    def json(self):
        return {"employeeId": self.employeeId, "contactNo": self.contactNo}


class HumanResource(Employee):
    __tablename__ = 'HumanResource'

    HRId = db.Column(ForeignKey('Employee.employeeId'), primary_key=True)
    HRName = db.Column(String(144), nullable=False)


class Learner(Employee):
    __tablename__ = 'Learner'

    learnerId = db.Column(ForeignKey('Employee.employeeId'), primary_key=True)
    learnerName = db.Column(String(144), nullable=False)
    coursesTaken = db.Column(ARRAY(String(length=144)))
    coursesApplied = db.Column(NullType)


class Enrolment(db.Model):
    __tablename__ = 'Enrolment'

    enrolmentId = db.Column(String(8), primary_key=True)
    courseId = db.Column(ForeignKey('Course.courseId'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId'), nullable=False)
    approvalStatus = db.Column(String(144), nullable=False)
    completionStatus = db.Column(String(144), nullable=False)
    numLessonCompleted = db.Column(Integer)

    Course = relationship(
        'Course', primaryjoin='Enrolment.courseId == Course.courseId', backref='enrolments')
    Learner = relationship(
        'Learner', primaryjoin='Enrolment.learnerId == Learner.learnerId', backref='enrolments')


class Forum(db.Model):
    __tablename__ = 'Forum'

    threadId = db.Column(String(8), primary_key=True)
    employeeId = db.Column(ForeignKey('Employee.employeeId'), nullable=False)

    Employee = relationship(
        'Employee', primaryjoin='Forum.employeeId == Employee.employeeId', backref='forums')


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

    Course = relationship(
        'Course', primaryjoin='Lesson.courseId == Course.courseId', backref='lessons')
    Material = relationship(
        'Material', primaryjoin='Lesson.courseMaterialId == Material.MaterialId', backref='lessons')
    Learner = relationship(
        'Learner', primaryjoin='Lesson.learnerId == Learner.learnerId', backref='lessons')
    parent = relationship('Lesson', remote_side=[
                          lessonId], primaryjoin='Lesson.prereqLessonId == Lesson.lessonId', backref='lessons')


class Material(db.Model):
    __tablename__ = 'Material'

    MaterialId = db.Column(String(144), primary_key=True)
    MaterialName = db.Column(String(144), nullable=False)
    File = db.Column(LargeBinary)


class Quiz(db.Model):
    __tablename__ = 'Quiz'

    quizId = db.Column(String(16), primary_key=True)
    lessonId = db.Column(ForeignKey('Lesson.lessonId'), nullable=False)
    quizName = db.Column(String(144), nullable=False)
    graded = db.Column(Boolean, nullable=False)

    Lesson = relationship(
        'Lesson', primaryjoin='Quiz.lessonId == Lesson.lessonId', backref='quizzes')


class Score(db.Model):
    __tablename__ = 'Score'

    scoreId = db.Column(String(8), primary_key=True)
    quizId = db.Column(ForeignKey('Quiz.quizId'), nullable=False)
    learnerId = db.Column(ForeignKey('Learner.learnerId'), nullable=False)
    score = db.Column(INT4RANGE, nullable=False)

    Learner = relationship(
        'Learner', primaryjoin='Score.learnerId == Learner.learnerId', backref='scores')
    Quiz = relationship(
        'Quiz', primaryjoin='Score.quizId == Quiz.quizId', backref='scores')


class Trainer(db.Model):
    __tablename__ = 'Trainer'

    trainerId = db.Column(String(8), primary_key=True)
    trainerName = db.Column(String(144), nullable=False)
    coursesAssigned = db.Column(ARRAY(String(length=8)))
