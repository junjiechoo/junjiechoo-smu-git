import pytest
from app.models.database import *

## Done by: Ong Cheng Hong (01349553)


def test_employee():
    employee = Employee("L088", "ahhock@smu.edu.sg", 92384912)
    assert employee.email == "ahhock@smu.edu.sg"
    assert employee.employeeId == "L088"
    assert employee.contactNo == 92384912

