import "./Header.css";
import { FaBars, FaTimes } from "react-icons/fa";
import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleHomeClick = () => {
    if (location.pathname === "/") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    setMenuOpen(false);
  };

  return (
    <header className="header">
      <div id="headerContainer">
        <div className="logo">
          <Link to="/" onClick={handleHomeClick}>
            <img src="/Logo.png" alt="Logo" id="Logo" />
          </Link>
        </div>
        <div className="navbarCenter">
          <nav className={`nav ${menuOpen ? "open" : ""}`}>
            <ul className="nav-links">
              <li>
                <Link to="/" onClick={handleHomeClick}>
                  Home
                </Link>
              </li>
              <li>
                <a href="#FaleConosco" onClick={() => setMenuOpen(false)}>
                  Contato
                </a>
              </li>
              <li>
                <Link to="/termos-condicoes" onClick={() => setMenuOpen(false)}>
                  Termos e Condições
                </Link>
              </li>
              <li>
                <a href="#Cadastrar" onClick={() => setMenuOpen(false)}>
                  Cadastrar
                </a>
              </li>
              <li>
                <a href="#Planos" onClick={() => setMenuOpen(false)}>
                  Planos
                </a>
              </li>
              <li>
                <a
                  href="#footerContainer"
                  className="downloadBtn"
                  onClick={() => setMenuOpen(false)}
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
