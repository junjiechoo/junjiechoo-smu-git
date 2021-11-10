from __future__ import print_function
from datetime import date
from app.models.database import *
import pytest

def test_Class(class_table):
    assert class_table.getCourseId() == "IS111"
    assert class_table.getStartendDate() == (date(2021,4,1), date(2021,4,10))