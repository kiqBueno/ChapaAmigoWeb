import "./Footer.css";
import { FaInstagram, FaWhatsapp, FaRegEnvelope } from "react-icons/fa";

const Footer = () => {
  return (
    <footer id="footerContainer">
      <div className="footerLogos">
        <div id="socialIcons">
          <a
            href="https://www.instagram.com/chapaamigo"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaInstagram />
          </a>
          <a
            href="https://api.whatsapp.com/send?phone=5512982882941"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaWhatsapp />
          </a>
          <a
            href="mailto:contato@chapaamigo.com.br"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaRegEnvelope />
          </a>
        </div>
        <div className="footerLogosImages">
          <a
            href="https://apps.apple.com/br/app/chapa-amigo/id6720754868"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img
              src="/AppStore.png"
              alt="Logo App Store"
              className="footerLogoImage"
            />
          </a>
          <a
            href="https://play.google.com/store/apps/details?id=com.kxp.chapa_amigo&pcampaignid=web_share"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img
              src="/GooglePlay.png"
              alt="Logo Google Play"
              className="footerLogoImage"
            />
          </a>
        </div>
      </div>{" "}
      <div className="footerRights">
        <hr className="footer-divider" />
        <p>
          A Plataforma de serviços online Chapa Amigo é gerida por Romicam do
          Brasil LTDA CNPJ: 51.560.854/0001-63
        </p>
        <p>Copyright 2025 © Todos os direitos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;
