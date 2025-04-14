import "./AcessPage.css";
import { Link } from "react-router-dom";

const AccessPage = () => {
  return (
    <div id="accessPageContainer">
      <a
        href="https://chapa-amigo-kxp.web.app/"
        target="_blank"
        rel="noopener noreferrer"
        className="button-3d"
      >
        <button className="button-3d">Painel Administrativo</button>
      </a>
      <a
        href=""
        target="_blank"
        rel="noopener noreferrer"
        className="button-3d"
      >
        <button className="button-3d">Consulta Exato</button>
      </a>
      <a
        href="https://drive.google.com/drive/my-drive"
        target="_blank"
        rel="noopener noreferrer"
        className="button-3d"
      >
        <button className="button-3d">Arquivos</button>
      </a>
      <a
        href="https://mail.hostinger.com/?_task=mail&_mbox=INBOX"
        target="_blank"
        rel="noopener noreferrer"
        className="button-3d"
      >
        <button className="button-3d">E-Mail</button>
      </a>
      <Link to="/acesso_sistema/check-up" className="button-3d">
        <button className="button-3d">Check-Up</button>
      </Link>
    </div>
  );
};

export default AccessPage;
