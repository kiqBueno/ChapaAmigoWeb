import Button from "../../components/Button"; // Importar o componente Button
import "./AcessPage.css";

const AccessPage = () => {
  return (
    <div id="accessPageContainer">
      <Button
        color="#ffca00"
        padding="2rem 1rem"
        onClick={() =>
          window.open("https://chapa-amigo-kxp.web.app/", "_blank")
        }
      >
        Painel Administrativo
      </Button>
      <Button
        color="#ffca00"
        padding="2rem 1rem"
        onClick={() =>
          window.open("https://chapa-amigo-kxp.web.app/", "_blank")
        }
      >
        EXATO
      </Button>
      <Button
        color="#ffca00"
        padding="2rem 1rem"
        onClick={() =>
          window.open("https://chapa-amigo-kxp.web.app/", "_blank")
        }
      >
        Arquivos
      </Button>
      <Button
        color="#ffca00"
        padding="2rem 1rem"
        onClick={() =>
          window.open("https://chapa-amigo-kxp.web.app/", "_blank")
        }
      >
        E-Mail
      </Button>
    </div>
  );
};

export default AccessPage;
