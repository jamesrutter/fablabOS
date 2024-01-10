-- fablabOS database design

-- TABLES -- 
-- Users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT, 
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
    date_start TEXT NOT NULL,
    date_end TEXT, 
    multi_day INTEGER NOT NULL, -- 0 = no, 1 = yes
    reoccuring INTEGER NOT NULL, -- 0 = no, 1 = yes
    reoccuring_freq TEXT, -- daily, weekly, monthly, yearly
    time_start TEXT,
    time_end TEXT,
    fee_reg INTEGER NOT NULL, -- 0 = no, 1 = yes
    fee_reg_amount INTEGER,
    fee_facilitator INTEGER,  -- 0 = no, 1 = yes
    fee_facilitator_amount INTEGER,
    max_cap INTEGER, -- 0 = no limit, 1 = limit
    max_participants INTEGER,
    min_cap INTEGER, -- 0 = no limit, 1 = limit
    min_participants INTEGER,
    target_audience TEXT, -- all, kids, adults, seniors, etc.
    tech_level TEXT, -- beginner, intermediate, advanced
    reg_url TEXT,
    image_url TEXT,
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