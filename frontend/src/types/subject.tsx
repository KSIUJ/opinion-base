import { Department, Time, Semester, LecturerRole} from '@/types/small';
import {ActiveSubjectFromSubject} from '@/types/active_subject';

export type SubjectBasic = {
    subject_id: number
    subject_name: string
    department: Department
    semester: Semester
    is_obligatory: boolean
    opinions_count: number
};


// Get from /subjects/all
export type SubjectsBasicResponse = {
    subjects: SubjectBasic[];
};

export type Subject = {
    subject_id: number
    subject_name: string
    department: Department
    semester: Semester
    is_obligatory: boolean
    opinions_count: number
    opinions: string[]
    lecturers_info: ActiveSubjectFromSubject
    groups_count: number
    groups: string[]
}

// Get from /subjects or /subjects/{id}
export type SubjectsResponse = {
    subjects: Subject[];
};