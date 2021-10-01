import enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Database(SQLAlchemy):
    def __init__(self, app: Flask):
        super().__init__(app)
        self.__init_model()

    def __init_model(self):
        db = self

        class BlogStatus(enum.Enum):
            COMMON = 0
            TRENDING = 1

            @classmethod
            def has_value(cls, value):
                return value in cls._member_names_

        class BlogCategory(enum.Enum):
            TRAVEL = 0
            BUSINESS = 1
            TECHNOLOGY = 2

            @classmethod
            def has_value(cls, value):
                return value in cls._member_names_

        class Blog(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String, nullable=False)
            status = db.Column(db.Enum(BlogStatus), default=BlogStatus.COMMON)
            content = db.Column(db.String, nullable=False)
            category = db.Column(db.Enum(BlogCategory), nullable=False)
            author = db.Column(db.String, nullable=False)
            created_at = db.Column(db.Integer, nullable=False)
            updated_at = db.Column(db.Integer)

            __table_args__ = {"schema": "blog"}
            __tablename__ = "blog"

            def as_dict(self):
                return {
                    c.name: str(getattr(self, c.name))
                    for c in self.__table__.columns
                }

        self.BlogStatus = BlogStatus
        self.BlogCategory = BlogCategory
        self.Blog = Blog
