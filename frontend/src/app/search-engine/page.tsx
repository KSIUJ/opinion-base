'use client';

import Link from "next/link";

import Search from './components/Search/Search';
import Dropdown from './components/Dropdown/Dropdown';
import Tristate from './components/Tristate/Tristate';

import { useEffect, useState } from 'react';
import { SubjectBasic, SubjectsBasicResponse } from '@/types/subject';
import { Subject, SubjectsResponse } from '@/types/subject';
import { LecturerBasic, LecturerBasicResponse } from "@/types/lecturer";


export default function Home() {
    const [searchValue, setSearchValue] = useState('');
    const [departmentOption, setDepartmentOption] = useState<string>('');
    const [semesterOption, setSemesterOption] = useState<string>('');
    const [isObligatory, setIsObligatory] = useState<Boolean | null>(null);
    const [isWinter, setIsWinter] = useState<Boolean | null>(null);


    const [searchType, setSearchType] =
        useState<'przedmioty' | 'prowadzacy'>('przedmioty');

    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [lecturers, setlecturers] = useState<LecturerBasic[]>([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hasSearched, setHasSearched] = useState(false);

    const [departments, setDepartments] = useState<string[]>([]);
    const [semesters, setSemesters] = useState<string[]>([]);

    const handleSearch = (value: string) => {
        console.log(searchType, value);
        setSearchValue(value);
    };

    const fetchSubjects = async () => {
        try {
            setLoading(true);
            setError(null);

            const response_para = new URLSearchParams();

            if(searchValue !== ''){
                response_para.append('subject_name', searchValue);
            }
            
            if(departmentOption !== ''){
                response_para.append('department_name', departmentOption);
            }

            if(semesterOption !== ''){
                response_para.append('semester_name', semesterOption);
            }

            if(isObligatory !== null){
                response_para.append('is_obligatory', String(isObligatory));
            }

            if(isWinter !== null){
                response_para.append('is_winter', String(isWinter));
            }

            const response = await fetch(
                `http://localhost:8000/subjects/?${response_para.toString()}`
            );

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const data: SubjectsResponse = await response.json();

            setSubjects(data.subjects);
            setHasSearched(true);
        } catch (error) {
            console.error(
                'Błąd podczas pobierania przedmiotów:',
                error
            );

            setError(
                'Nie udało się pobrać przedmiotów.'
            );
        } finally {
            setLoading(false);
        }
    };

    const fetchLecturers = async () => {
        try {
            setLoading(true);
            setError(null);

            const response_para = new URLSearchParams();

            if(searchValue !== ''){
                response_para.append('surname', searchValue);
            }
            
            if(departmentOption !== ''){
                response_para.append('department_name', departmentOption);
            }

            const response = await fetch(
                `http://localhost:8000/lecturers/search?${response_para.toString()}`
                // `http://localhost:8000/lecturers?${response_para.toString()}`
            );

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const data: LecturerBasicResponse = await response.json();

            setlecturers(data.lecturers);
            setHasSearched(true);
        } catch (error) {
            console.error(
                'Błąd podczas pobierania przedmiotów:',
                error
            );

            setError(
                'Nie udało się pobrać przedmiotów.'
            );
        } finally {
            setLoading(false);
        }
    }

    const openSubject = () => {
        setSearchType('przedmioty')
        setHasSearched(false);
    };

    const openLecturers = () => {
        setSearchType('prowadzacy')
        setHasSearched(false);
    };


    useEffect(() => {
        const fetchDepartments = async () => {
            try {
                const response = await fetch(`http://localhost:8000/general/departments/list`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch departments: ${response.status}`);
                }
                const data: { names: string[] } = await response.json();
                setDepartments(data.names);
            } catch (error) {
                console.error('Error fetching departments:', error);
            }
        };

        fetchDepartments();

        const fetchSemesters = async () => {
            try {
                const response = await fetch(`http://localhost:8000/general/semesters/list`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch departments: ${response.status}`);
                }
                const data: { names: string[] } = await response.json();
                setSemesters(data.names);
            } catch (error) {
                console.error('Error fetching departments:', error);
            }
        };

        fetchSemesters();

    }, []);


    return (
        <main className = "flex flex-wrap items-center justify-center gap-4 my-7">

            <h1 className = "text-5xl text-green-600">
                ZaopiniUJ:
            </h1>

            <button
                onClick = {() => openSubject()}
                className = {`px-4 py-2 rounded-lg ${
                    searchType === 'przedmioty'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-200 text-gray-700 dark:bg-zinc-800 dark:text-gray-200'
                }`}
            >
                Przedmioty
            </button>

            <button
                onClick = {() => openLecturers()}
                className = {`px-4 py-2 rounded-lg ${
                    searchType === 'prowadzacy'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-200 text-gray-700 dark:bg-zinc-800 dark:text-gray-200'
                }`}
                >
                    Prowadzących
                </button>

                <div className = "flex items-center justify-center gap-3 w-full mt-6">
                    <Search
                        onSearch = {handleSearch}
                        searchType = {searchType}
                    />

                    <button
                        onClick = {searchType === 'przedmioty' ? fetchSubjects : fetchLecturers}
                        disabled = {loading}
                        className = "px-6 py-2 rounded-lg bg-red-600 text-white disabled:opacity-50"
                    >
                        {loading ? 'Szukam...' : 'Szukaj'}
                    </button>
                </div>

                <div className = "grid grid-cols-2 md:grid-cols-4 gap-3 w-full max-w-xl text-justify">
                    <Dropdown
                        options = {departments}
                        onSelect = {(value) => setDepartmentOption(value)}
                        placeholder = "kierunek"
                    />

                    {searchType === 'przedmioty' && (<Dropdown
                        options = {semesters}
                        onSelect = {(value) => setSemesterOption(value)}
                        placeholder = "semestr"
                    />)}

                    {/* {searchType === 'przedmioty' && (<Tristate */}
                    {/*     onSelect = {(value) => setIsObligatory(value)} */}
                    {/*     placeholder = "Obowiązkowość" */}
                    {/*     stringTrue = "Obowiązkowy" */}
                    {/*     stringFalse = "Fakultet" */}
                    {/*     stringNull = "Dowolnie" */}
                    {/*     name = "isObligatory"     */}
                    {/* />)} */}

                    <Dropdown
                        options = {['Obowiązkowy', 'Fakultet', 'Dowolnie']}
                        onSelect = {(value) => {
                            setIsObligatory(
                                value === 'Obowiązkowy'
                                    ? true
                                    : value === 'Fakultet'
                                        ? false
                                        : null
                            );
                        }}
                        placeholder = "typ"
                    />                    
                                  
                    {/* {searchType === 'przedmioty' && (<Tristate */}
                    {/*     onSelect = {(value) => setIsWinter(value)} */}
                    {/*     placeholder = "Okres Roku" */}
                    {/*     stringTrue = "Zimowy" */}
                    {/*     stringFalse = "Letni" */}
                    {/*     stringNull = "Dowolny" */}
                    {/*     name = "isWinter"     */}
                    {/* />)} */}

                    <Dropdown
                        options = {['Zimowy', 'Letni', 'Dowolny']}
                        onSelect = {(value) => {
                            setIsWinter(
                                value === 'Zimowy'
                                    ? true
                                    : value === 'Letni'
                                        ? false
                                        : null
                            );
                        }}
                        placeholder = "pora roku"
                    />

                </div>


                <div className = "flex flex-wrap items-center justify-center gap-4 my-7 w-full">
                    {hasSearched &&(
                        <h2 className = "text-2xl mt-7 mx-2">
                            Znaleziono:
                        </h2>
                    )}
                    {loading && (
                        <p className = "mt-4">
                            Ładowanie...
                        </p>
                    )}

                    {error && (
                        <p className = "mt-4 text-red-500">
                            {error}
                        </p>
                    )}
                </div>

                <div className = "flex flex-wrap items-center justify-center gap-4 my-7 w-full">
                    {!loading && !error && hasSearched && searchType === 'przedmioty' && (                   
                        <div className = "flex flex-col gap-2 mt-4">
                            {subjects.map((subject) => (
                                <div
                                    key={subject.subject_id}
                                    className="flex items-center gap-2"
                                >
                                    <Link
                                        href={`/search-engine/subject/${subject.subject_id}`}
                                        className="hover:underline"
                                    >
                                        {subject.subject_name}
                                    </Link>
                                    
                                    {subject.department.id !== -1 && ( 
                                        <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 text-gray-600 border border-gray-300">
                                            {subject.department.name}
                                        </span>
                                    )}

                                    {subject.department.id === -1 && ( 
                                        <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-gray-600 border border-gray-300">
                                            Nieznany Kierunek
                                        </span>
                                    )}
                                    {subject.semester.id !== -1 && ( 
                                        <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-gray-600 border border-gray-300">
                                            Sem {subject.semester.name}
                                        </span>
                                    )}

                                    {!subject.is_obligatory && (
                                        <span className="text-xs px-2 py-0.5 rounded-full bg-purple-100 text-gray-600 border border-gray-300">
                                            Fakultet
                                        </span>
                                    )}

                                    {subject.semester.id !== -1 && subject.semester.is_winter && (
                                        <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-gray-600 border border-gray-300">
                                            Zimowy
                                        </span>
                                    )}

                                    {subject.semester.id !== -1 && !subject.semester.is_winter && (
                                        <span className="text-xs px-2 py-0.5 rounded-full bg-orange-100 text-gray-600 border border-gray-300">
                                            Letni
                                        </span>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}

                    {!loading && !error && hasSearched && searchType === 'prowadzacy' && (                   
                        <div className = "flex flex-col gap-2 mt-4">
                            {lecturers.map((lecturer) => (
                                <div
                                    key={lecturer.id}
                                    className="flex items-center gap-2"
                                >
                                    <Link
                                        href={`/search-engine/teacher/${lecturer.id}`}
                                        className="hover:underline"
                                    >
                                        {lecturer.name} {lecturer.surname}
                                    </Link>
                                    
                                    {/* <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 text-gray-600 border border-gray-300">
                                        {lecturer.department.name}
                                    </span> */}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

        </main>
    );
}
