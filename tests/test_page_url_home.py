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