from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"