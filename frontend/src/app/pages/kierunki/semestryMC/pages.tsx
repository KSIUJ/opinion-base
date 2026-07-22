import Link from 'next/link';

export default function Home() {
    return (
        <div className = "semestry">
        <h1>Kierunki</h1>
            <div className = "s1">
                <Link href = "/przedmioty1">
                    semestr 1
                </Link>
            </div>

            <div className = "s2">
                <Link href = "/przedmioty1">
                    semestr 2
                </Link>
            </div>

            <div className = "s3">
                <Link href = "/semestryM">
                    semestr 3
                </Link>
            </div>

            <div className = "s4">
                <Link href = "/semestryMC">
                    semestr 4
                </Link>
            </div>
        </div>
    );
}
