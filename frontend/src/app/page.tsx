import Image from "next/image";
import Link from 'next/link';

export default function Home() {
  return (
    <div className = "m-auto">

      <main className = "app-center">
        <Image
          className = "theme-logo-light"
          src = "/images/ksiLogo.png"
          alt = "ksi logo"
          width = {300}
          height = {300}
          priority
        />
        <Image
          className = "theme-logo-dark"
          src = "/images/ksiLogo_transparent.png"
          alt = "ksi logo"
          width = {300}
          height = {300}
          priority
        />

        <br />

        <div className = "flex justify-center items-center text-3xl antialiased not-italic font-mono">
          <h1 className = "site-title">
            KSI OpiniUJ
          </h1>
        </div>

        <br />

        <form>
            Login: <input type = "text" name = "login" /> <br /> <br />
            Hasło: <input type = "text" name = "haslo" /> <br />
        </form>

        <br />

        <Link href = "/search-engine" className = "login-button">
          Zaloguj
        </Link>

      </main>

    </div>
  );
}
