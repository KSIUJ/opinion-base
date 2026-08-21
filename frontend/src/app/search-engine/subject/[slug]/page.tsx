import { Subject, SubjectsResponse } from '@/types/subject';
import AddOpinion from '../../components/AddOpinion/AddOpinion';

interface Props {
    params: Promise<{
        slug: string;
    }>;
}

export default async function SubjectPage({ params }: Props) {
    const { slug } = await params;

    const response = await fetch(
        'http://localhost:8000/subjects/',
        {
            cache: 'no-store',
        }
    );

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data: SubjectsResponse = await response.json();

    const subject = data.subjects.find(
        (subject) => subject.subject_id === Number(slug)
    );

    if (!subject) {
        return <h1>Nie znaleziono przedmiotu.</h1>;
    }

    return (
        <main className = "max-w-4xl mx-auto p-8">
            <h1 className = "text-4xl sm:text-5xl font-bold tracking-tight">
                {subject.subject_name}
            </h1>

            <section className = "mt-8">
                <h2 className = "text-2xl font-semibold mb-4">
                    Podstawowe informacje
                </h2>

                <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-6 shadow-sm bg-white dark:bg-gray-800">
                    <div className = "grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-5">
                        <div>
                            <p className = "text-sm text-gray-500">
                                Kierunek
                            </p>
                            <p className = "font-medium mt-1">
                                {subject.department.name}
                            </p>
                        </div>

                        <div>
                            <p className = "text-sm text-gray-500">
                                Semestr
                            </p>
                            <p className = "font-medium mt-1">
                                {subject.semester.name}
                            </p>
                        </div>

                        <div>
                            <p className = "text-sm text-gray-500">
                                Okres
                            </p>
                            <p className = "font-medium mt-1">
                                {subject.semester.is_winter
                                    ? 'Zimowy'
                                    : 'Letni'}
                            </p>
                        </div>

                        <div>
                            <p className = "text-sm text-gray-500">
                                Obowiązkowy
                            </p>
                            <p className = "font-medium mt-1">
                                {subject.is_obligatory ? 'Tak' : 'Nie'}
                            </p>
                        </div>

                        <div>
                            <p className = "text-sm text-gray-500">
                                Liczba opinii
                            </p>
                            <p className = "font-medium mt-1">
                                {subject.opinions_count}
                            </p>
                        </div>

                        <div>
                            <p className = "text-sm text-gray-500">
                                Liczba grup
                            </p>
                            <p className = "font-medium mt-1">
                                {subject.groups_count}
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <section className = "mt-12">
                <h2 className = "text-2xl font-semibold mb-4">
                    Prowadzący
                </h2>

                {subject.lecturers_info.length > 0 ? (
                    <div className = "grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {subject.lecturers_info.map((lecturer, index) => (
                            <div
                                key = {index}
                                className = "border border-gray-200 dark:border-gray-700 rounded-xl p-6 shadow-sm bg-white dark:bg-gray-800"
                            >
                                <p className = "font-semibold text-lg">
                                    {lecturer.lecturer_name}{' '}
                                    {lecturer.lecturer_surname}
                                </p>

                                <p className = "text-sm text-gray-500 mt-1">
                                    {lecturer.role.name}
                                </p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className = "text-gray-500">
                        Brak informacji o prowadzących.
                    </p>
                )}
            </section>

            <section className = "mt-12">
                <h2 className = "text-2xl font-semibold mb-4">
                    Grupy
                </h2>

                {subject.groups.length > 0 ? (
                    <div className = "grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div className = "flex flex-wrap gap-2">
                            {subject.groups.map((group, index) => (
                                <span
                                    key = {index}
                                    className = "border border-gray-200 dark:border-gray-700 rounded-xl p-6 shadow-sm bg-white dark:bg-gray-800"
                                >
                                    {group}
                                </span>
                            ))}
                        </div>
                    </div>
                ) : (
                    <p className = "text-gray-500">
                        Brak grup.
                    </p>
                )}
            </section>

            <AddOpinion
                subjectId = {subject.subject_id}
            />


            <section className = "mt-10">
                <h2 className = "text-2xl font-semibold mb-4">
                    Opinie o przedmiocie
                </h2>

                {subject.opinions.length > 0 ? (
                    <div className = "space-y-4">
                        {subject.opinions.map((opinion, index) => (
                            <div
                                key = {index}
                                className = "border border-gray-200 dark:border-gray-700 rounded-xl p-6 shadow-sm bg-white dark:bg-gray-800"
                            >
                                {opinion}
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>Nikt jeszcze nie wystawił oceny, Ty to zrób! :3.</p>
                )}
            </section>
        </main>
    );
}
