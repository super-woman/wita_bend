"""Fixtures for users"""
import pytest

from ..factories import SampleFactory


@pytest.fixture
def sample(db):
    sample = SampleFactory()
    db.session.commit()
    return sample
