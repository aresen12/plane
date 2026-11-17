import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime
import hashlib


class Per(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'per'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    list_note = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    list_plans = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    id_user = sqlalchemy.Column(sqlalchemy.Integer, default=False)
