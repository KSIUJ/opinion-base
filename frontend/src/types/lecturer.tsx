import {ActiveSubjectFromLecturer} from '@/types/active_subject';
import {Opinion} from '@/types/small'

export type Lecturer = {
    id: number
    name: string
    surname: string 
    subjects: ActiveSubjectFromLecturer[]
    opinions: Opinion[]
}

export type LecturerBasic = {
    id: number
    name: string
    surname: string
    subject_count: number 
}

export type LecturerBasicResponse = {
    lecturers: LecturerBasic[]
}