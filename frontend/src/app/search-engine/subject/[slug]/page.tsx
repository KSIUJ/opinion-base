import { subjects } from "../../data/subjects";

interface Props {
    params: Promise<{
        slug: string;
    }>;
}

export default async function SubjectPage({ params }: Props) {
    const { slug } = await params;

    const subject = subjects[slug as keyof typeof subjects];

    if (!subject) {
        return <h1>Nie znaleziono przedmiotu.</h1>;
    }

    return (
        <main className = "max-w-4xl mx-auto p-8">
            <h1 className = "text-4xl font-bold mb-4">
                {subject.title}
            </h1>

            <p className = "mb-6">
                {subject.description}
            </p>

            <div className = "space-y-2">
                <p>
                    <strong>ECTS: </strong> {subject.ects}
                </p>

                <p>
                    <strong>Prowadzący: </strong> {subject.teacher}
                </p>
                <p>
                    <strong>Semestr: </strong> {subject.semester}
                </p>
                <p>
                    <strong>Grupa przedmiotów: </strong> {subject.semGroup}
                </p>

                <h2 className = "text-4xl font-bold mb-4">
                    Opinie o przedmiocie
                </h2>
            </div>
        </main>
    );
}
