# This file contains pytest 'fixtures'.
# If a test functions specifies the name of a fixture function as a parameter,
# the fixture function is called and its result is passed to the test function.
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from datetime import date, datetime, time
from app.commands.init_db import init_db
import pytest
from app import create_app, db as the_db
from app.models.database import *
from flask import template_rendered


# Initialize the Flask-App with test-specific settings
the_app = create_app(dict(
    TESTING=True,  # Propagate exceptions
    LOGIN_DISABLED=False,  # Enable @register_required
    MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
    SERVER_NAME='localhost.localdomain',  # Enable url_for() without request context
    # Testing Postgresql database
    SQLALCHEMY_DATABASE_URI='postgresql://spm_pytest_db:ilovespm@spm-pytest-database.cjoz1mqq6cvp.us-east-1.rds.amazonaws.com:5432/spm',
    WTF_CSRF_ENABLED=False,  # Disable CSRF form validation
))

# Setup an application context (since the tests run outside of the webserver context)
the_app.app_context().push()

# Create and populate roles and users tables
# init_db()

@pytest.fixture(scope='session')
def app():
    """ Makes the 'app' parameter available to test functions. """
    return the_app


@pytest.fixture(scope='session')
def db():
    """ Makes the 'db' parameter available to test functions. """
    return the_db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)

    try: 
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def enrolment():
    return Enrolment("IS111","L001","Approved","completed",1,"C001")

@pytest.fixture
def lesson():
    return Lesson("LS001", 1, "Lesson1", "C001", "", ["M001"],  "Q001")

@pytest.fixture
def class_table():
    return Class("C001", "IS111 C001", 45, "IS111", "T001", date(2021,4,1), date(2021,4,10),time(1,0), time(12,0), 10, datetime(2021,1,1,1,0), datetime(2021,1,1,12,0), ["1"])

@pytest.fixture
def quiz():
    return Quiz("Q1", "Quiz 1", True, "C001", [{"test":"test"}])


@pytest.fixture
def score():
    return Score("Q1", "L003", True, 100)
