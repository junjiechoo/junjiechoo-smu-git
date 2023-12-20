from __future__ import print_function
from re import template  # Use print() instead of print
from flask import url_for
from flask.signals import template_rendered
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json
import codecs


def test_lesson_page(client, session, captured_templates):
    response = client.get(
        "/learner/courses/lesson",
        follow_redirects=True
    )

    template, context = captured_templates[0]
    
    assert template.name == 'main/lesson.html'
    assert context['learnerId'] == "L003"
    assert 'course' is not None
    assert context['enteredCourses'] == True
    assert context['courseId'] == "IS111"
    assert 'lesson_content' in context