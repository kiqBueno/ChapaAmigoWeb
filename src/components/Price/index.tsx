import "./Price.css";

const Price = () => {
  return (
    <div id="priceContainer">
      <h1>Nossos planos</h1>
      <div className="pricePlans">
        <div className="plan">
          <h2>Plano TESTE</h2>
          <p>Ideal para quem está começando.</p>
          <p>Preço: R$ 29,90/mês</p>
          <button>Assinar</button>
        </div>
        <div className="plan">
          <h2>Plano TESTE</h2>
          <p>Para quem busca o máximo de recursos.</p>
          <p>Preço: R$ 49,90/mês</p>
          <button>Assinar</button>
        </div>
      </div>
    </div>
  );
};

export default Price;
