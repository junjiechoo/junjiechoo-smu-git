import pytest
from app.models.database import *

def test_hr():
    
    hr = HumanResource()
    hr.setHrName("ahhock")
    assert hr.getHrName() == "ahhock"
    
