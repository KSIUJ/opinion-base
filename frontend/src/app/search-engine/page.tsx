'use client';

import Link from "next/link";

import Search from './components/Search/Search';
import { useState } from 'react';

import { subjects } from "./a/a";

export default function Home() {
    const [searchValue, setSearchValue] = useState('');
    const [searchType, setSearchType] =
        useState<'przedmioty' | 'prowadzacy'>('przedmioty');

    const handleSearch = (value: string) => {
        console.log(searchType, value);
        setSearchValue(value);
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

                <h2 className = {'text-2xl mt-20 mx-2 underline'}>
                        Wyszukiwano:
                </h2>

                {subjects.map(subject => (
                    <Link
                        key = {subject.slug}
                        href = {`/search-engine/subject/${subject.slug}`}
                    >
                        <div>
                            {subject.name}
                        </div>
                    </Link>
                ))}

            </div>

        </main>
    );
}
