import "./styles.css";

export default function SearchEngineLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return <main>{children}</main>;
}
