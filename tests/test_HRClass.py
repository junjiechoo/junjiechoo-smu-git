import pytest
from app.models.database import *

# Done by Ong Cheng Hong (01349553)
def test_hr():
    
    hr = HumanResource()
    hr.setHrName("ahhock")
    assert hr.getHrName() == "ahhock"
    
