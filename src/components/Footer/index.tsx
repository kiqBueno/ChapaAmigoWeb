import "./Footer.css";
import { FaInstagram, FaWhatsapp, FaRegEnvelope } from "react-icons/fa";

const Footer = () => {
  return (
    <footer id="footerContainer">
      <div className="footerLogos">
        <div id="socialIcons">
          <a
            href="https://www.instagram.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaInstagram />
          </a>
          <a
            href="https://wa.me/yourwhatsappnumber"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaWhatsapp />
          </a>
          <a
            href="mailto:youremail@example.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaRegEnvelope />
          </a>
        </div>
        <div className="footerLogosImages">
          <img
            src="/AppStore.png"
            alt="Logo App Store"
            className="footerLogoImage"
          />
          <img
            src="/GooglePlay.png"
            alt="Logo Google Play"
            className="footerLogoImage"
          />
        </div>
      </div>
      <div className="footerRights">
        <hr />
        <p>Copyright 2025 © Todos os direitos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;
