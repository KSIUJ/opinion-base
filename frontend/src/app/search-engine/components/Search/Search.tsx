'use client';

import Link from "next/link";

import { useState, ChangeEvent, KeyboardEvent } from 'react';

export type SearchProps = {
    onSearch: (value: string) => void
    searchType: 'przedmioty' | 'prowadzacy';
}

export default function Search ({ onSearch, searchType }: SearchProps) {
    const [value, setValue] = useState('');

    const searchHandler = (event: ChangeEvent<HTMLInputElement>) => {
        const { target } = event;
        setValue(target.value)
        console.log(value)
    }

    const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
        // if (event.key === 'Enter') { 
            onSearch(value); // issue 1
        // }
    };

    return (
        <div className="relative py-1 w-70" >
            <input
                type = "search"
                value = {value}
                onChange = {searchHandler}
                onKeyDown = {handleKeyDown}
                placeholder = {
                    searchType === 'przedmioty'
                        ? 'Wpisz nazwę przedmiotu...'
                        : 'Wpisz nazwisko prowadzącego...'
                }

                // className = {`w-full px-4 pr-6 py-2 border border-gray-400 rounded-md text-gray-900 placeholder:text-gray-500 focus:outline-none focus:border-gray-500`}
                className={`w-full px-4 pr-6 py-2 border border-gray-400 dark:border-zinc-600 rounded-md text-gray-900 dark:text-gray-100 placeholder:text-gray-500 dark:placeholder:text-gray-400 bg-white dark:bg-zinc-900 focus:outline-none focus:border-gray-500 dark:focus:border-zinc-400`}
            />
            <button 
                type = "submit" 
                className = "absolute right-3 top-1/2 -translate-y-1/2"
            >
                <svg
                    className = "h-4 w-4 fill-current text-gray-500"
                    xmlns = "http://www.w3.org/2000/svg"
                    viewBox = "0 0 20 20"
                >
                    <path
                        fillRule = "evenodd"
                        d = "M13.53 14.47a8 8 0 111.414-1.414l3.96 3.96a1 1 0 01-1.414 1.414l-3.96-3.96zM8 14a6 6 0 100-12 6 6 0 000 12z"
                        clipRule = "evenodd"
                    />
                </svg>
            </button>
        </div>
    );
}
