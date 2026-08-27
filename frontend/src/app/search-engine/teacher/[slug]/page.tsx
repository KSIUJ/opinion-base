import { Lecturer, LecturerBasicResponse } from "@/types/lecturer";
import AddOpinion from '../../components/AddOpinion/AddOpinion';

interface Props {
    params: Promise<{
        slug: string;
    }>;
}

export default async function TeacherPage({ params }: Props) {
    const { slug } = await params;

    const response = await fetch(
        `http://localhost:8000/lecturers/${slug}`,
        {
            cache: `no-store`,
        }
    );

    const teacher: Lecturer = await response.json();

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    if (!teacher) {
        return <h1>Nie znaleziono prowadzącego.</h1>;
    }

    return (
        <main className = "max-w-4xl mx-auto p-8">
            <header className = "mb-10">
                <div className = "flex items-center gap-5">
                    <div className = "flex h-16 w-16 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                        <span className = "text-2xl font-semibold text-gray-700 dark:text-gray-200">
                            {teacher.name[0]}
                            {teacher.surname[0]}
                        </span>
                    </div>

                    <div>
                        <h1 className = "text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
                            {teacher.name} {teacher.surname}
                        </h1>

                        <p className = "mt-1 text-gray-500 dark:text-gray-400">
                            Prowadzący
                        </p>
                    </div>
                </div>
            </header>

            <section className = "mb-12">
                <h2 className = "text-2xl font-semibold mb-4 text-gray-900 dark:text-gray-100">
                    Informacje
                </h2>

                <div className = "grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className = "rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6 shadow-sm">
                        <p className = "text-sm text-gray-500 dark:text-gray-400">
                            Prowadzone przedmioty
                        </p>

                        <p className = "mt-2 text-3xl font-bold text-gray-900 dark:text-gray-100">
                            {teacher.subjects.length}
                        </p>
                    </div>

                    <div className = "rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6 shadow-sm">
                        <p className = "text-sm text-gray-500 dark:text-gray-400">
                            Liczba opinii
                        </p>

                        <p className = "mt-2 text-3xl font-bold text-gray-900 dark:text-gray-100">
                            {teacher.opinions.length}
                        </p>
                    </div>
                </div>
            </section>

            <section className = "mb-12">
                <h2 className = "text-2xl font-semibold mb-4 text-gray-900 dark:text-gray-100">
                    Prowadzone przedmioty
                </h2>

                {teacher.subjects.length > 0 ? (
                    <div className = "space-y-3">
                        {teacher.subjects.map((subject, index) => (
                            <div
                                key = {index}
                                className = "group flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5 shadow-sm transition hover:shadow-md"
                            >
                                <span className = "font-medium text-gray-900 dark:text-gray-100">
                                    {subject.name}
                                </span>

                                <span className = "text-gray-400 transition-transform group-hover:translate-x-1">
                                    →
                                </span>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className = "text-gray-500 dark:text-gray-400">
                        Ten prowadzący nie prowadzi żadnych kursów.
                    </p>
                )}
            </section>

        <section className = "mt-12">
            <h2 className = "text-2xl font-semibold mb-4 text-gray-900 dark:text-gray-100">
                Opinie o prowadzącym
            </h2>

            <AddOpinion
                lecturerId = {teacher.lecturer_id}
            />

            <div className = "mt-6">
                {teacher.opinions.length > 0 ? (
                    <div className = "space-y-4">
                        {teacher.opinions.map((opinion, index) => (
                            <div
                                key = {index}
                                className = "rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5 shadow-sm"
                            >
                                <p className = "leading-relaxed text-gray-700 dark:text-gray-300">
                                    {opinion.content}
                                </p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className = "rounded-xl border border-dashed border-gray-300 dark:border-gray-600 p-8 text-center">
                        <p className = "text-gray-500 dark:text-gray-400">
                            Nikt jeszcze nie wystawił opinii.
                        </p>

                        <p className = "mt-1 text-sm text-gray-400 dark:text-gray-500">
                            Bądź pierwszą osobą, która podzieli się swoją opinią! :3
                        </p>
                    </div>
                )}
            </div>
        </section>

        </main>
    );
}
