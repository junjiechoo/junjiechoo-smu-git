from __future__ import print_function
from datetime import date
from app.models.database import *
import pytest

def test_Enrolment_class(enrolment):
    # enrolment = Enrolment("IS111","L001","Approved","completed",1,"C001")
    assert enrolment.getCourseId() == "IS111"
    assert enrolment.getLearnerId() == "L001"
    assert enrolment.getApprovalStatus() == "Approved"
    assert enrolment.getCompletionStatus() == "completed"
    assert enrolment.getNumLessonCompleted() == 1
    assert enrolment.getClassId() == "C001"

    assert enrolment.getCompletedCourses(enrolment.learnerId) == ['IS111']
    assert enrolment.getClassStartEndDate(enrolment.classId) == (date(2021,4,1), date(2021,4,10))


    
