from __future__ import print_function
from re import template  # Use print() instead of print
from flask import url_for
from flask.signals import template_rendered
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json
import codecs


def test_course_home(client, session, captured_templates):
    response = client.get("/learner/courses", follow_redirects=True)

    template, context = captured_templates[0]

    assert template.name == "main/learner.html"

    assert "courses" in context
    assert "learner" in context
    assert "trainer" in context
    assert "enrolment" in context
    assert "enteredCourses" in context

    assert isinstance(context["courses"][0], Course)
    assert isinstance(context["learner"][0], Learner)
    assert isinstance(context["trainer"][0], Trainer)
    assert isinstance(context["enrolment"][0], Enrolment)
    assert context["enteredCourses"] == True


def test_course_application(client, session):
    userInfo = {
        "learnerId": "L003",
        "courseId": "IS112"
    }

    userInfo = json.dumps(userInfo)

    response = client.get(
        f"/learner/courses/{userInfo}",
        data=userInfo,
        headers={"Content-Type": "application/json"},
        follow_redirects=True
    )
    assert response.get_data() == b"Learner3 has applied for course IS112"


def test_uploadmaterials_page(client, session, captured_templates):
    response = client.get(
        "/courses/upload-materials",
        follow_redirects=True
    )

    template, context = captured_templates[1]

    assert template.name == 'main/upload_materials.html'
    
    assert len(list(context['courses'])) >= 1
    assert len(list(context['lessons'])) >= 1
    assert len(list(context['materials'])) >= 1