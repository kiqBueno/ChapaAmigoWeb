import "./Home.css";
import Cards from "../../components/Card/Cards";

const Home = () => {
  return (
    <div id="homeContainer">
      <main className="homeContent">
        <div className="homeText">
          <h1>Descarga Sem Complicações!</h1>
          <h3>
            Chega de dificuldades e taxas abusivas! A Plataforma{" "}
            <strong style={{ color: "#ffca00" }}> Chapa Amigo</strong> é a
            solução completa para chapas e transportadoras que buscam liberdade,
            oportunidades e eficiência.
          </h3>
          <h4>
            Conecte-se diretamente com os melhores profissionais de descarga,
            negocie seus preços e tenha total controle na palma das mãos.
          </h4>
        </div>
        <Cards />
      </main>
    </div>
  );
};

export default Home;
