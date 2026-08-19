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
            <h1 className = "text-4xl font-bold mb-6">
                {subject.subject_name}
            </h1>

            <div className = "space-y-3">
                <p>
                    <strong>Kierunek: </strong>
                    {subject.department.name}
                </p>

                <p>
                    <strong>Semestr: </strong>
                    {subject.semester.name}
                </p>

                <p>
                    <strong>Okres: </strong>
                    {subject.semester.is_winter
                        ? 'Zimowy'
                        : 'Letni'}
                </p>

                <p>
                    <strong>Obowiązkowy: </strong>
                    {subject.is_obligatory ? 'Tak' : 'Nie'}
                </p>

                <p>
                    <strong>Liczba opinii: </strong>
                    {subject.opinions_count}
                </p>

                <p>
                    <strong>Liczba grup: </strong>
                    {subject.groups_count}
                </p>
            </div>

            <section className = "mt-10">
                <h2 className = "text-3xl font-bold mb-4">
                    Prowadzący
                </h2>

                {subject.lecturers_info.length > 0 ? (
                    <div className = "space-y-4">
                        {subject.lecturers_info.map(
                            (lecturer, index) => (
                                <div key = {index}>
                                    <p>
                                        <strong>
                                            {lecturer.lecturer_name}{' '}
                                            {lecturer.lecturer_surname}
                                        </strong>
                                    </p>

                                    <p>
                                        <strong>Rola: </strong>
                                        {lecturer.role.name}
                                    </p>
                                </div>
                            )
                        )}
                    </div>
                ) : (
                    <p>Brak informacji o prowadzących.</p>
                )}
            </section>

            <section className = "mt-10">
                <h2 className = "text-3xl font-bold mb-4">
                    Grupy
                </h2>

                {subject.groups.length > 0 ? (
                    <ul className = "list-disc pl-6">
                        {subject.groups.map((group, index) => (
                            <li key = {index}>{group}</li>
                        ))}
                    </ul>
                ) : (
                    <p>Brak grup.</p>
                )}
            </section>

            <h2 className = "text-3xl font-bold mb-4">
                Opinie o przedmiocie
            </h2>

            <AddOpinion
                subjectId = {subject.subject_id}
            />

            <section className = "mt-10">
                {subject.opinions.length > 0 ? (
                    <div className = "space-y-4">
                        {subject.opinions.map((opinion, index) => (
                            <div
                                key = {index}
                                className = "border rounded-lg p-4"
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
