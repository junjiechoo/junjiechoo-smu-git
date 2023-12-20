from sqlalchemy.sql.expression import null
import pytest
from app.models.database import *
from .conftest import *

# Done by Low Qi Long (01354150)
def test_get_quizId(quiz):
    assert quiz.getQuizId() == "Q1"
    
def test_get_quizName(quiz):
    assert quiz.getQuizName() == "Quiz 1"

def test_get_graded(quiz):
    assert quiz.getGraded() == True

def test_get_classId(quiz):
    assert quiz.getClassId() == "C001"

def test_get_quizContent(quiz):
    assert quiz.getQuizContent() == '[{"test": "test"}]'
    
def test_set_quizId(quiz):
    quiz.setQuizId("Q2")
    assert quiz.getQuizId() == "Q2"
    
def test_set_quizName(quiz):
    quiz.setQuizName("Quiz 2")
    assert quiz.getQuizName() == "Quiz 2"

def test_set_graded(quiz):
    quiz.setGraded(False)
    assert quiz.getGraded() == False

def test_set_classId(quiz):
    quiz.setQuizId("C002")
    assert quiz.getQuizId() == "C002"

def test_set_quizContent(quiz):
    quiz.setQuizContent([{"test2": "test2"}])
    assert quiz.getQuizContent() == '[{"test2": "test2"}]'