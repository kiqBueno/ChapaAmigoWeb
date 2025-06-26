import "./AcessPage.css";
import { Link } from "react-router-dom";

const AccessPage = () => {
  return (
    <div id="accessPageContainer">
      <a
        href="https://chapa-amigo-kxp.web.app/"
        target="_blank"
        rel="noopener noreferrer"
        className="button3d"
      >
        <button className="button3d">Painel Administrativo</button>
      </a>
      <a href="" target="_blank" rel="noopener noreferrer" className="button3d">
        {" "}
        <button className="button3d">Consulta Exato</button>
      </a>
      <a
        href="https://drive.google.com/drive/my-drive"
        target="_blank"
        rel="noopener noreferrer"
        className="button3d"
      >
        <button className="button3d">Arquivos</button>
      </a>
      <a
        href="https://mail.hostinger.com/?_task=mail&_mbox=INBOX"
        target="_blank"
        rel="noopener noreferrer"
        className="button3d"
      >
        <button className="button3d">E-Mail</button>
      </a>{" "}
      <Link to="/acessoSistema/checkUp" className="button3d">
        <button className="button3d">Check-Up</button>
      </Link>
      <Link to="/acessoSistema/carouselManagement" className="button3d">
        <button className="button3d">Gerenciar Carrossel</button>
      </Link>
    </div>
  );
};

export default AccessPage;
