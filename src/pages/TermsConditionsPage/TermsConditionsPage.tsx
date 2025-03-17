import { useState } from "react";
import "./TermsConditionsPage.css";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import termosCondicoes from "../../assets/Termos_de_Uso_Chapa_Amigo.pdf";
import Button from "../../components/Button/Button";

const TermsConditionsPage = () => {
  const [isOpen1, setIsOpen1] = useState(false);
  const section1 = "Conteúdo da seção 1";

  return (
    <div id="termosCondicoesContainer">
      <main>
        <h1>Termos e Condições</h1>
        <div>
          <h3 onClick={() => setIsOpen1(!isOpen1)}>
            Seção 1
            {isOpen1 ? (
              <FaChevronUp className="icon" />
            ) : (
              <FaChevronDown className="icon" />
            )}
          </h3>
          <div className="sectionContent">{isOpen1 && <p>{section1}</p>}</div>
        </div>
        <Button color="#0f3558" padding="0.5rem 1rem">
          <a
            href={termosCondicoes}
            download="Termos_de_Uso_Chapa_Amigo.pdf"
            className="downloadBtn2"
          >
            Baixar Termos de Uso
          </a>
        </Button>
      </main>
    </div>
  );
};

export default TermsConditionsPage;
