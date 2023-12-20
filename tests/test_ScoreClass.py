from sqlalchemy.sql.expression import null
import pytest
from app.models.database import *
from .conftest import *

# Done by Low Qi Long (01354150)
def test_get_scoreId(score):
    score.setScoreId("S1")
    assert score.getScoreId() == "S1"
    
def test_get_quizId(score):
    assert score.getQuizId() == "Q1"

def test_get_learnerId(score):
    assert score.getLearnerId() == "L003"

def test_get_completedStatus(score):
    assert score.getCompletedStatus() == True

def test_get_scorePerc(score):
    assert score.getScorePerc() == 100
    
def test_set_scoreId(score):
    score.setScoreId("S2")
    assert score.getScoreId() == "S2"

def test_set_quizId(score):
    score.setQuizId("Q2")
    assert score.getQuizId() == "Q2"

def test_set_learnerId(score):
    score.setLearnerId("L003")
    assert score.getLearnerId() == "L003"

def test_set_completedStatus(score):
    score.setCompletedStatus(False)
    assert score.getCompletedStatus() == False

def test_set_scorePerc(score):
    score.setScorePerc(100)
    assert score.getScorePerc() == 100