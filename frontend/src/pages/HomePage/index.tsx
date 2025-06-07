import "./HomePage.css";
import { Link } from "react-router-dom";
import Cards from "../../components/Card/Cards";
import PlansSection from "../../components/PlansSection";
import Carousel from "../../components/Carousel";
import AdvancedScrollReveal from "../../components/ScrollReveal/AdvancedScrollReveal";
import StaggerReveal from "../../components/ScrollReveal/StaggerReveal";
import DownloadButton from "../../components/DownloadButton";

const Home = () => {
  return (
    <div id="homeContainer">
      <main className="homeContent">
        <div className="homeTextContainer">
          <div className="homeText">
            <h2>Sua Liberdade na Estrada</h2>
            <h1 style={{ margin: 0 }}>Começa Aqui!</h1>
            <p style={{ marginBottom: 0 }}>
              Conecte-se aos melhores, negocie direto e tenha o controle de sua
              carga{" "}
            </p>{" "}
            <p>Menos Burocracia, mais lucro!</p>{" "}
            <div className="homeButtonsContainer">
              <DownloadButton variant="home" />
              <Link to="/contato" className="btn-home btn-primary">
                Fale Conosco
              </Link>
            </div>
          </div>
        </div>
        <hr className="footer-divider" />
        <AdvancedScrollReveal
          direction="left"
          duration={900}
          delay={150}
          distance={60}
          scale={0.98}
        >
          <PlansSection />
        </AdvancedScrollReveal>
        <hr className="footer-divider" />{" "}
        <AdvancedScrollReveal
          direction="right"
          duration={1100}
          delay={200}
          distance={80}
          scale={0.94}
          blur
        >
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
              className="btn-home btn-secondary"
              onClick={() => {
                document.getElementById("footerContainer")?.scrollIntoView({
                  behavior: "smooth",
                });
              }}
            >
              Download
            </a>{" "}
          </div>
        </AdvancedScrollReveal>
        <hr className="footer-divider" />{" "}
        <StaggerReveal staggerDelay={180}>
          <Cards />
        </StaggerReveal>
        <hr className="footer-divider" />{" "}
        <AdvancedScrollReveal
          direction="down"
          duration={1200}
          delay={100}
          distance={70}
          scale={0.92}
        >
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
        </AdvancedScrollReveal>
        <hr className="footer-divider" />{" "}
        <AdvancedScrollReveal
          direction="up"
          duration={1000}
          delay={250}
          distance={90}
          scale={0.96}
          blur
        >
          <Carousel />
        </AdvancedScrollReveal>
      </main>
    </div>
  );
};

export default Home;
