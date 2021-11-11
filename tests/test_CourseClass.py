import pytest
from app.models.database import *

## Done by: Ong Cheng Hong (01349553)
def test_courseId():
    course1 = Course()
    course1.setCourseId("COR1306")
    assert course1.displayCourseId() == "COR1306"

def test_courseName():
    course1 = Course()
    course1.setCourseName("Capital Market")
    assert course1.displayCourseName() == "Capital Market"

def test_preReq():
    course1 = Course()
    course1.setPreReq("COR1311")
    assert course1.getPrerequisite() == "COR1311"

def test_retireStatus():
    course1 = Course()
    course1.setRetire(False)
    assert course1.getRetireStatus() == False

 