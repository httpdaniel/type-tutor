DROP DATABASE IF EXISTS Touch_Typing_Tutor;
CREATE DATABASE Touch_Typing_Tutor;
use Touch_Typing_Tutor;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
	user_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    words_per_min DECIMAL(5,2) NOT NULL DEFAULT 0,
    words_per_min_total DECIMAL(5,2) NOT NULL DEFAULT 0,
    tests_taken INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS Characters;
CREATE TABLE Characters (
	character_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    character_name varchar(1) NOT NULL
);

DROP TABLE IF EXISTS User_Characters;
CREATE TABLE User_Characters (
	user_characters_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    incorrect_characters INTEGER NOT NULL,
    correct_characters INTEGER NOT NULL,
    total_occurances INTEGER NOT NULL,
	character_time INTEGER NOT NULL,
    character_id int NOT NULL, 
    user_id int NOT NULL, 
	FOREIGN KEY (character_id) REFERENCES Characters(character_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Characters (character_name) VALUES ('a');
INSERT INTO Characters (character_name) VALUES ('b');
INSERT INTO Characters (character_name) VALUES ('c');
INSERT INTO Characters (character_name) VALUES ('d');
INSERT INTO Characters (character_name) VALUES ('e');
INSERT INTO Characters (character_name) VALUES ('f');
INSERT INTO Characters (character_name) VALUES ('g');
INSERT INTO Characters (character_name) VALUES ('h');
INSERT INTO Characters (character_name) VALUES ('i');
INSERT INTO Characters (character_name) VALUES ('j');
INSERT INTO Characters (character_name) VALUES ('k');
INSERT INTO Characters (character_name) VALUES ('l');
INSERT INTO Characters (character_name) VALUES ('m');
INSERT INTO Characters (character_name) VALUES ('n');
INSERT INTO Characters (character_name) VALUES ('o');
INSERT INTO Characters (character_name) VALUES ('p');
INSERT INTO Characters (character_name) VALUES ('q');
INSERT INTO Characters (character_name) VALUES ('r');
INSERT INTO Characters (character_name) VALUES ('s');
INSERT INTO Characters (character_name) VALUES ('t');
INSERT INTO Characters (character_name) VALUES ('u');
INSERT INTO Characters (character_name) VALUES ('v');
INSERT INTO Characters (character_name) VALUES ('w');
INSERT INTO Characters (character_name) VALUES ('x');
INSERT INTO Characters (character_name) VALUES ('y');
INSERT INTO Characters (character_name) VALUES ('z');
