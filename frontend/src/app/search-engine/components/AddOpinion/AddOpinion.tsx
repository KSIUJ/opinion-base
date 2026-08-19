'use client';

import { useState } from 'react';

interface AddOpinionProps {
    subjectId: number;
    onSuccess?: () => void;
}

export default function AddOpinion({
    subjectId,
    onSuccess,
}: AddOpinionProps) {
    const [content, setContent] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (
        event: React.FormEvent<HTMLFormElement>
    ) => {
        event.preventDefault();

        if (!content.trim()) {
            setError('Treść opinii nie może być pusta.');
            return;
        }

        setIsSubmitting(true);
        setError('');

        try {
            const response = await fetch(
                'http://localhost:8000/subjects/{subjects_id}', //gdzie można wysyłać zapytania do backendu? czy też będzie można do subjects?
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        subject_id: subjectId,
                        content: content.trim(),
                    }),
                }
            );

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            setContent('');

            onSuccess?.();
        } catch (error) {
            console.error(error);
            setError('Nie udało się dodać opinii.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form
            onSubmit = {handleSubmit}
            className = "mt-6 space-y-4"
        >
            <div>
                <label
                    htmlFor = "content"
                    className = "block font-medium mb-1"
                >
                    Twoja opinia
                </label>

                <textarea
                    id = "content"
                    value = {content}
                    onChange = {(e) =>
                        setContent(e.target.value)
                    }
                    placeholder = "Napisz swoją opinię..."
                    className = "w-full border rounded-lg p-3 min-h-32"
                />
            </div>

            {error && (
                <p className = "text-red-600">
                    {error}
                </p>
            )}

            <button
                type = "submit"
                disabled = {isSubmitting}
                className = "px-6 py-2 rounded-lg bg-pink-600 text-white disabled:opacity-50"
            >
                {isSubmitting
                    ? 'Dodawanie...'
                    : 'Dodaj opinię'}
            </button>
        </form>
    );
}
