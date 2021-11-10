from __future__ import print_function
from app.models.database import *
import pytest

def test_learner_id():
    learner1 = Learner()
    learner1.setLearnerID("L005")
    assert learner1.getLearnerId() == "L005"
    
def test_lesson_id():
    lesson1 = LessonStatus()
    lesson1.setLessonId("LS001")
    assert lesson1.getLessonId() == "LS001"

def test_completion_Status():
    lesson1 = LessonStatus()
    lesson1.setCompletionStatus("LS001")
    assert lesson1.getCompletionStatus() == "LS001"

