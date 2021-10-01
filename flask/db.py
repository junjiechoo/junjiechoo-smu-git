# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, MetaData, String, Time
from sqlalchemy.dialects.postgresql.ranges import INT4RANGE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class Clas(Base):
    __tablename__ = 'Class'

    classId = Column(String(8), primary_key=True)
    className = Column(String(144), nullable=False)
    noStudents = Column(INT4RANGE)
    courseId = Column(ForeignKey('Course.courseId'))
    trainerId = Column(ForeignKey('Trainer.trainerId'), nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    startTime = Column(Time(True), nullable=False)
    endTime = Column(Time(True), nullable=False)
    numAvailableSeats = Column(Integer, nullable=False)
    enrolmentStart = Column(DateTime(True))
    enrolmentEnd = Column(DateTime(True))
    lessonIdList = Column(ARRAY(VARCHAR()))

    Course = relationship('Course', primaryjoin='Clas.courseId == Course.courseId', backref='class')
    Trainer = relationship('Trainer', primaryjoin='Clas.trainerId == Trainer.trainerId', backref='class')



class Course(Base):
    __tablename__ = 'Course'

    courseId = Column(String(8), primary_key=True)
    courseName = Column(String(144), nullable=False)
    prereq = Column(ARRAY(VARCHAR(length=8)))
    retireStatus = Column(Boolean, nullable=False)



class Employee(Base):
    __tablename__ = 'Employee'

    employeeId = Column(String(8), primary_key=True)
    email = Column(String(144))
    contactNo = Column(Integer)


class HumanResource(Employee):
    __tablename__ = 'HumanResource'

    HRId = Column(ForeignKey('Employee.employeeId'), primary_key=True)
    HRName = Column(String(144), nullable=False)


class Learner(Employee):
    __tablename__ = 'Learner'

    learnerId = Column(ForeignKey('Employee.employeeId'), primary_key=True)
    learnerName = Column(String(144), nullable=False)
    coursesTaken = Column(ARRAY(VARCHAR(length=144)))
    coursesApplied = Column(NullType)



class Enrolment(Base):
    __tablename__ = 'Enrolment'

    enrolmentId = Column(String(8), primary_key=True)
    courseId = Column(ForeignKey('Course.courseId'), nullable=False)
    learnerId = Column(ForeignKey('Learner.learnerId'), nullable=False)
    approvalStatus = Column(String(144), nullable=False)
    completionStatus = Column(String(144), nullable=False)
    numLessonCompleted = Column(Integer)

    Course = relationship('Course', primaryjoin='Enrolment.courseId == Course.courseId', backref='enrolments')
    Learner = relationship('Learner', primaryjoin='Enrolment.learnerId == Learner.learnerId', backref='enrolments')



class Forum(Base):
    __tablename__ = 'Forum'

    threadId = Column(String(8), primary_key=True)
    employeeId = Column(ForeignKey('Employee.employeeId'), nullable=False)

    Employee = relationship('Employee', primaryjoin='Forum.employeeId == Employee.employeeId', backref='forums')



class Lesson(Base):
    __tablename__ = 'Lesson'

    lessonId = Column(String(144), primary_key=True)
    chapterNo = Column(Integer, nullable=False)
    lessonTitle = Column(String(144), nullable=False)
    completionStatus = Column(Boolean, nullable=False)
    courseId = Column(ForeignKey('Course.courseId'), nullable=False)
    learnerId = Column(ForeignKey('Learner.learnerId'), nullable=False)
    prereqLessonId = Column(ForeignKey('Lesson.lessonId'))
    courseMaterialId = Column(ForeignKey('Material.MaterialId'), nullable=False)

    Course = relationship('Course', primaryjoin='Lesson.courseId == Course.courseId', backref='lessons')
    Material = relationship('Material', primaryjoin='Lesson.courseMaterialId == Material.MaterialId', backref='lessons')
    Learner = relationship('Learner', primaryjoin='Lesson.learnerId == Learner.learnerId', backref='lessons')
    parent = relationship('Lesson', remote_side=[lessonId], primaryjoin='Lesson.prereqLessonId == Lesson.lessonId', backref='lessons')



class Material(Base):
    __tablename__ = 'Material'

    MaterialId = Column(String(144), primary_key=True)
    MaterialName = Column(String(144), nullable=False)
    File = Column(LargeBinary)



class Quiz(Base):
    __tablename__ = 'Quiz'

    quizId = Column(String(16), primary_key=True)
    lessonId = Column(ForeignKey('Lesson.lessonId'), nullable=False)
    quizName = Column(String(144), nullable=False)
    graded = Column(Boolean, nullable=False)

    Lesson = relationship('Lesson', primaryjoin='Quiz.lessonId == Lesson.lessonId', backref='quizzes')



class Score(Base):
    __tablename__ = 'Score'

    scoreId = Column(String(8), primary_key=True)
    quizId = Column(ForeignKey('Quiz.quizId'), nullable=False)
    learnerId = Column(ForeignKey('Learner.learnerId'), nullable=False)
    score = Column(INT4RANGE, nullable=False)

    Learner = relationship('Learner', primaryjoin='Score.learnerId == Learner.learnerId', backref='scores')
    Quiz = relationship('Quiz', primaryjoin='Score.quizId == Quiz.quizId', backref='scores')



class Trainer(Base):
    __tablename__ = 'Trainer'

    trainerId = Column(String(8), primary_key=True)
    trainerName = Column(String(144), nullable=False)
    coursesAssigned = Column(ARRAY(VARCHAR(length=8)))
