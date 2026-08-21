import {LecturerRole} from '@/types/small';


export type ActiveSubjectFromSubject = {
    lecturer_name: string
    lecturer_surname: string
    role: LecturerRole
}

export type ActiveSubjectFromLecturer = {
    id: number
    name: string
    opinions_count: number
}