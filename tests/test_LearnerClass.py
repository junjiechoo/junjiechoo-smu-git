from __future__ import print_function
from app.models.database import *
import pytest

# Done by Choo Jun Jie
def test_learner_id():
    learner1 = Learner()
    learner1.setLearnerID("L005")
    assert learner1.getLearnerId() == "L005"
    
def test_learner_name():
    learner1 = Learner()
    learner1.setLearnerName("Learner1")
    assert learner1.getLearnerName() == "Learner1"
    
def test_coursesTaken():
    coursesTaken = ["IS212", "IS213"]
    learner1 = Learner()
    learner1.setCoursesTaken(coursesTaken)
    assert len(coursesTaken) == len(learner1.getCoursesTaken())

def test_enrolledCourses():
    enrolledCourses = ["IS212", "IS213"]
    learner1 = Learner()
    learner1.setEnrolledCourses(enrolledCourses)
    assert len(enrolledCourses) == len(learner1.getEnrolledCourses())

def test_coursesApplied():
    coursesApplied = ["IS212", "IS213"]
    learner1 = Learner()
    learner1.setCoursesApplied(coursesApplied)
    assert len(coursesApplied) == len(learner1.getCoursesApplied())