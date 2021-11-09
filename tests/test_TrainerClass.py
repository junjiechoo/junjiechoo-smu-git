import pytest
from app.models.database import *


def test_trainer_id():
    trainer1 = Trainer()
    trainer1.setTrainerID("T0005")
    assert trainer1.getTrainerId() == "T0005"
    
def test_trainer_name():
    trainer1 = Trainer()
    trainer1.setTrainerName("Hock")
    assert trainer1.getTrainerName() == "Hock"
    
def test_trainer_coursesAssigned():
    courses = ["IS212", "IS213"]
    trainer1 = Trainer()
    trainer1.setCoursesAssigned(courses)
    assert len(courses) == len(trainer1.getCoursesAssigned())
