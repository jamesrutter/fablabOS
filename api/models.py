from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String
from api.database import Base

# class User(db.Model):
#     __tablename__ = 'users'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(unique=True)
#     email: Mapped[str] = mapped_column(unique=True)
#     role: Mapped[str]
#     fullname: Mapped[Optional[str]]
#     password: Mapped[str]

#     def __repr__(self):
#         return '<User %r>' % self.username


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'