import "./Header.css";
import { FaBars, FaTimes } from "react-icons/fa";
import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleHomeClick = () => {
    if (location.pathname === "/") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    setMenuOpen(false);
  };

  const handleAnchorClick = (anchor: string) => {
    navigate("/");
    setTimeout(() => {
      window.location.hash = anchor;
    }, 0);
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
                <a
                  href="#videoContainerComercial"
                  onClick={() => handleAnchorClick("Planos")}
                >
                  Comercial
                </a>
              </li>
              <li>
                <a
                  href="#videoContainerCadastro"
                  onClick={() => handleAnchorClick("Cadastrar")}
                >
                  Cadastro
                </a>
              </li>
              <li>
                <Link to="/planos" onClick={() => setMenuOpen(false)}>
                  Planos
                </Link>
              </li>
              <li>
                <Link to="/pagamento" onClick={() => setMenuOpen(false)}>
                  Pagamento
                </Link>
              </li>
              <li>
                <Link to="/termos-condicoes" onClick={() => setMenuOpen(false)}>
                  Termos e Condições
                </Link>
              </li>
              <li>
                <Link to="/contato" onClick={() => setMenuOpen(false)}>
                  Contato
                </Link>
              </li>
              <li>
                <a
                  href="#footerContainer"
                  className="downloadBtn"
                  onClick={() => handleAnchorClick("footerContainer")}
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
