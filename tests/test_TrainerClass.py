import pytest
from app.models.database import *
from .conftest import *

# Done by Low Qi Long (01354150)
def test_set_trainer_id(trainer):
    trainer.setTrainerID("T0005")
    assert trainer.getTrainerId() == "T0005"
    
def test_set_trainer_name(trainer):
    trainer.setTrainerName("Hock")
    assert trainer.getTrainerName() == "Hock"
    
def test_set_coursesAssigned(trainer):
    courses = ["IS212", "IS213"]
    trainer.setCoursesAssigned(courses)
    assert trainer.getCoursesAssigned() == ["IS212", "IS213"]

def test_get_trainer_id(trainer):
    assert trainer.getTrainerId() == "T1"
    
def test_get_trainer_name(trainer):
    assert trainer.getTrainerName() == "Trainer 1"
    
def test_get_coursesAssigned(trainer):
    assert trainer.getCoursesAssigned() == ["IS111", "IS112"]
