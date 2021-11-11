from __future__ import print_function
from re import template  # Use print() instead of print
from flask import url_for
from flask.signals import template_rendered
from app.models.database import *
from app.views.main_views import *
from .conftest import captured_templates
import json
import codecs


def test_enrolment_page(client,session, captured_templates):
    response = client.get(
        "/learner/enrolment",
        follow_redirects=True
    )

    template, context = captured_templates[0]

    assert template.name == 'main/learner.html'
    assert context['enrolments'][0][1].displayCourseId() == "IS111"