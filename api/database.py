from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random


engine = create_engine('sqlite:///instance/project.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import api.models
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Create tables based on current models


def seed_db():
    # Create Users
    from api.models import User, Role, UserRole, Equipment, TimeSlots, Reservation
    users = [
        User(username='john_doe', email='john@example.com', fullname='John Doe', password=generate_password_hash('password123')),
        User(username='jane_doe', email='jane@example.com', fullname='Jane Doe', password=generate_password_hash('password123'))
    ]

    # Create Roles
    roles = [
        Role(name='admin', description='Administrator role'),
        Role(name='user', description='User role')
    ]

    # Create Equipment
    equipment_list = [
        Equipment(name='Camera', description='Digital Camera'),
        Equipment(name='Microscope', description='Laboratory Microscope')
    ]

    # Create TimeSlots
    now = datetime.now()
    time_slots = [
        TimeSlots(start_time=now, end_time=now + timedelta(hours=1), description='Morning Slot'),
        TimeSlots(start_time=now + timedelta(hours=1), end_time=now + timedelta(hours=2), description='Afternoon Slot')
    ]

    # Add to session
    db_session.add_all(users)
    db_session.add_all(roles)
    db_session.add_all(equipment_list)
    db_session.add_all(time_slots)
    db_session.commit()

    # Create UserRoles and Reservations
    for user in users:
        user_role = UserRole(user_id=user.id, role_id=random.choice(roles).id)
        db_session.add(user_role)

        reservation = Reservation(user_id=user.id, equipment_id=random.choice(equipment_list).id, time_slot_id=random.choice(time_slots).id)
        db_session.add(reservation)

    db_session.commit()

if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    seed_db()  # Seed the database
