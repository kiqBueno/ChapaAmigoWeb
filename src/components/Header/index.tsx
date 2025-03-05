import "./Header.css";
import { FaBars, FaTimes } from "react-icons/fa";
import { useState } from "react";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <header className="header">
      <div className="headerContainer">
        <div className="logo">
          <a href="#home">
            <img src="/Logo.png" alt="Logo" id="Logo" />
          </a>
        </div>
        <div className="navbarCenter">
          <nav className={`nav ${menuOpen ? "open" : ""}`}>
            <ul className="nav-links">
              <li>
                <a href="#home">Home</a>
              </li>
              <li>
                <a href="#FaleConosco">Contato</a>
              </li>
              <li>
                <a href="#TermosCondições">Termos e Condições</a>
              </li>
              <li>
                <a href="#Cadastrar">Cadastrar</a>
              </li>
              <li>
                <a href="#Planos">Planos</a>
              </li>
              <li>
                <button className="downloadBtn">Download</button>
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
