# -*- coding: utf-8 -*-
from ..database import db, Model, SurrogatePK


class Sample(SurrogatePK, Model):
    """Sample model"""

    __tablename__ = "sample"

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Sample({self.name})>"
