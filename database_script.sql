DROP DATABASE IF EXISTS Touch_Typing_Tutor;
CREATE DATABASE Touch_Typing_Tutor;
use Touch_Typing_Tutor;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
	user_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    words_per_min DECIMAL(5,2) NOT NULL DEFAULT 0,
    tests_taken INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS characters;
CREATE TABLE characters (
	character_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    character_name varchar(1) NOT NULL
);

DROP TABLE IF EXISTS og_user_characters;
CREATE TABLE og_user_characters (
	user_characters_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    incorrect_characters INTEGER NOT NULL,
    correct_characters INTEGER NOT NULL,
    total_occurances INTEGER NOT NULL,
	character_time INTEGER NOT NULL,
	character_accuracy INTEGER NOT NULL,
    character_id int NOT NULL, 
    user_id int NOT NULL, 
	FOREIGN KEY (character_id) REFERENCES characters(character_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

DROP TABLE IF EXISTS sessionstats;
CREATE TABLE sessionstats (
	sessionID integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    WPM DECIMAL(5,2) NOT NULL DEFAULT 0,
	totalAccuracy DECIMAL(5,2) NOT NULL DEFAULT 0,
    user_id int NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

DROP TABLE IF EXISTS testsessions;
CREATE TABLE testsessions (
	user_characters_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    incorrect_characters INTEGER NOT NULL,
    correct_characters INTEGER NOT NULL,
    total_occurances INTEGER NOT NULL,
	character_time INTEGER NOT NULL,
	character_accuracy INTEGER NOT NULL,
    character_id int NOT NULL, 
    user_id int NOT NULL, 
	sessionID integer NOT NULL, 
	FOREIGN KEY (sessionID) REFERENCES sessionstats(sessionID),
	FOREIGN KEY (character_id) REFERENCES characters(character_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


INSERT INTO characters (character_name) VALUES ('a');
INSERT INTO characters (character_name) VALUES ('b');
INSERT INTO characters (character_name) VALUES ('c');
INSERT INTO characters (character_name) VALUES ('d');
INSERT INTO characters (character_name) VALUES ('e');
INSERT INTO characters (character_name) VALUES ('f');
INSERT INTO characters (character_name) VALUES ('g');
INSERT INTO characters (character_name) VALUES ('h');
INSERT INTO characters (character_name) VALUES ('i');
INSERT INTO characters (character_name) VALUES ('j');
INSERT INTO characters (character_name) VALUES ('k');
INSERT INTO characters (character_name) VALUES ('l');
INSERT INTO characters (character_name) VALUES ('m');
INSERT INTO characters (character_name) VALUES ('n');
INSERT INTO characters (character_name) VALUES ('o');
INSERT INTO characters (character_name) VALUES ('p');
INSERT INTO characters (character_name) VALUES ('q');
INSERT INTO characters (character_name) VALUES ('r');
INSERT INTO characters (character_name) VALUES ('s');
INSERT INTO characters (character_name) VALUES ('t');
INSERT INTO characters (character_name) VALUES ('u');
INSERT INTO characters (character_name) VALUES ('v');
INSERT INTO characters (character_name) VALUES ('w');
INSERT INTO characters (character_name) VALUES ('x');
INSERT INTO characters (character_name) VALUES ('y');
INSERT INTO characters (character_name) VALUES ('z');
