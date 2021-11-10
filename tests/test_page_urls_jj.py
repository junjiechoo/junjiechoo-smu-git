from __future__ import print_function
import pytest
from re import template  # Use print() instead of print
from flask import url_for
from flask.signals import template_rendered
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json
import codecs

	
# def test_trainer_course(client, session, captured_templates):

#     userInfo = {
#         "trainerId": "T004",
#         "trainerName": "Locky",
#         "coursesAssigned": "{IS112}"
#     }

#     userInfo = json.dumps(userInfo)

#     response = client.post(
#         "/trainer",
#         data=userInfo,
#         headers={"Content-Type": "application/json"},
#         follow_redirects=True
#     )

#     assert(b'Quiz created' in response.data)
#     assert response.json['code'] == 201

    
