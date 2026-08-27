'use client';

import { useState } from 'react';

interface AddOpinionProps {
    subjectId?: number;
    lecturerId?: number;
    onSuccess?: () => void;
}

export default function AddOpinion({
    subjectId,
    lecturerId,
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

        if (!subjectId && !lecturerId) {
            setError('Nie określono, czego dotyczy opinia.');
            return;
        }

        setIsSubmitting(true);
        setError('');

        try {
            let url = '';
            let body = {};

            if (subjectId) {
                url = `http://localhost:8000/subjects/${subjectId}/add_opinion`;

                body = {
                    subject_id: subjectId,
                    content: content.trim(),
                };
            } else if (lecturerId) {
                url = `http://localhost:8000/lecturers/${lecturerId}/add_opinion`;

                body = {
                    lecturer_id: lecturerId,
                    content: content.trim(),
                };
            }

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
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
                    className = "block font-medium mb-1 text-gray-900 dark:text-gray-100"
                >
                    Twoja opinia
                </label>

                <textarea
                    id = "content"
                    value = {content}
                    onChange = {(e) => setContent(e.target.value)}
                    placeholder = "Napisz swoją opinię..."
                    className = "w-full border border-gray-300 dark:border-gray-600 rounded-lg p-3 min-h-32 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                />
            </div>

            {error && (
                <p className = "text-red-600 dark:text-red-400">
                    {error}
                </p>
            )}

            <button
                type = "submit"
                disabled = {isSubmitting}
                className = "px-6 py-2 rounded-lg bg-green-600 text-white disabled:opacity-50"
            >
                {isSubmitting
                    ? 'Dodawanie...'
                    : 'Dodaj opinię'}
            </button>
        </form>
    );
}
