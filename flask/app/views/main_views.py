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
from app.models.database import *

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone


@main_blueprint.route('/')
def home_page():
    employeeList = Learner.query.all()
    return render_template('main/home_page.html', content=employeeList)


@main_blueprint.route('/learner')
def learner_page():
    #hello-wor
    learner = Learner.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', learner=learner)


@main_blueprint.route('/learner/enrolment')
def enrolment_page():
    enrolments = db.session.query(Enrolment, Course).join(
        Course, Course.courseId == Enrolment.courseId).filter(Enrolment.learnerId == 'L003')
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

@main_blueprint.route('/trainer')
def trainer_page():
    trainer = Trainer.query.filter_by(trainerId = 'T001')
    return render_template('main/admin_page.html', trainer=trainer)

@main_blueprint.route('/trainer/quizzes')
def quiz_page():
    lessonsWithoutQuiz = {}
    assignedClasses = Class.query.filter_by(trainerId = 'T001')
    for classId in assignedClasses:
        if classId.lessonIdList != None:
            for lessonIdQuery in classId.lessonIdList:
                lessonIdQuery = lessonIdQuery[1:-1]
                lessonDetails = Lesson.query.filter_by(lessonId = lessonIdQuery)
                for lesson in lessonDetails:
                    if lesson.quizId != None:
                        lessonsWithoutQuiz[lesson.lessonId] = classId.classId
    return render_template('main/admin_page.html', assignedClasses=assignedClasses, lessonsWithoutQuiz=lessonsWithoutQuiz, enteredCreateQuiz = True)

# @main_blueprint.route('/trainer/quizzes/<string:quizInfo>', methods=['GET', 'POST'])
# def create_quiz(quizInfo):
#     print("------------------------------")
#     # for key, value in request.form.items():
#     #     print("key:", key, " value:", value)
#     # print(request.form)
#     newQuizId = ""
#     newQuizName = ""
#     quizContent = []
#     for qnNum in range(1, int(request.form['totalNumQuestions'])+1):
#         formattedQnContent = {}

#         formattedQnContent['qnNum'] = f"qn{qnNum}"
#         formattedQnContent['question'] = request.form[f"qn{qnNum}"]

#         if request.form[f"ansType{qnNum}"] == "trueFalse":
#             formattedQnContent['answerType'] = "trueFalse"
#             formattedQnContent['answer'] = request.form[f'tfAns{qnNum}']
#         else:
#             formattedQnContent['answerType'] = "mcq"
#             options = []
#             for optionNum in range(1,5):
#                 options.append(request.form[f'qn{qnNum}_option{optionNum}'])
#             formattedQnContent['answer'] = options
        
#         quizContent.append(formattedQnContent)
    
#     print(quizContent)

#     if request.form['graded'] == 'true':
#         graded = True
#     else:
#         graded = False

#     last_quizId = Quiz.query.order_by(Quiz.quizId.desc()).first()
#     if last_quizId == None:
#         last_quizId = 'Q001'
#     else:
#         last_quizId = last_quizId.quizId
#         quizId_alphabet = last_quizId[0]
#         quiz_number = int(last_quizId[1:])
#         quiz_number += 1
#         newQuizId = quizId_alphabet + str(quiz_number)
#         newQuizName = "Quiz " + str(quiz_number)

#     classId = request.form['classDetails']

#     # quizContent = json.dumps(quizContent)
#     print(quizContent)

#     newQuiz = Quiz(newQuizId, newQuizName, graded, classId, quizContent)
#     db.session.add(newQuiz)
#     db.session.commit()
   
#     print("------------------------------")
#     return "quiz created"

@main_blueprint.route('/learner/courses/lesson')
def lesson_page():
    courseId = "IS111"
    learnerId = "L003"
    course = Course.query.filter_by(courseId=courseId)
    lesson_content = []
    lessons = Lesson.query.filter_by(
        courseId=courseId).order_by(Lesson.lessonNo)
    for lesson in lessons:
        quiz = Quiz.query.filter_by(quizId=lesson.quizId).first()
        score = Score.query.filter_by(
            quizId=quiz.quizId, learnerId=learnerId).first()
        material = Material.query.filter_by(lessonId=lesson.lessonId).all()
        content = {
            "lesson": lesson,
            "material": material,
            "quiz": quiz,
            "score": score if score else None,
        }
        lesson_content.append(content)
    return render_template('main/lesson.html', learnerId=learnerId, course=course, enteredCourses=True, courseId=courseId, lesson_content=lesson_content)


@main_blueprint.route('/learner/courses/lesson/score', methods=['POST'])
def create_score():
    data = request.get_json()
    quizId = data['quizId']
    learnerId = data['learnerId']
    completedStatus = data['completedStatus']
    scorePerc = data['scorePerc']
    try:
        score = Score.query.filter_by(
            quizId=quizId, learnerId=learnerId).first()
        if not score:
            score = Score(**data)
            db.session.add(score)
            db.session.commit()
        score.completedStatus = completedStatus
        score.scorePerc = scorePerc
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "message": "An error occured creating the score."
        })
    return jsonify(
        {
            "code": 201,
            "data": "Score created"
        }
    ), 201


# IGNORE ALL BELOW FIRST
# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')

@main_blueprint.route('/admin')
def admin_page():
    courses = Course.query.all()
    learner = Learner.query.all()
    trainer = Trainer.query.all()
    return render_template('main/admin_courses.html', courses=courses, learner=learner, trainer=trainer,  enteredCourses=True)

@main_blueprint.route('/admin/create', methods=['POST', 'GET'])
def admin_create():
    return render_template('main/admin_create_course.html')

@main_blueprint.route('/admin/create/course', methods=['POST', 'GET'])
def admin_create_course():
    name = request.form.get('name')
    id = request.form.get('id')
    prereq = request.form.get('prereq')
    course = Course()
    course.setCourseId(id)
    course.setCourseName(name)
    course.setPreReq(prereq)
    course.setRetire(False)

    db.session.add(course)
    db.session.commit()

    return redirect(url_for('main.admin_page'))

@main_blueprint.route('/admin/courses/<string:id>', methods=['POST', 'GET'])
def course_id(id):
    learner = request.form.get('learner')
    learner_to_update = Learner.query.filter_by(learnerId=learner).first()
    learner_to_update = Learner.query.get(learner_to_update.learnerId)

    trainer = request.form.get('trainer')
    trainer_to_update = Trainer.query.filter_by(trainerName=trainer).first()
    trainer_to_update = Trainer.query.get(trainer_to_update.trainerId)

    print(learner_to_update.enrolledCourses)
    learner_to_update.enrolledCourses.append(id)
    trainer_to_update.coursesAssigned.append(id)
    db.session.commit()

    return render_template('main/learner.html')


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


@main_blueprint.route('/trainer/quizzes/<string:quizInfo>', methods=['GET', 'POST'])
def create_quiz(quizInfo):
    print("------------------------------")
    # for key, value in request.form.items():
    #     print("key:", key, " value:", value)
    # print(request.form)

    quizContent = []
    for qnNum in range(1, int(request.form['totalNumQuestions'])+1):
        formattedQnContent = {}

        formattedQnContent['qnNum'] = f"qn{qnNum}"
        formattedQnContent['question'] = request.form[f"qn{qnNum}"]

        if request.form[f"ansType{qnNum}"] == "trueFalse":
            formattedQnContent['answerType'] = "trueFalse"
            formattedQnContent['answer'] = request.form[f'tfAns{qnNum}']
        else:
            formattedQnContent['answerType'] = "mcq"
            options = []
            for optionNum in range(1, 5):
                options.append(request.form[f'qn{qnNum}_option{optionNum}'])
            formattedQnContent['answer'] = options

        quizContent.append(formattedQnContent)

    print(quizContent)

    if request.form['graded'] == 'true':
        graded = True
    else:
        graded = False

    last_quizId = Quiz.query.order_by(Quiz.quizId.desc()).first()
    newQuizId = ""
    newQuizName = ""
    if last_quizId == None:
        last_quizId = 'Q001'
    else:
        last_quizId = last_quizId.quizId
        quizId_alphabet = last_quizId[0]
        quiz_number = int(last_quizId[1:])
        quiz_number += 1
        newQuizId = quizId_alphabet + str(quiz_number)
        newQuizName = "Quiz " + str(quiz_number)

    classId = request.form['classDetails']

    # quizContent = json.dumps(quizContent)
    print(quizContent)

    newQuiz = Quiz(newQuizId, newQuizName, graded, classId, quizContent)
    db.session.add(newQuiz)
    db.session.commit()

    print("------------------------------")
    return "quiz created"
