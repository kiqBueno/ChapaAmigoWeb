import "./HomePage.css";
import Cards from "../../components/Card/Cards";
import PlansSection from "../../components/PlansSection";
import Carousel from "../../components/Carousel";

const Home = () => {
  return (
    <div id="homeContainer">
      <main className="homeContent">
        {" "}
        <div className="homeTextContainer">
          <div className="homeText">
            <h1>Descarga Sem Complicações!</h1>
            <h3 style={{ color: "#0f3558" }}>
              Chega de dificuldades e taxas abusivas! A Plataforma{" "}
              <strong style={{ color: "#ffca00" }}> Chapa Amigo</strong> é a
              solução completa para chapas e transportadoras que buscam
              liberdade, oportunidades e eficiência.
            </h3>
            <h4>
              Conecte-se diretamente com os melhores profissionais de descarga,
              negocie seus preços e tenha total controle na palma das mãos.
            </h4>
          </div>{" "}
        </div>
        <hr className="footer-divider" />
        <PlansSection />
        <hr className="footer-divider" />
        <div id="videoContainerComercial" className="videoContainer">
          <h1>Assista nosso Comercial</h1>
          <iframe
            src="https://www.youtube.com/embed/BZyYDXTPXyk?si=HFqsq8z4frxUkO9g"
            title="YouTube video player"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          />{" "}
          <a
            href="#footerContainer"
            className="saibaMaisBtn"
            onClick={() => {
              document.getElementById("footerContainer")?.scrollIntoView({
                behavior: "smooth",
              });
            }}
          >
            Download
          </a>{" "}
        </div>
        <hr className="footer-divider" />
        <Cards />
        <hr className="footer-divider" />{" "}
        <div id="videoContainerCadastro" className="videoContainer">
          <h1>Veja Como se Cadastrar</h1>
          <iframe
            src="https://www.youtube.com/embed/vbh_pOCsX4E?si=lddg59uBCy548O-v"
            title="YouTube video player"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          />
        </div>
        <hr className="footer-divider" />
        <Carousel />
      </main>
    </div>
  );
};

export default Home;
