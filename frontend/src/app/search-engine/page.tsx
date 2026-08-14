'use client';

import Link from "next/link";

import Search from './components/Search/Search';
import { useEffect, useState } from 'react';

type Subject = {
    subject_id: number;
    subject_name: string;
    department: unknown;
    semester: unknown;
    is_obligatory: boolean;
    opinions_count: number;
};

type SubjectsResponse = {
    subjects: Subject[];
};

export default function Home() {
    const [searchValue, setSearchValue] = useState('');
    const [searchType, setSearchType] =
        useState<'przedmioty' | 'prowadzacy'>('przedmioty');

    const [subjects, setSubjects] = useState<Subject[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = (value: string) => {
        console.log(searchType, value);
        setSearchValue(value);
    };

    const fetchSubjects = async () => {
        try {
            setLoading(true);
            setError(null);

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


    return (
        <main className = "flex min-h-screen flex-col items-center justify-between p-24">

            <div className = "z-10 w-full max-w-5xl font-mono text-sm flex flex-col items-center">
            
                <h1 className = {'text-5xl my-10'}>
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
                            <Link
                                key = {subject.subject_id}
                                href = {`/search-engine/subject/${subject.subject_id}`}
                                className = "hover:underline"
                            >
                                {subject.subject_name}
                            </Link>
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
