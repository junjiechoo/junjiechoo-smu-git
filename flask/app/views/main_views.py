# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import xml.dom.minidom
from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask import json
from flask_user import current_user, login_required, roles_required
from flask.json import jsonify
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import NullType

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
    learner = Learner.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', learner=learner)


@main_blueprint.route('/learner/enrolment')
def enrolment_page():
    # enrolments = Enrolment.query.join(Course, Enrolment.courseId==Course.courseId).filter(Enrolment.learnerId=='L003')
    enrolments = db.session.query(Enrolment, Course).join(Course, Course.courseId == Enrolment.courseId).filter(Enrolment.learnerId=='L003')
    for i in enrolments:
        print(i)
    learner = Learner.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', learner=learner, enrolments=enrolments, enteredEnrolment=True)


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
    learner_to_update.enrolledCourses.append(id)
    trainer_to_update.coursesAssigned.append(id)
    db.session.commit()
    

    return render_template('main/learner.html')

@main_blueprint.route('/learner/courses/withdraw/<string:id>', methods=['POST', 'GET'])
def coursewithdraw_id(id):
    trainer = request.form.get('trainer')
    print(trainer)
    trainer_to_update = Trainer.query.filter_by(trainerName=trainer).first()
    trainer_to_update = Trainer.query.get(trainer_to_update.trainerId)
    trainer_to_update.coursesAssigned.remove(id)
    db.session.commit()

    return render_template('main/withdrawl_page.html', trainer=trainer, courseid = id)


# to enrol into a course
# can only use GET for now cause POST causes CSRF token missing, something to do with flask-wtf
@main_blueprint.route('/learner/courses/<string:userInfo>', methods=['GET'])
def applicationInfo(userInfo):
    userInfo = json.loads(userInfo)
    print()
    print(
        f"Learner: {userInfo['learnerId']} is now applying for courseId: {userInfo['courseId']}")
    print('------------------')

    # use this two lines to add a new enrolment (have to edit to dynamically create new enrolment id, filter_by last row then +1?)
    latest_enrolment = Enrolment.query.order_by(
        Enrolment.enrolmentId.desc()).first()

    if latest_enrolment == None:
        latest_enrolment_id = 'E1'
    else:
        latest_enrolment_id = latest_enrolment.enrolmentId
        enrolment_letter = latest_enrolment_id[0]
        enrolment_number = int(latest_enrolment_id[1:])
        enrolment_number += 1
        latest_enrolment_id = enrolment_letter + str(enrolment_number)

    newEnrolment = Enrolment(
        latest_enrolment_id, userInfo['courseId'], userInfo['learnerId'], 'pending', 'pending approval', 0, 'C001')
    db.session.add(newEnrolment)

    # delete test row
    # Enrolment.query.filter_by(enrolmentId = 'E002').delete()

    # commit row insert/delete to make change visible to db
    db.session.commit()
    return('trying to do this part now')
    
@main_blueprint.route('/learner/courses/lesson')
def lesson_page():
    courseId = "IS111";
    course = Course.query.filter_by(courseId = courseId);
    learner = Learner.query.all()
    lessons = Lesson.query.filter_by(courseId = courseId).order_by(Lesson.lessonNo).all();
    material = Material.query.all();
    return render_template('main/lesson.html', course=course, learner=learner, enteredCourses=True, courseId=courseId, lessons=lessons, material=material)


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

# def layout():
#     return render_template('layout.html')
