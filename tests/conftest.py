# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import pytest
from faker import Faker
from webtest import TestApp

from apps.app import create_app
from apps.database import db as _db

from .utils import TestClient

fake = Faker()

pytest_plugins = ["tests.fixtures.sample"]


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    ctx = _app.test_request_context()
    ctx.push()
    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    app.test_client_class = TestClient
    client = app.test_client()
    yield client
