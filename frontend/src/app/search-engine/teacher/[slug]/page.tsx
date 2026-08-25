import { Lecturer, LecturerBasicResponse } from "@/types/lecturer";

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
            <h1 className = "text-4xl font-bold mb-4">
                {teacher.name} {teacher.surname}
            </h1>

            <p className = "mb-6">
                Liczba prowadzonych przedmiotów/kursów: {teacher.subjects.length}
            </p>

            {teacher.subjects.length > 0 ? (
                <div className = "spae-y-4">
                    {teacher.subjects.map(
                        (subject, index) => (
                            <div 
                                key = {index}
                            >
                                {subject.name}
                            </div>
                        )
                    )}
                </div>
                ) : (
                    <p>Ten prowadzący nie prowadzi żadnych kursów.</p>
            )}

            <div className = "space-y-2">

                <h2 className = "text-4xl font-bold mb-4">
                    Opinie o prowadzącym
                </h2>
            </div>

            <section className = "mt-10">
                {teacher.opinions.length > 0 ? (
                    <div className = "space-y-4">
                        {teacher.opinions.map((opinion, index) => (
                            <div
                                key = {index}
                                className = "border rounded-lg p-4"
                            >
                                {opinion.content}
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>Nikt jeszcze nie wystawił oceny, Ty to zrób! :3</p>
                )}
            </section>
        </main>
    );
}
