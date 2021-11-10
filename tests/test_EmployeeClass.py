import pytest
from app.models.database import *

## Done by: Ong Cheng Hong (01349553)


def test_contact():
    employee = Employee()
    employee.setContact(999)
    assert employee.getContact() == 999


def test_name():
    employee = Employee()
    employee.setEID("T999")
    assert employee.getEID() == "T999"


def test_email():
    employee = Employee()
    employee.setEmail("ch.ong@smu.edu.sg")
    assert employee.getEmail() == "ch.ong@smu.edu.sg"



