import Image from "next/image";
import Link from 'next/link';

export default function Home() {
  return (
    <div className = "logo">

      <main className = "app-center">
        <Image
          className = "theme-logo"
          src = "/images/ksiLogo_transparent.png"
          alt = "ksi logo"
          width = {300}
          height = {300}
          priority
        />

        <div className = "welcome-text">
          <h1 className = "site-title">
            KSI opinion base
          </h1>
        </div>

        <br />

        <form>
            Login: <input type = "text" name = "login" /> <br /> <br />
            Hasło: <input type = "text" name = "haslo" /> <br />
        </form>

        <br />

        <div className = "login-button">
          <Link href = "/search-engine">
            Zaloguj
          </Link>
        </div>

      </main>

    </div>
  );
}
