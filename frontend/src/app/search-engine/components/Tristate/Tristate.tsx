'use client';

import { useState } from 'react';

type TriStateValue = 'true' | 'false' | 'null';


export type TriStateProps = {
    onSelect: (value: Boolean | null) => void;
    placeholder: string;
    stringTrue: string;
    stringFalse: string;
    stringNull: string;
    name: string;
};

export default function TriState( {onSelect, placeholder = 'Wybierz...', stringTrue, stringFalse, stringNull, name }: TriStateProps) {
       const [selected, setSelected] = useState<TriStateValue>('null');

        const handleSelect = (value: TriStateValue) => {
            setSelected(value);
            if (value === 'true') onSelect(true);
            else if (value === 'false') onSelect(false);
            else onSelect(null);
        };

        return(
        <fieldset className="flex gap-4 mt-4">
            <legend className="mb-2 font-semibold">{placeholder}:</legend>

                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="radio"
                        name={name}
                        checked={selected === 'true'}
                        onChange={() => handleSelect('true')}
                    />
                    <p>{stringTrue}</p>
                </label>

                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="radio"
                        name={name}
                        checked={selected === 'false'}
                        onChange={() => handleSelect('false')}
                    />
                    <p>{stringFalse}</p>
                </label>

                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="radio"
                        name={name}
                        checked={selected === 'null'}
                        onChange={() => handleSelect('null')}
                    />
                    <p>{stringNull}</p>
                </label>
            </fieldset>           
        )
}