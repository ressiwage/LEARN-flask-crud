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
  `take_date` DATE NOT NULL DEFAULT CURRENT_DATE,
  `return_date` DATE,
  PRIMARY KEY (`id`));