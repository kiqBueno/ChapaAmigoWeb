import "./Carousel.css";

const Carousel = () => {
  const carouselItems = [
    {
      position: 1,
      title: "Segurança Total",
      subtitle: "Proteção em cada negociação",
      gradient: "linear-gradient(to right, #ff7e5f, #feb47b)",
    },
    {
      position: 2,
      title: "Conexão Direta",
      subtitle: "Sem intermediários",
      gradient: "linear-gradient(to right, #6a11cb, #2575fc)",
    },
    {
      position: 3,
      title: "Flexibilidade",
      subtitle: "Trabalhe quando quiser",
      gradient: "linear-gradient(to right, #00c6ff, #0072ff)",
    },
    {
      position: 4,
      title: "Preço Justo",
      subtitle: "Mensalidade acessível",
      gradient: "linear-gradient(to right, #ff512f, #dd2476)",
    },
    {
      position: 5,
      title: "Suporte 24/7",
      subtitle: "Sempre disponível",
      gradient: "linear-gradient(to right, #ffb6c1, #ff69b4)",
    },
    {
      position: 6,
      title: "Interface Intuitiva",
      subtitle: "Fácil de usar",
      gradient: "linear-gradient(to right, #ff9a8b, #ffc3a0)",
    },
    {
      position: 7,
      title: "Comunidade Ativa",
      subtitle: "Milhares de usuários",
      gradient: "linear-gradient(to right, #a1c4fd, #c2e9fb)",
    },
    {
      position: 8,
      title: "Tecnologia Avançada",
      subtitle: "Plataforma moderna",
      gradient: "linear-gradient(to right, #fbc2eb, #a18cd1)",
    },
    {
      position: 9,
      title: "Crescimento Garantido",
      subtitle: "Mais oportunidades",
      gradient: "linear-gradient(to right, #84fab0, #8fd3f4)",
    },
  ];

  return (
    <div className="carouselContainer">
      <h2 className="carouselTitle">Vantagens da Plataforma Chapa Amigo</h2>
      <div className="slider">
        {" "}
        <div className="list">
          {/* Primeira passagem dos itens */}
          {carouselItems.map((item) => (
            <div
              key={`first-${item.position}`}
              className="item"
              style={{ "--position": item.position } as React.CSSProperties}
            >
              <div className="card" style={{ background: item.gradient }}>
                <p className="cardTitle">{item.title}</p>
                <p className="cardSubtitle">{item.subtitle}</p>
              </div>
            </div>
          ))}
          {/* Segunda passagem dos itens para loop infinito */}
          {carouselItems.map((item) => (
            <div
              key={`second-${item.position}`}
              className="item"
              style={{ "--position": item.position } as React.CSSProperties}
            >
              <div className="card" style={{ background: item.gradient }}>
                <p className="cardTitle">{item.title}</p>
                <p className="cardSubtitle">{item.subtitle}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Carousel;
