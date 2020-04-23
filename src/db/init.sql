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
VALUES ("admin", "admin@sample.com", "admin", "pbkdf2:sha256:150000$xTLN8CgG$10dcd8678851e272a6706f37cdcf1955c762b80f4ab480337dca2d56d1145496");

INSERT INTO user (username, email, role, password)
VALUES ("user1", "user1@sample.com", "user", "pbkdf2:sha256:150000$xTLN8CgG$10dcd8678851e272a6706f37cdcf1955c762b80f4ab480337dca2d56d1145496");
