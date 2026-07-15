CREATE TABLE lecturers(
    id serial PRIMARY KEY,
    name varchar,
    surname varchar 
);

CREATE TABLE subjects(
    id serial PRIMARY KEY,
    name varchar,
    lecturer int REFERENCES lecturers(id) on delete CASCADE   
);

CREATE TABLE opinions(
    id serial PRIMARY KEY,
    subject int REFERENCES subjects(id) on delete CASCADE,
    content varchar
);

COPY lecturers (id, name, surname) FROM stdin WITH DELIMITER ' ';
1 Piotr Micek
2 Iwona Cieślik
\.

COPY subjects (id, name, lecturer) FROM stdin WITH DELIMITER ' ';
1 Dyskretna 1
2 Propabil 1
3 Podstawy\ Programowania 2
\.


COPY opinions (id, subject, content) FROM stdin WITH DELIMITER ';';
1;1;Najlepszy Przedmiot na Świecie i TCS-esie. Polecam Każdemu.
2;3;Nic nowego dla mnie, ale ważny dla ludzi bez doświadczenia z programowaniem.
3;1;Cieżko zdać, trzeba poświęcić bardzo dużo czasu na naukę
4;2;Wypowiem się jak go w końcy zdam xd. Miałem trochę skill issue w tym roku.
\.


SELECT * FROM lecturers;
