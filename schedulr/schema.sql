DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `project`;
DROP TABLE IF EXISTS `equipment`;
DROP TABLE IF EXISTS `reservation`;
DROP TABLE IF EXISTS `time_slot`;
CREATE TABLE `user` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
CREATE TABLE `project` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `title` TEXT NOT NULL,
    `description` TEXT NOT NULL,
    `user_id` INTEGER NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES user(id)
);
CREATE TABLE `equipment`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL,
    `description` TEXT NOT NULL,
);
CREATE TABLE `reservation`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `time_slot_id` INTEGER NOT NULL,
    `user_id` INTEGER NOT NULL,
    `equipment_id` INTEGER NOT NULL,
    FOREIGN KEY (`time_slot_id`) REFERENCES time_slot(id),
    FOREIGN KEY (`user_id`) REFERENCES user(id),
    FOREIGN KEY (`equipment_id`) REFERENCES equipment(id)
);
CREATE TABLE `time_slot`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME NOT NULL,
    UNIQUE (`start_time`, `end_time`)
);