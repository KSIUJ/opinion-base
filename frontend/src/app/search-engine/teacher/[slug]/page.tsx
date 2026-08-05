import { teachers } from "../../data/t";

interface Props {
    params: Promise<{
        slug: string;
    }>;
}

export default async function TeacherPage({ params }: Props) {
    const { slug } = await params;

    const teacher = teachers[slug as keyof typeof teachers];

    if (!teacher) {
        return <h1>Nie znaleziono prowadzącego.</h1>;
    }

    return (
        <main className = "max-w-4xl mx-auto p-8">
            <h1 className = "text-4xl font-bold mb-4">
                {teacher.title}
            </h1>

            <p className = "mb-6">
                {teacher.description}
            </p>

            <div className = "space-y-2">
                <p>
                    <strong>Kursy: </strong> {teacher.courses}
                </p>

                <h2 className = "text-4xl font-bold mb-4">
                    Opinie o prowadzącym
                </h2>
            </div>
        </main>
    );
}
