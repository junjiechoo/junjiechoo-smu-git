# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for
from app.models.database import *
from app.views.main_views import *
import json



def test_page_urls(client, session):
    # Visit home page
    response = client.get(url_for('main.home_page'), follow_redirects=True)
    assert response.status_code==200

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
        data = data,
        headers={"Content-Type": "multipart/form-data"},
    )

    print(response_quiz_created.data)

    assert(response_quiz_created.data == b'quiz created')

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
