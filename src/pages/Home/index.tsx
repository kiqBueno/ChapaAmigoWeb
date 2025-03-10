import "./Home.css";
import React from "react";
import Card from "../../components/Card/Card";

const handleNavClick = (
  event: React.MouseEvent<HTMLAnchorElement, MouseEvent>
) => {
  event.preventDefault();
  const targetId = event.currentTarget.getAttribute("href")?.substring(1);
  if (targetId) {
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: "smooth" });
    }
  }
};

const Home = () => {
  return (
    <div id="homeContainer">
      <main className="homeContent">
        <div className="homeText">
          <h1>Cansado de burocracia e taxas abusivas?</h1>
          <h3>
            A Plataforma{" "}
            <strong style={{ color: "#ffca00" }}> Chapa Amigo</strong> é a sua
            parceria na estrada.
          </h3>
          <p>
            Criada pensando em você, Chapa, caminhoneiro e transportador, que
            busca mais liberdade, controle e oportunidades no mundo dos fretes.
          </p>
          <p>
            Com a gente, você tem mais do que uma plataforma de fretes, você tem
            uma ferramenta completa para gerenciar seu trabalho de forma
            eficiente, encontrar as melhores oportunidades e aumentar seus
            ganhos.
          </p>
          <a
            href="#footerContainer"
            className="downloadBtn"
            onClick={handleNavClick}
          >
            Download
          </a>
        </div>
        <div className="cardsContainer">
          <Card
            title="Conexão direta"
            content="Conectamos você diretamente com empresas e transportadoras que precisam dos seus serviços. Sem intermediários, a negociação é feita de forma transparente e você tem total controle sobre os valores."
          />
          <Card
            title="Liberdade para negociar"
            content="Defina seus próprios preços, negocie diretamente com os clientes e encontre as melhores oportunidades que se encaixam na sua rota e disponibilidade."
          />
          <Card
            title="Sem surpresas"
            content="Na Plataforma Chapa Amigo, você sabe exatamente quanto vai receber pelo seu trabalho. Sem taxas escondidas ou comissões inesperadas, o valor combinado é seu!"
          />
          <Card
            title="Mensalidade fixa"
            content="Com uma mensalidade acessível, você tem acesso ilimitado a todas as funcionalidades da plataforma e pode participar quando e como quiser. Sem taxas adicionais por frete ou comissão sobre seus ganhos."
          />
          <Card
            title="Flexibilidade"
            content="Você decide quando e como quer trabalhar. A plataforma está sempre disponível para te conectar com novas oportunidades, mas a decisão de aceitar ou não é sempre sua."
          />
          <Card
            title="Segurança"
            content="A Plataforma Chapa Amigo oferece um ambiente seguro para você realizar suas negociações e encontrar parceiros confiáveis."
          />
        </div>
      </main>
    </div>
  );
};

export default Home;
