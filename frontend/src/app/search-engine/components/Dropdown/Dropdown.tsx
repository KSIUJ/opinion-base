'use client';

import { useState } from 'react';

export type DropdownProps = {
    options: string[];
    onSelect: (value: string) => void;
    placeholder?: string;
};

export default function Dropdown({ options, onSelect, placeholder = 'Wybierz...' }: DropdownProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [selected, setSelected] = useState<string | null>(null);

    const handleSelect = (option: string | null) => {
        setSelected(option);
        if (option !== null) {
            onSelect(option);
        }else{
            onSelect('');
        }
        setIsOpen(false);
    };

    return (
        <div className="pt-1 relative w-full max-w-xs">
            <button
                type="button"
                onClick={() => setIsOpen((prev) => !prev)}
                className="filter-control w-full px-4 py-2 border border-gray-400 rounded-md text-center"
            >
                {selected ?? <span className='text-gray-400 italicr'>{placeholder}</span> }
            </button>
            {/* className={`dark:border-zinc-600 dark:text-gray-100 dark:placeholder:text-gray-400 dark:bg-zinc-900 dark:focus:border-zinc-400`} */}

            {isOpen && (
                <ul className="filter-menu absolute z-10 w-full mt-1 border rounded-md shadow-md max-h-60 overflow-auto">
                        <li
                            onClick={() => handleSelect(null)}
                            className="filter-option px-4 py-2 cursor-pointer text-gray-400 italic"
                        >
                            {placeholder}
                        </li>
                                    
                    
                    
                    {options.length === 0 && (
                        <li className="filter-option px-4 py-2 text-gray-500">Brak opcji</li>
                    )}

                    {options.map((option) => (
                        <li
                            key={option}
                            onClick={() => handleSelect(option)}
                            className="filter-option px-4 py-2 cursor-pointer"
                        >
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
