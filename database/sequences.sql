SELECT setval(pg_get_serial_sequence('lecturers','id'), (SELECT COALESCE(max(id),1) FROM lecturers));
SELECT setval(pg_get_serial_sequence('subjects','id'), (SELECT COALESCE(max(id),1) FROM subjects));
SELECT setval(pg_get_serial_sequence('active_subjects','id'), (SELECT COALESCE(max(id),1) FROM active_subjects));
