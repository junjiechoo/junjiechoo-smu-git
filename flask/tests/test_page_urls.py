# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json


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


def test_course_apply(client, session):

    userInfo = {
        "courseId": "IS113",
        "learnerId": "L003",
    }

    userInfo = json.dumps(userInfo)

    response = client.post(
        "/learner/courses",
        data=userInfo,
        headers={"Content-Type": "application/json"},
        follow_redirects=True
    )

    assert response.json['code'] == 201


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

    assert(response_quiz_created.data == b'quiz created')




# Just leave for reference for now, but must delete later
    # print(quiz1)
    # assert quiz1.quizId == "q1"

    # Login as user and visit User page
    # response = client.post(url_for('user.login'), follow_redirects=True,
    #                        data=dict(email='user@example.com', password='Password1'))
    # assert response.status_code==200
    # response = client.get(url_for('main.member_page'), follow_redirects=True)
    # assert response.status_code==200

    # # Edit User Profile page
    # response = client.get(url_for('main.user_profile_page'), follow_redirects=True)
    # assert response.status_code==200
    # response = client.post(url_for('main.user_profile_page'), follow_redirects=True,
    #                        data=dict(first_name='User', last_name='User'))
    # response = client.get(url_for('main.member_page'), follow_redirects=True)
    # assert response.status_code==200

    # # Logout
    # response = client.get(url_for('user.logout'), follow_redirects=True)
    # assert response.status_code==200

    # # Login as admin and visit Admin page
    # response = client.post(url_for('user.login'), follow_redirects=True,
    #                        data=dict(email='admin@example.com', password='Password1'))
    # assert response.status_code==200
    # response = client.get(url_for('main.admin_page'), follow_redirects=True)
    # assert response.status_code==200

    # # Logout
    # response = client.get(url_for('user.logout'), follow_redirects=True)
    # assert response.status_code==200
