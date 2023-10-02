CREATE TABLE `library`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(250),
  PRIMARY KEY (`id`));

CREATE TABLE `library`.`books` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(250),
  `author` VARCHAR(250),
  `genre` VARCHAR(250),
  PRIMARY KEY (`id`));

CREATE TABLE `library`.`r_u_b` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `book_id` INT NOT NULL,
  `take_ts` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `return_ts` TIMESTAMP,
  PRIMARY KEY (`id`));

USE library;
INSERT INTO users (name) VALUES ('john'), ('matthew'), ('karrie');
INSERT INTO books (name, author, genre) VALUES ('antifragility', 'john doe', 'psychology'), ('python for beginners', 'conan doyle', 'technical'), ('mysql for beginners','conan doyle', 'technical');
INSERT INTO r_u_b (user_id, book_id) VALUES (1, 1), (2,2), (2,3);