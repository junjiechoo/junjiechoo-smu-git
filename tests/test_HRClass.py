import pytest
from app.models.database import *

def test_hr():
    hr = HumanResource("H001", "hr@smu.edu.sg", 1)
    hr.setHrName("ahhock")
    assert hr.getHrName() == "ahhock"
    
