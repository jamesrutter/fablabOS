-- fablabOS database design

-- TABLES -- 
PRAGMA foreign_keys = ON;
-- Users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT UNIQUE, 
    social TEXT,
    website TEXT,
    bio TEXT,
    lab_role TEXT NOT NULL -- staff, intern, guest, member, student, teacher, speaker, resident 
);

-- Equipment table
DROP TABLE IF EXISTS equipment;
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL,
    available INTEGER NOT NULL
);

-- Reservations table
DROP TABLE IF EXISTS reservations;
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);

-- Usage table
DROP TABLE IF EXISTS usage;
CREATE TABLE usage (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);

-- Events table 
DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_name TEXT NOT NULL,
    event_description TEXT,
    event_type TEXT NOT NULL, -- workshop, class, meeting, drop-in, etc.
    date_start DATE NOT NULL, -- YYYY-MM-DD
    date_end DATE, -- YYYY-MM-DD
    multi_day BOOLEAN CHECK (multi_day IN (0,1)),
    reoccuring BOOLEAN CHECK (reoccuring IN (0,1)), 
    reoccuring_freq TEXT, -- daily, weekly, monthly, yearly
    time_start TEXT, -- HH:MM AM/PM
    time_end TEXT, -- HH:MM AM/PM
    fee_reg BOOLEAN CHECK (fee_reg IN (0,1))
    fee_reg_amount REAL,
    fee_facilitator BOOLEAN CHECK (fee_facilitator IN (0,1)), 
    fee_facilitator_amount REAL,
    max_cap BOOLEAN,
    max_participants INTEGER,
    min_cap BOOLEAN CHECK (min_cap IN (0,1)), 
    min_participants INTEGER,
    target_audience TEXT, -- all, kids, adults, seniors, etc.
    tech_level TEXT, -- beginner, intermediate, advanced
    reg_url TEXT,
    image_url TEXT
); 

-- Event Facilitators junction table
DROP TABLE IF EXISTS event_facilitators;
CREATE TABLE event_facilitators (
    event_id INTEGER NOT NULL,
    facilitator_id INTEGER NOT NULL,
    PRIMARY KEY (event_id, facilitator_id),
    FOREIGN KEY (event_id) REFERENCES events (id),
    FOREIGN KEY (facilitator_id) REFERENCES users (id)
);