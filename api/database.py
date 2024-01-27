import random
from datetime import time, datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///instance/project.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that they will be registered properly on the metadata.
    # Otherwise you will have to import them first before calling init_db()
    import api.models
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    # Create tables based on current models
    Base.metadata.create_all(bind=engine)


def seed_db():
    # Create Users
    from api.models import User, Role, UserRole, Equipment, TimeSlots, Reservation

    # Create Roles
    roles = [
        Role(id='admin', description='Administrator'),
        Role(id='user', description='User'),
        Role(id='guest', description='Guest'),
        Role(id='student', description='Student'),
        Role(id='faculty', description='Faculty'),
        Role(id='staff', description='Staff'),
        Role(id='alumni', description='Alumni'),
        Role(id='community', description='Community'),
        Role(id='tech', description='Technician')
    ]

    users = [
        User(username='jamesrutter', email='jamesdavidrutter@gmail.com',
             fullname='James Rutter', password=generate_password_hash('password123')),
        User(username='john_doe', email='john@example.com',
             fullname='John Doe', password=generate_password_hash('password123')),
        User(username='jane_doe', email='jane@example.com',
             fullname='Jane Doe', password=generate_password_hash('password123')),
        User(username='alice_smith', email='alice@example.com',
             fullname='Alice Smith', password=generate_password_hash('password123')),
        User(username='bob_jones', email='bob@example.com',
             fullname='Bob Jones', password=generate_password_hash('password123')),
        User(username='emma_wilson', email='emma@example.com',
             fullname='Emma Wilson', password=generate_password_hash('password123')),
    ]

    # Create Equipment
    equipment_list = [
        Equipment(name='Epilog Legend 24TT',
                  description='24 x 12, Laser Cutter - 25W'),
        Equipment(name='Epilog Legend 36EXT',
                  description='36 x 24, Laser Cutter - 75W'),
        Equipment(name='Universal VLS 6.60',
                  description='32 x 18 Laser Cutter - 60W'),
        Equipment(name='Universal VLS 3.50',
                  description='32 x 18 Laser Cutter - 60W')
    ]

    # Create TimeSlots
    time_slots = []
    start_hour = 9  # 9:00 AM
    end_hour = 17   # 5:00 PM

    for hour in range(start_hour, end_hour):
        start_time = datetime.combine(
            datetime.today(), time(hour=hour, minute=0))
        end_time = datetime.combine(
            datetime.today(), time(hour=hour + 1, minute=0))

        # Format times in 12-hour format with AM/PM
        start_time_formatted = start_time.strftime('%I:%M %p')
        end_time_formatted = end_time.strftime('%I:%M %p')

        description = f'{start_time_formatted} - {end_time_formatted} Slot'
        time_slot = TimeSlots(start_time=start_time,
                              end_time=end_time, description=description)
        time_slots.append(time_slot)

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
        # reservation = Reservation(user_id=user.id, equipment_id=random.choice(
        #     equipment_list).id, time_slot_id=random.choice(time_slots).id)
        # db_session.add(reservation)

    # Create Reservations
    for _ in range(25):  # 50 reservations
        reservation = Reservation(
            user_id=random.choice(users).id,
            equipment_id=random.choice(equipment_list).id,
            time_slot_id=random.choice(time_slots).id
        )
        db_session.add(reservation)

    db_session.commit()


if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    seed_db()  # Seed the database
