import "./Home.css";
import React from "react";

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
          <p>
            A Plataforma Chapa Amigo foi criada pensando em você, Chapa,
            caminhoneiro e transportador, que busca mais liberdade, controle e
            oportunidades no mundo dos fretes.
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
        <ul>
          <li>
            Conexão direta: Conectamos você diretamente com empresas e
            transportadoras que precisam dos seus serviços. Sem intermediários,
            a negociação é feita de forma transparente e você tem total controle
            sobre os valores.
          </li>
          <li>
            Liberdade para negociar: Defina seus próprios preços, negocie
            diretamente com os clientes e encontre as melhores oportunidades que
            se encaixam na sua rota e disponibilidade.
          </li>
          <li>
            Sem surpresas: Na Plataforma Chapa Amigo, você sabe exatamente
            quanto vai receber pelo seu trabalho. Sem taxas escondidas ou
            comissões inesperadas, o valor combinado é seu!
          </li>
          <li>
            Mensalidade fixa: Com uma mensalidade acessível, você tem acesso
            ilimitado a todas as funcionalidades da plataforma e pode participar
            quando e como quiser. Sem taxas adicionais por frete ou comissão
            sobre seus ganhos.
          </li>
          <li>
            Flexibilidade: Você decide quando e como quer trabalhar. A
            plataforma está sempre disponível para te conectar com novas
            oportunidades, mas a decisão de aceitar ou não é sempre sua.
          </li>
          <li>
            Segurança: A Plataforma Chapa Amigo oferece um ambiente seguro para
            você realizar suas negociações e encontrar parceiros confiáveis.
          </li>
        </ul>
        <h3>A Plataforma Chapa Amigo é a sua parceria na estrada.</h3>
      </main>
    </div>
  );
};

export default Home;
