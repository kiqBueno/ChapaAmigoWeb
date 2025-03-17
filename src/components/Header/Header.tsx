import { useState, useEffect } from "react";
import "./Header.css";
import Logo from "../../assets/Logo.png";
import Button from "../Button";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 1175) {
        setIsOpen(false);
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <header className="header">
      <div id="headerContainer">
        <img src={Logo} alt="Logo" id="Logo" />
        <div className="navbarCenter">
          <ul className={`nav-links ${isOpen ? "open" : ""}`}>
            <li>
              <a href="#homeContainer" onClick={closeMenu}>
                Home
              </a>
            </li>
            <li>
              <a href="#priceContainer" onClick={closeMenu}>
                Planos
              </a>
            </li>
            <li>
              <a href="#contatoContainer" onClick={closeMenu}>
                Contato
              </a>
            </li>
            <li>
              <a href="/termos-e-condicoes" onClick={closeMenu}>
                Termos e Condições
              </a>
            </li>
          </ul>
          <Button color="#ffca00" padding="0.5rem 1rem">
            Download
          </Button>
        </div>
        <div className="menuIcon" onClick={toggleMenu}>
          <i className="fas fa-bars"></i>
        </div>
      </div>
    </header>
  );
};

export default Header;
