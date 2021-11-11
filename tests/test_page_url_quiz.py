from __future__ import print_function
from re import template  # Use print() instead of print
from flask import url_for
from flask.signals import template_rendered
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json
import codecs

def test_quiz_home(client, session, captured_templates):
    response = client.get("/trainer/quizzes", follow_redirects=True)

    template, context = captured_templates[0]

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