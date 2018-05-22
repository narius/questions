CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


--- A table to keep track of questions
CREATE TABLE question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL
)


--- A table to keep track of every time a question is asked
CREATE TABLE vote (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    question_id INTEGER NOT NULL
    FOREIGN KEY (question_id) REFERENCES question (id)
)