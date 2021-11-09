from __future__ import print_function  # Use print() instead of print
from flask import url_for
from app.models.database import *
from app.views.main_views import *
import json

# def test_enrolment_page(client, session):
#     response = client.get(url_for('main.enrolment_page'), follow_redirects=True)
#     assert response.status_code == 200