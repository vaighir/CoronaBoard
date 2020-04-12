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
  created DATE,
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
  created DATE,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)
    REFERENCES user(id)
    ON DELETE CASCADE,
  FOREIGN KEY (post_id)
    REFERENCES post(id)
    ON DELETE CASCADE
);

INSERT INTO user (username, email, role, password)
VALUES ("admin", "admin@sample.com", "admin", "password");

INSERT INTO user (username, email, role, password)
VALUES ("user1", "user1@sample.com", "user", "password");
