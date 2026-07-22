import Link from 'next/link';

export default function Home() {
    return (
        <div className = "kierunki">
        <h1>Kierunki</h1>
        <br />
            <div className = "cs">
                <Link href = "/semestryCS">
                    Informatyka
                </Link>
            </div>

            <br />
            <div className = "tcs">
                <Link href = "/semestryTCS">
                    Informatyka analityczna
                </Link>
            </div>

            <br />
            <div className = "math">
                <Link href = "/semestryM">
                    Matematyka
                </Link>
            </div>

            <br />
            <div className = "matcomp">
                <Link href = "/semestryMC">
                    Matematyka komputerowa
                </Link>
            </div>
        </div>
    );
}
