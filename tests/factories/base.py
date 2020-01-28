# -*- coding: utf-8 -*-
"""Factories to help in tests."""
import factory
from factory.alchemy import SQLAlchemyModelFactory

from apps.database import db


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
