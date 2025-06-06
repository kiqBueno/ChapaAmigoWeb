import "./Carousel.css";

const Carousel = () => {
  const carouselItems = [
    {
      position: 1,
      image: "/carrousel1.jpg",
      alt: "Carrossel 1",
    },
    {
      position: 2,
      image: "/carrousel2.jpg",
      alt: "Carrossel 2",
    },
    {
      position: 3,
      image: "/carrousel3.jpg",
      alt: "Carrossel 3",
    },
    {
      position: 4,
      image: "/carrousel4.jpg",
      alt: "Carrossel 4",
    },
    {
      position: 5,
      image: "/carrousel5.jpg",
      alt: "Carrossel 5",
    },
    {
      position: 6,
      image: "/carrousel6.jpg",
      alt: "Carrossel 6",
    },
  ];
  return (
    <div className="carouselContainer">
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
              <div className="card">
                <img
                  src={item.image}
                  alt={item.alt}
                  className="carouselImage"
                />
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
              <div className="card">
                <img
                  src={item.image}
                  alt={item.alt}
                  className="carouselImage"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Carousel;
