# Copyright 2014 SolidBuilds.com. All rights reserved
#


import xml.dom.minidom
from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask import json
from flask_user import current_user, login_required, roles_required
from flask.json import jsonify
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import NullType

from app import db
from app.models.user_models import UserProfileForm
from app.models.database import *

from werkzeug.utils import secure_filename
import boto3
import subprocess
import os

s3 = boto3.client('s3',
                  aws_access_key_id='AKIA45COZBM2IR5UOVXO', aws_secret_access_key='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'
                  )

BUCKET_NAME = 'keithprojectbucket'

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone


@main_blueprint.route('/')
def home_page():
    employeeList = Learner.query.all()
    return render_template('main/home_page.html', content=employeeList)


@main_blueprint.route('/learner')
def learner_page():
    learner = Learner.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', learner=learner)


@main_blueprint.route('/learner/enrolment')
def enrolment_page():
    enrolments = db.session.query(Enrolment, Course).join(
        Course, Course.courseId == Enrolment.courseId).filter(Enrolment.learnerId == 'L003')
    if enrolments.count() == 0:
        enrolments = None

    learner = Learner.query.filter_by(learnerId='L003')
    print("-----")
    print(enrolments[0])
    print(learner[0])
    return render_template('main/learner.html', learner=learner, enrolments=enrolments, enteredEnrolment=True)


@main_blueprint.route('/learner/courses')
def courses_page():
    courses = Course.query.all()
    learner = Learner.query.filter_by(learnerId='L003')
    trainer = Trainer.query.all()
    enrolment = Enrolment.query.filter_by(learnerId='L003')
    return render_template('main/learner.html', courses=courses, learner=learner, trainer=trainer, enrolment=enrolment, enteredCourses=True)


@main_blueprint.route('/admin/courses/<string:id>', methods=['POST', 'GET'])
def course_id(id):
    learner = request.form.get('learner')
    learner_to_update = Learner.query.filter_by(learnerId=learner).first()
    learnerCourseRemove = learner_to_update.coursesApplied
    learnerCourseRemove.remove(id)
    learnerCourseEnrolled = learner_to_update.enrolledCourses
    learnerCourseEnrolled.append(id)
    learner_to_update.coursesApplied = learnerCourseRemove
    db.session.commit()

    learner_to_update.enrolledCourses = learnerCourseEnrolled
    db.session.commit()

    trainer = request.form.get('trainer')
    trainer_to_update = Trainer.query.filter_by(trainerId=trainer).first()
    coursesAssigned = trainer_to_update.coursesAssigned
    trainer_to_update.coursesAssigned.append(id)
    trainer_to_update.coursesAssigned = coursesAssigned
    db.session.commit()

    return redirect(url_for('main.admin_page'))


@main_blueprint.route('/learner/courses/withdraw/<string:id>', methods=['POST', 'GET'])
def coursewithdraw_id(id):
    trainer = request.form.get('trainer')
    trainer_to_update = Trainer.query.filter_by(trainerName=trainer).first()
    removeCourse = trainer_to_update.coursesAssigned
    removeCourse.remove(id)

    trainer_to_update.coursesAssigned = removeCourse
    db.session.commit()

    return render_template('main/withdrawl_page.html', trainer=trainer, courseid=id)

@main_blueprint.route('/learner/courses/<string:userInfo>', methods=['GET'])
def applicationInfo(userInfo):
    userInfo = json.loads(userInfo)
    print(
        f"Learner: {userInfo['learnerId']} is now applying for courseId: {userInfo['courseId']}")
    print('------------------')

    learner = Learner.query.filter_by(learnerId=userInfo['learnerId'])

    newEnrolment = Enrolment(
        userInfo['courseId'], userInfo['learnerId'], 'Approved', 'Approved', 0, 'C001')
    db.session.add(newEnrolment)

    db.session.commit()
    print("application successful")
    return f"{learner[0].getLearnerName()} has applied for course {userInfo['courseId']}"


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
        print(course)
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
        score.completedStatus = completedStatus
        score.scorePerc = scorePerc
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "message": "An error occured when creating the score."
        })
    return jsonify(
        {
            "code": 201,
            "data": "Score created"
        }
    ), 201

# The Admin page is accessible to users with the 'admin' role
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



@main_blueprint.route('/trainer')
def trainer_page():
    trainer = Trainer.query.filter_by(trainerId='T001')
    return render_template('main/trainer.html', trainer=trainer)


@main_blueprint.route('/trainer/quizzes')
def quiz_page():
    lessonsWithoutQuiz = {}
    assignedClasses = Class.query.filter_by(trainerId='T001')
    for classId in assignedClasses:
        if classId.lessonIdList != None:
            for lessonIdQuery in classId.lessonIdList:
                lessonIdQuery = lessonIdQuery[1:-1]
                lessonDetails = Lesson.query.filter_by(lessonId=lessonIdQuery)
                for lesson in lessonDetails:
                    if lesson.quizId != None:
                        lessonsWithoutQuiz[lesson.lessonId] = classId.classId
    return render_template('main/admin_page.html', assignedClasses=assignedClasses, lessonsWithoutQuiz=lessonsWithoutQuiz, enteredCreateQuiz=True)


@main_blueprint.route('/trainer/quizzes/<string:quizInfo>', methods=['POST'])
def create_quiz(quizInfo):
    newQuizId = ""
    newQuizName = ""
    graded = ""
    classId = ""
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

    if request.form['graded'] == 'true':
        graded = True
    else:
        graded = False

    last_quizId = Quiz.query.order_by(Quiz.quizId.desc()).first()
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

    try:
        newQuiz = Quiz(newQuizId, newQuizName, graded, classId, quizContent)
        db.session.add(newQuiz)
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "message": "An error occured when creating the quiz."
        })
    return jsonify(
        {
            "code": 201,
            "data": "Quiz created"
        }
    ), 201

    print("------------------------------")
    return "quiz created"


@main_blueprint.route('/courses/upload-materials')
def uploadmaterials_page():
    trainer = Trainer.query.filter_by(trainerId='T003').first()
    courses = Course.query.all()
    lessons = Lesson.query.order_by(Lesson.lessonId).all()
    materials = Material.query.all()
    print(trainer)
    print(materials)
    return render_template('main/upload_materials.html', trainer=trainer, courses=courses, lessons=lessons, materials=materials)


@main_blueprint.route('/courses/upload-materials/results', methods=['GET', 'POST'])
def upload_materials():
    newMaterialId = ""
    newMaterialName = ""
    newMaterialType = ""
    newFileLink = ""
    lessonId = ""

    last_materialId = Material.query.order_by(Material.materialId.desc()).first()
    list_materialId = Material.query.order_by(Material.materialId.desc()).all()

    if last_materialId == None:
        last_materialId = 'M001'
    else:
        last_materialId = last_materialId.materialId
        materialId_alphabet = last_materialId[0]
        numbers = [int(mid[1:]) for mid in list_materialId]
        material_number = max(numbers) + 1
        newMaterialId = materialId_alphabet + str(material_number)

    newMaterialName = request.form["name_input"]
    newMaterialType = request.form["type_select"]
    if newMaterialType == "document":
        file = request.files["doc_upload"]
        filename = secure_filename(file.filename)
        file.save(filename)
        s3.upload_file(filename, BUCKET_NAME, "materials/documents/"+filename)
        newFileLink = "https://"+BUCKET_NAME + \
            ".s3.amazonaws.com/materials/documents/" + \
            (file.filename).replace(" ", "_")
    elif (newMaterialType == "video"):
        file = request.files["vid_upload"]
        filename = secure_filename(file.filename)
        file.save(filename)
        s3.upload_file(filename, BUCKET_NAME, "materials/videos/"+filename)
        newFileLink = "https://"+BUCKET_NAME + \
            ".s3.amazonaws.com/materials/videos/" + \
            (file.filename).replace(" ", "_")
    else:
        newFileLink = request.form["file_text"].replace(" ", "_")

    lessonId = request.form[(request.form["course_select"]+"_lesson_select")]

    newMaterial = Material(newMaterialId, newMaterialName,
                           newMaterialType, newFileLink, lessonId)
    db.session.add(newMaterial)
    db.session.commit()

    newMaterialIdList = []
    lesson = Lesson.query.filter_by(lessonId=lessonId).first()
    for materialId in lesson.getMaterialIdList():
        newMaterialIdList.append(materialId)
    newMaterialIdList.append(newMaterialId)
    lesson.materialIdList = newMaterialIdList
    db.session.commit()

    return render_template('main/upload_materials_results.html', message="material uploaded successfully")
