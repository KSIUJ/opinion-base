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
                className="w-full px-4 py-2 border border-gray-400 rounded-md text-left bg-white text-gray-900"
            >
                {selected ?? placeholder}
            </button>

            {isOpen && (
                <ul className="absolute z-10 w-full mt-1 border border-gray-300 rounded-md bg-white shadow-md max-h-60 overflow-auto">
                        <li
                            onClick={() => handleSelect(null)}
                            className="px-4 py-2 cursor-pointer hover:bg-gray-100 text-gray-500 italic"
                        >
                            {placeholder}
                        </li>
                                    
                    
                    
                    {options.length === 0 && (
                        <li className="px-4 py-2 text-gray-500">Brak opcji</li>
                    )}

                    {options.map((option) => (
                        <li
                            key={option}
                            onClick={() => handleSelect(option)}
                            className="px-4 py-2 cursor-pointer hover:bg-gray-100"
                        >
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}