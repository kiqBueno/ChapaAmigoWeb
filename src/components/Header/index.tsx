import "./Header.css";
import { FaBars, FaTimes } from "react-icons/fa";
import { useState } from "react";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleNavClick = (
    event: React.MouseEvent<HTMLAnchorElement, MouseEvent>
  ) => {
    event.preventDefault();
    const targetId = event.currentTarget.getAttribute("href")?.substring(1);
    if (targetId) {
      if (targetId === "homeContainer") {
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: "smooth" });
        }
      }
    }
    setMenuOpen(false);
  };

  return (
    <header className="header">
      <div id="headerContainer">
        <div className="logo">
          <a href="#homeContainer" onClick={handleNavClick}>
            <img src="/Logo.png" alt="Logo" id="Logo" />
          </a>
        </div>
        <div className="navbarCenter">
          <nav className={`nav ${menuOpen ? "open" : ""}`}>
            <ul className="nav-links">
              <li>
                <a href="#homeContainer" onClick={handleNavClick}>
                  Home
                </a>
              </li>
              <li>
                <a href="#FaleConosco" onClick={handleNavClick}>
                  Contato
                </a>
              </li>
              <li>
                <a href="#TermosCondições" onClick={handleNavClick}>
                  Termos e Condições
                </a>
              </li>
              <li>
                <a href="#Cadastrar" onClick={handleNavClick}>
                  Cadastrar
                </a>
              </li>
              <li>
                <a href="#Planos" onClick={handleNavClick}>
                  Planos
                </a>
              </li>
              <li>
                <a
                  href="#footerContainer"
                  className="downloadBtn"
                  onClick={handleNavClick}
                >
                  Download
                </a>
              </li>
            </ul>
          </nav>
        </div>
        <div className="menuIcon" onClick={toggleMenu} aria-label="Toggle menu">
          {menuOpen ? <FaTimes /> : <FaBars />}
        </div>
      </div>
    </header>
  );
};

export default Header;
