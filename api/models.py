from __future__ import annotations
from typing import Optional
from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[Optional[str]]
    password: Mapped[str]
    reservations: Mapped[List["Reservation"]] = relationship("Reservation")
    user_roles: Mapped[List["UserRole"]] = relationship(
        "UserRole", back_populates="user")

    def __repr__(self):
        return '<User id=%r username=%r>' % (self.id, self.username)


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
    user_roles: Mapped[List[UserRole]] = relationship(
        "UserRole", back_populates="role")

    def __repr__(self):
        return f"<Role(name={self.name}, description={self.description})>"


class UserRole(Base):
    __tablename__ = 'user_roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id: Mapped[str] = mapped_column(ForeignKey('roles.id'))
    user: Mapped["User"] = relationship("User", back_populates="user_roles")
    role: Mapped["Role"] = relationship("Role", back_populates="user_roles")


class Equipment(Base):
    __tablename__ = 'equipment'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    reservations: Mapped[List["Reservation"]] = relationship("Reservation")


class TimeSlots(Base):
    __tablename__ = 'timeslots'
    id: Mapped[int] = mapped_column(primary_key=True)
    # Using Python datetime type in annotation
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Using Python datetime type in annotation
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column()
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="timeslot")


class Reservation(Base):
    __tablename__ = 'reservations'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    equipment_id: Mapped[int] = mapped_column(ForeignKey('equipment.id'))
    time_slot_id: Mapped[int] = mapped_column(ForeignKey('timeslots.id'))
    user: Mapped["User"] = relationship("User", back_populates="reservations")
    equipment: Mapped["Equipment"] = relationship(
        "Equipment", back_populates="reservations")
    timeslot: Mapped["TimeSlots"] = relationship(
        "TimeSlots", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation(id={self.id}, user_id={self.user_id}, " \
            f"equipment_id={self.equipment_id}, time_slot_id={self.time_slot_id})>"
