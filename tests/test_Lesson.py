from __future__ import print_function
from app.models.database import *
import pytest

# Done by Keith Tan (01348868)
def test_lesson(lesson):
    assert lesson.lessonId == "LS001"
    assert lesson.lessonNo == 1
    assert lesson.lessonTitle == "Lesson1"
    assert lesson.courseId == "C001"
    assert lesson.prereqLessonId == ""
    assert lesson.materialIdList == ["M001"]
    assert lesson.quizId == "Q001"