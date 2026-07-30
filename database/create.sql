-- Departments
CREATE TABLE department (
    id serial PRIMARY KEY,
    name varchar not null
);

CREATE TABLE semester (
    id serial PRIMARY KEY,
    name varchar not null,
    is_winter boolean not null
);

CREATE TABLE lecturers_roles(
    id serial PRIMARY KEY,
    name varchar not null
);

-- Lecturers 
CREATE TABLE lecturers(
    id serial PRIMARY KEY,
    name varchar,
    surname varchar not null,
    department_id int REFERENCES department(id) on delete CASCADE 
);

-- Subjects
CREATE TABLE subjects (
    id serial PRIMARY KEY,
    name varchar not null,
    department_id int REFERENCES department(id) on delete CASCADE,
    semester_id int REFERENCES semester(id) on delete CASCADE,
    is_obligatory boolean default true
);

CREATE TABLE subject_groups(
    id serial PRIMARY KEY,
    name varchar not null
);

CREATE TABLE subject_subject_group_relation (
  id serial PRIMARY KEY,
  id_subject int REFERENCES subjects(id),
  id_subject_group int REFERENCES subject_groups(id)
);

-- Time
CREATE TABLE time (
    id serial PRIMARY KEY
);

--Active Subject
CREATE TABLE active_subjects (
  id serial PRIMARY KEY,
  lecturer_id int REFERENCES lecturers(id),
  role_id int REFERENCES lecturers_roles(id),
  subject_id int REFERENCES subjects(id),
  time_id int REFERENCES time(id)
);

--Opinions
CREATE TABLE opinions (
  id serial PRIMARY KEY,
  content varchar default '[empty opinion]'
);

CREATE TABLE subjects_opinion_relation (
    id serial PRIMARY KEY,
    subject_id int REFERENCES subjects(id),
    opinion_id int REFERENCES opinions(id),
    time_id int REFERENCES time(id)
);

CREATE TABLE lecturers_opinion_relation (
    id serial PRIMARY KEY,
    lecturer_id int REFERENCES lecturers(id),
    opinion_id int REFERENCES opinions(id),
    time_id int REFERENCES time(id)
);