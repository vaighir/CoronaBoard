DROP DATABASE IF EXISTS corona;

CREATE DATABASE corona;
USE corona;

CREATE TABLE user (
  id INT AUTO_INCREMENT,
  username VARCHAR(30) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(5),
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE post (
  id INT AUTO_INCREMENT,
  user_id INT,
  title VARCHAR(255),
  category VARCHAR(255),
  description TEXT,
  created DATETIME,
  edited BOOLEAN NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)
    REFERENCES user(id)
    ON DELETE CASCADE
);

CREATE TABLE comment (
  id INT AUTO_INCREMENT,
  user_id INT,
  post_id INT,
  description TEXT,
  created DATETIME,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)
    REFERENCES user(id)
    ON DELETE CASCADE,
  FOREIGN KEY (post_id)
    REFERENCES post(id)
    ON DELETE CASCADE
);

INSERT INTO user (username, email, role, password)
VALUES ("admin@admin.de", "admin@admin.de", "admin", "pbkdf2:sha256:150000$2bfdFpEs$4799a07a2145bb6edd197be29c05ca140134a10a88d33cd12199534fe874dbe1");

INSERT INTO user (username, email, role, password)
VALUES ("user@user.de", "user@user.de", "user", "pbkdf2:sha256:150000$2bfdFpEs$4799a07a2145bb6edd197be29c05ca140134a10a88d33cd12199534fe874dbe1");
