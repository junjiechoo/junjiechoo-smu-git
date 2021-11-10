# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function
from re import template  # Use print() instead of print
from flask import url_for
from flask.signals import template_rendered
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json
import codecs

def test_home_page(client, session):
    # Visit home page
    response = client.get(url_for('main.home_page'), follow_redirects=True)
    assert response.status_code == 200


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

def test_quiz_home(client, session, captured_templates):
    response = client.get("/trainer/quizzes", follow_redirects=True)

    template, context = captured_templates[1]

    assert template.name == "main/admin_page.html"

    assert "assignedClasses" in context
    assert "lessonsWithoutQuiz" in context
    assert "enteredCreateQuiz" in context

    assert isinstance(context["assignedClasses"][0], Class)
    assert list(context["lessonsWithoutQuiz"].keys())[0] == "LS001"
    assert list(context["lessonsWithoutQuiz"].values())[0] == "C001"
    assert context["enteredCreateQuiz"] == True

def test_quiz_submission(client, session):

    data = {
        "csrf_token": "IjJiZjNkZWEwYjQ4MGM0ODA3NjliNWE4MjhhMzBlOTM5ZjQyMDczNTci.YXQeJg.k9HPT8_Sm2Lghf23UMJT-xB6pm8",
        "totalNumQuestions": 2,
        "classDetails": "C001",
        "qn1": "qn1",
        "ansType1": "trueFalse",
        "tfAns1": "true",
        "graded": False,
        "qn2": "qn2",
        "ansType2": "mcq",
        "qn2_option1": "option1",
        "qn2_option2": "option2",
        "qn2_option3": "option3",
        "qn2_option4": "option4",
        "submit": "Submit"
    }

    response_quiz_created = client.post(
        "/trainer/quizzes/IS114-C001-LS005",
        data=data,
        headers={"Content-Type": "multipart/form-data"},
    )

    assert(b'Quiz created' in response_quiz_created.data)
    assert b'201' in response_quiz_created.data

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

def test_lesson_page(client, session, captured_templates):
    response = client.get(
        "/learner/courses/lesson",
        follow_redirects=True
    )

    template, context = captured_templates[2]
    
    assert template.name == 'main/lesson.html'
    assert context['learnerId'] == "L003"
    assert 'course' is not None
    assert context['enteredCourses'] == True
    assert context['courseId'] == "IS111"
    assert 'lesson_content' in context

def test_uploadmaterials_page(client, session, captured_templates):
    response = client.get(
        "/courses/upload-materials",
        follow_redirects=True
    )

    template, context = captured_templates[3]

    assert template.name == 'main/upload_materials.html'
    
    assert len(list(context['courses'])) >= 1
    assert len(list(context['lessons'])) >= 1
    assert len(list(context['materials'])) >= 1

def test_enrolment_page(client,session, captured_templates):
    response = client.get(
        "/learner/enrolment",
        follow_redirects=True
    )

    template, context = captured_templates[4]

    assert template.name == 'main/learner.html'
    assert context['enrolments'][0][1].displayCourseId() == "IS111"