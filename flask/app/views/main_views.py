# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import xml.dom.minidom
from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask import json
from flask_user import current_user, login_required, roles_required
from flask.json import jsonify

from app import db
from app.models.user_models import UserProfileForm
# from app.models.employee import Employee
from app.models.database import *

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    employeeList = Learner.query.all()
    return render_template('main/home_page.html', content=employeeList)


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/learner')
# @login_required  # Limits access to authenticated users
def learner_page():
    #hello-wor
    learner = Learner.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', learner=learner)

@main_blueprint.route('/learner/enrolment')
def enrolment_page():
    enrolment = Enrolment.query.all()
    learner = Learner.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', enrolment=enrolment, enteredEnrolment=True)

@main_blueprint.route('/learner/courses')
def courses_page():
    courses = Course.query.all()
    learner = Learner.query.filter_by(learnerId='L003')
    trainer = Trainer.query.all()
    enrolment = Enrolment.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', courses=courses, learner=learner, trainer=trainer, enrolment=enrolment, enteredCourses=True)

# for HR to assign trainer and learners to a course
@main_blueprint.route('/learner/courses/<string:id>', methods=['POST', 'GET'])
def course_id(id):
    learner = request.form.get('learner')
    learner_to_update = Learner.query.filter_by(learnerName=learner).first()
    learner_to_update = Learner.query.get(learner_to_update.learnerId)

    trainer = request.form.get('trainer')
    trainer_to_update = Trainer.query.filter_by(trainerName=trainer).first()
    trainer_to_update = Trainer.query.get(trainer_to_update.trainerId)

    print(learner_to_update.enrolledCourses)
    print(learner_to_update.enrolledCourses.append(id))
    # learner_to_update.enrolledCourses = data
    trainer_to_update.coursesAssigned.append(id)
    print(learner_to_update.enrolledCourses)

    db.session.commit()
    

    return render_template('main/learner.html',  learner=learner, trainer=trainer,)

# to enrol into a course
# can only use GET for now cause POST causes CSRF token missing, something to do with flask-wtf
@main_blueprint.route('/learner/courses/<string:userInfo>', methods=['GET'])
def applicationInfo(userInfo):
    # userInfo = json.loads(userInfo)
    userInfo = userInfo
    print('------------------')
    print(f"information: {userInfo}")
    return 'application received'





# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)

# @main_blueprint.route('/layout')

# def layout():asdasd
#     return render_template('layout.html')
