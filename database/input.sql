-- Departments
COPY department (id, name) FROM stdin WITH DELIMITER ';';
1;Informatyka Analityczna
2;Informatyka
\.

COPY semester (id, name, is_winter) FROM stdin WITH DELIMITER ';';
1;1;true
2;2;false
3;3;true
4;4;false
5;5;true
6;6;false
7;7;true
8;8;false
9;9;true
10;10;false
\.

COPY lecturers_roles (id, name) FROM stdin WITH DELIMITER ';';
1;Wykładowca
2;Ćwiczeniowca
\.

--Lecturers
COPY lecturers (id, name, surname, department_id) FROM stdin WITH DELIMITER ';';
1;Piotr;Micek;1
2;Iwona;Cieślik;1
\.

-- Subjects
COPY subjects (id, name, department_id, semester_id, is_obligatory) FROM stdin WITH DELIMITER ';';
1;Dyskretna;1;2;true
2;Propabil;1;3;true
3;Podstawy Programowania;1;1;false
\.

COPY subject_groups (id, name) FROM stdin WITH DELIMITER ';';
1;Micek Super Group
\.

COPY subject_subject_group_relation (id_subject, id_subject_group) FROM stdin WITH DELIMITER ';';
1;1
2;1
\.

COPY time (id) FROM stdin WITH DELIMITER ';';
1
\.

COPY active_subjects (id, lecturer_id, role_id, subject_id, time_id) FROM stdin WITH DELIMITER ';';
1;1;1;2;1
\.

--Opinions
COPY opinions (id, content) FROM stdin WITH DELIMITER ';';
1;Najlepszy Przedmiot na Świecie i TCS-esie. Polecam Każdemu.
2;Nic nowego dla mnie, ale ważny dla ludzi bez doświadczenia z programowaniem.
3;Cieżko zdać, trzeba poświęcić bardzo dużo czasu na naukę
4;Wypowiem się jak go w końcy zdam xd. Miałem trochę skill issue w tym roku.
5;Świetny prowadzący
\.

COPY subjects_opinion_relation (subject_id, opinion_id, time_id) FROM stdin WITH DELIMITER ';';
1;1;1
3;2;1
1;3;1
2;4;1
\.

COPY lecturers_opinion_relation (lecturer_id, opinion_id, time_id) FROM stdin WITH DELIMITER ';';
1;5;1
\.
