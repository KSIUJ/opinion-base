'use client';

import Link from "next/link";

import Search from './components/Search/Search';
import Dropdown from './components/Dropdown/Dropdown';
import Tristate from './components/Tristate/Tristate';

import { useEffect, useState } from 'react';
import { SubjectBasic, SubjectsBasicResponse } from '@/types/subject';
import { Subject, SubjectsResponse } from '@/types/subject';


export default function Home() {
    const [searchValue, setSearchValue] = useState('');
    const [departmentOption, setDepartmentOption] = useState<string>('');
    const [semesterOption, setSemesterOption] = useState<string>('');
    const [isObligatory, setIsObligatory] = useState<Boolean | null>(null);
    const [isWinter, setIsWinter] = useState<Boolean | null>(null);


    const [searchType, setSearchType] =
        useState<'przedmioty' | 'prowadzacy'>('przedmioty');

    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hasSearched, setHasSearched] = useState(false);

    const handleSearch = (value: string) => {
        console.log(searchType, value);
        setSearchValue(value);
    };

    const fetchSubjects = async () => {
        try {
            setLoading(true);
            setError(null);

<<<<<<< HEAD
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
=======
            const response = await fetch(
                'http://localhost:8000/subjects/all'
            );

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const data: SubjectsResponse = await response.json();

            setSubjects(data.subjects);
>>>>>>> e509620 (Szukaj button)
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

<<<<<<< HEAD
    const fetchLecturers = async () => {}

=======
>>>>>>> e509620 (Szukaj button)

    return (
        <main className = "flex min-h-screen flex-col items-center justify-between p-4">

            <div className = "z-10 w-full max-w-5xl font-mono text-sm flex flex-col items-center">
            
                <h1 className = {'text-5xl my-7'}>
                    Wyszukuj po:
                </h1>

                <div className="flex gap-4 mb-6">
                    <button
                        onClick={() => setSearchType('przedmioty')}
                        className={`px-4 py-2 rounded-lg ${
                            searchType === 'przedmioty'
                                ? 'bg-green-600 text-white'
                                : 'bg-gray-200'
                        }`}
                    >
                        Przedmioty
                    </button>

                    <button
                            onClick={() => setSearchType('prowadzacy')}
                            className={`px-4 py-2 rounded-lg ${
                                searchType === 'prowadzacy'
                                    ? 'bg-green-600 text-white'
                                    : 'bg-gray-200'
                            }`}
                        >
                            Prowadzacy
                        </button>
                </div>

                <Search
                    onSearch = {handleSearch}
                    searchType = {searchType}
                />

<<<<<<< HEAD
                <Dropdown
                    options={[ 'TCS', 'Informatyka', 'Matematyka']}
                    onSelect={(value) => setDepartmentOption(value)}
                    placeholder="Wybierz Kierunek..."
                />

                {searchType === 'przedmioty' && (<Dropdown
                    options={[ '1', '2', '3']}
                    onSelect={(value) => setSemesterOption(value)}
                    placeholder="Wybierz Numer Semestru..."
                />)}

                {searchType === 'przedmioty' && (<Tristate
                    onSelect={(value) => setIsObligatory(value)}
                    placeholder="Obowiązkowość"
                    stringTrue="Obowiązkowy"
                    stringFalse="Fakultet"
                    stringNull="Dowolnie"
                    name="isObligatory"    
                />)}
                              
                              
                {searchType === 'przedmioty' && (<Tristate
                    onSelect={(value) => setIsWinter(value)}
                    placeholder="Okres Roku"
                    stringTrue="Zimowy"
                    stringFalse="Letni"
                    stringNull="Dowolny"
                    name="isWinter"    
                />)}

                <button
                    onClick={searchType === 'przedmioty' ? fetchSubjects : fetchLecturers}
                    disabled={loading}
                    className="mt-7 px-6 py-2 rounded-lg bg-red-600 text-white disabled:opacity-50"
                >
                    {loading ? 'Szukam...' : 'Szukaj'}
                </button>

                {hasSearched &&(
                    <h2 className = "text-2xl mt-7 mx-2 underline">
                        Znaleziono:
=======
                <button
                    onClick={fetchSubjects}
                    disabled={loading}
                    className="mt-4 px-6 py-2 rounded-lg bg-red-600 text-white disabled:opacity-50"
                >
                    {loading ? 'Szukam...' : 'Szukaj'}
                </button>

                {loading &&(
                    <h2 className = "text-2xl mt-20 mx-2 underline">
                        Wyszukiwano:
>>>>>>> e509620 (Szukaj button)
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

                {!loading && !error && searchType === 'przedmioty' && (                   
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
                                
                                <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 text-gray-600 border border-gray-300">
                                    {subject.department.name}
                                </span>
                                
                                <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-gray-600 border border-gray-300">
                                    Sem {subject.semester.name}
                                </span>

                                {!subject.is_obligatory && (
                                    <span className="text-xs px-2 py-0.5 rounded-full bg-purple-100 text-gray-600 border border-gray-300">
                                        Fakultet
                                    </span>
                                )}

                                {subject.semester.is_winter && (
                                    <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-gray-600 border border-gray-300">
                                        Zimowy
                                    </span>
                                )}

                                {!subject.semester.is_winter && (
                                    <span className="text-xs px-2 py-0.5 rounded-full bg-orange-100 text-gray-600 border border-gray-300">
                                        Letni
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {searchType === 'prowadzacy' && (
                    <p className="mt-4">
                        Wyszukiwanie prowadzących nie jest jeszcze
                        podłączone do backendu.
                    </p>
                )}

            </div>

        </main>
    );
}
