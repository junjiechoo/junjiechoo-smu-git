yea got# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, ForeignKey, Integer, MetaData, String, Time
from sqlalchemy.dialects.postgresql.ranges import INT4RANGE
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class Clas(Base):
    __tablename__ = 'Class'

    classId = Column(String(8), primary_key=True)
    className = Column(String(144), nullable=False)
    noStudents = Column(INT4RANGE)
    courseId = Column(ForeignKey('Course.courseId', ondelete='CASCADE'))
    trainerId = Column(ForeignKey('Trainer.trainerId', ondelete='CASCADE'), nullable=False)
    startDate = Column(Date)
    endDate = Column(Date)
    startTime = Column(Time(True))
    endTime = Column(Time(True))
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

    HRId = Column(ForeignKey('Employee.employeeId', ondelete='CASCADE'), primary_key=True)
    HRName = Column(String(144), nullable=False)


class Learner(Employee):
    __tablename__ = 'Learner'

    learnerId = Column(ForeignKey('Employee.employeeId', ondelete='CASCADE'), primary_key=True)
    learnerName = Column(String(144), nullable=False)
    coursesTaken = Column(ARRAY(VARCHAR(length=144)))
    enrolledCourses = Column(ARRAY(VARCHAR()))
    coursesApplied = Column(ARRAY(VARCHAR()))



class Enrolment(Base):
    __tablename__ = 'Enrolment'

    enrolmentId = Column(String(8), primary_key=True)
    courseId = Column(ForeignKey('Course.courseId', ondelete='CASCADE'), nullable=False)
    learnerId = Column(ForeignKey('Learner.learnerId', ondelete='CASCADE'), nullable=False)
    approvalStatus = Column(String(144), nullable=False)
    completionStatus = Column(String(144), nullable=False)
    numLessonCompleted = Column(Integer)
    classId = Column(ForeignKey('Class.classId', ondelete='CASCADE'), nullable=False)

    Clas = relationship('Clas', primaryjoin='Enrolment.classId == Clas.classId', backref='enrolments')
    Course = relationship('Course', primaryjoin='Enrolment.courseId == Course.courseId', backref='enrolments')
    Learner = relationship('Learner', primaryjoin='Enrolment.learnerId == Learner.learnerId', backref='enrolments')



class Forum(Base):
    __tablename__ = 'Forum'

    threadId = Column(String(8), primary_key=True)
    employeeId = Column(ForeignKey('Employee.employeeId', ondelete='CASCADE'), nullable=False)

    Employee = relationship('Employee', primaryjoin='Forum.employeeId == Employee.employeeId', backref='forums')



class Lesson(Base):
    __tablename__ = 'Lesson'

    lessonId = Column(String(144), primary_key=True)
    lessonNo = Column(Integer, nullable=False)
    lessonTitle = Column(String(144), nullable=False)
    prereqLessonId = Column(ForeignKey('Lesson.lessonId', ondelete='CASCADE'))
    materialIdList = Column(ARRAY(VARCHAR()))
    quizId = Column(ForeignKey('Quiz.quizId', ondelete='CASCADE'))
    courseId = Column(ForeignKey('Course.courseId', ondelete='CASCADE'), nullable=False)

    Course = relationship('Course', primaryjoin='Lesson.courseId == Course.courseId', backref='lessons')
    parent = relationship('Lesson', remote_side=[lessonId], primaryjoin='Lesson.prereqLessonId == Lesson.lessonId', backref='lessons')
    Quiz = relationship('Quiz', primaryjoin='Lesson.quizId == Quiz.quizId', backref='lessons')



class LessonStatu(Base):
    __tablename__ = 'LessonStatus'

    lessonId = Column(ForeignKey('Lesson.lessonId', ondelete='CASCADE'), primary_key=True, nullable=False)
    learnerId = Column(ForeignKey('Learner.learnerId', ondelete='CASCADE'), primary_key=True, nullable=False)
    completionStatus = Column(Boolean, nullable=False)

    Learner = relationship('Learner', primaryjoin='LessonStatu.learnerId == Learner.learnerId', backref='lesson_status')
    Lesson = relationship('Lesson', primaryjoin='LessonStatu.lessonId == Lesson.lessonId', backref='lesson_status')



class Material(Base):
    __tablename__ = 'Material'

    materialId = Column(String(144), primary_key=True)
    materialName = Column(String(144), nullable=False)
    materialType = Column(String(144), nullable=False)
    fileLink = Column(String(1000), nullable=False)
    lessonId = Column(ForeignKey('Lesson.lessonId', ondelete='CASCADE'), nullable=False)

    Lesson = relationship('Lesson', primaryjoin='Material.lessonId == Lesson.lessonId', backref='materials')



class MaterialAcces(Base):
    __tablename__ = 'MaterialAccess'

    learnerId = Column(ForeignKey('Learner.learnerId', ondelete='CASCADE'), primary_key=True, nullable=False)
    materialId = Column(ForeignKey('Material.materialId', ondelete='CASCADE'), primary_key=True, nullable=False)
    accessStatus = Column(Boolean, nullable=False)

    Learner = relationship('Learner', primaryjoin='MaterialAcces.learnerId == Learner.learnerId', backref='material_access')
    Material = relationship('Material', primaryjoin='MaterialAcces.materialId == Material.materialId', backref='material_access')



class Quiz(Base):
    __tablename__ = 'Quiz'

    quizId = Column(String(16), primary_key=True)
    quizName = Column(String(144), nullable=False)
    graded = Column(Boolean, nullable=False)
    classId = Column(ForeignKey('Class.classId', ondelete='CASCADE'), nullable=False)
    quizContent = Column(ARRAY(JSONB(astext_type=Text())))

    Clas = relationship('Clas', primaryjoin='Quiz.classId == Clas.classId', backref='quizzes')



class Score(Base):
    __tablename__ = 'Score'

    scoreId = Column(String(8), primary_key=True, server_default=FetchedValue())
    quizId = Column(ForeignKey('Quiz.quizId', ondelete='CASCADE'), nullable=False)
    learnerId = Column(ForeignKey('Learner.learnerId', ondelete='CASCADE'), nullable=False)
    completedStatus = Column(Boolean, nullable=False)
    scorePerc = Column(Integer, nullable=False)

    Learner = relationship('Learner', primaryjoin='Score.learnerId == Learner.learnerId', backref='scores')
    Quiz = relationship('Quiz', primaryjoin='Score.quizId == Quiz.quizId', backref='scores')



class Trainer(Base):
    __tablename__ = 'Trainer'

    trainerId = Column(String(8), primary_key=True)
    trainerName = Column(String(144), nullable=False)
    coursesAssigned = Column(ARRAY(VARCHAR(length=8)))
