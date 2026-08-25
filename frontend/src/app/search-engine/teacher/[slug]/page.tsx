import { Lecturer, LecturerBasicResponse } from "@/types/lecturer";

interface Props {
    params: Promise<{
        slug: string;
    }>;
}

export default async function TeacherPage({ params }: Props) {
    const { slug } = await params;

    const response = await fetch(
        `https://localhost:8000/lecturers/${slug}`,
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

            <div className = "space-y-2">
                <p>
                    <strong>Kursy: </strong>
                </p>

                <h2 className = "text-4xl font-bold mb-4">
                    Opinie o prowadzącym
                </h2>
            </div>
        </main>
    );
}
