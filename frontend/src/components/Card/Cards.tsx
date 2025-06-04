import "./Card.css";

const Cards = () => (
  <div className="bentoContainer">
    <ul className="bentoWrapper">
      <li className="firstRowCol1 primaryColorBox primaryTextContrast">
        <h2>Segurança em Primeiro Lugar</h2>
        <hr />
        <span className="bentoSub">
          Verificação de perfis, canal de comunicação exclusivo e suporte
          eficiente garantem a proteção dos usuários e integridade das
          transações.
        </span>
      </li>
      <li className="firstRowCol2 secondaryColorBox secondaryTextContrast">
        <h3>Conexão Direta</h3>
        <hr />
        <span className="bentoSub">
          Converse diretamente com caminhoneiros e transportadoras, sem
          intermediários e taxas. Garantindo negociações transparentes.
        </span>
      </li>{" "}
      <li className="secondRowCol1 textColorBox textColorContrast">
        <h3>Flexibilidade Total</h3>
        <hr />
        <span className="bentoSub">
          Amigo Chapa, aqui você decide quando e como quer trabalhar. A
          plataforma está sempre disponível para te conectar com novas
          oportunidades.
        </span>
      </li>
      <li className="secondRowCol2 accentColorBox accentTextContrast">
        <h3>Acesso Total por um Preço Justo</h3>
        <hr />
        <span className="bentoSub">
          Com uma mensalidade acessível, você tem acesso a todas as
          funcionalidades do nosso aplicativo e pode participar quando e como
          quiser.
        </span>
      </li>
    </ul>
  </div>
);

export default Cards;
