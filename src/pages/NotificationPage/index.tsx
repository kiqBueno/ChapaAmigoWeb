import Carousel from "../../components/Carousel";
import "../../components/Button/Button.css";
import "./NotificationPage.css";

const NotificationPage = () => {
  return (
    <div id="notificationContainer">
      <section className="section section-gray">
        <div className="content-wrapper fade-in-delayed">
          <h1>Ei, Amigo! 👋</h1>
          <p className="subtitle">Sim, é a gente mesmo.</p>
          <h2>Sabemos que não tem sido Fácil...</h2>
          <p className="subtitle">Poucos serviços, muita espera.</p>
          <p className="subtitle">
            <strong>Mas Você Continuou com a Gente. 💪</strong>
          </p>

          <div className="divider"></div>

          <p className="subtitle">E isso faz Toda a diferença!</p>
        </div>
      </section>

      <hr className="sectionDivider" />

      <section className="section section-yellow">
        <h1 style={{ color: "#000" }}>Chegou a Nossa Vez! 🎉</h1>

        <div className="card-container">
          <div className="card">
            <div className="card-icon">🏢</div>
            <div className="card-title">Grandes Empresas estão a Caminho</div>
          </div>
          <div className="card">
            <div className="card-icon">📦</div>
            <div className="card-title">Mais cargas = Mais trabalho</div>
          </div>
          <div className="card">
            <div className="card-icon">💰</div>
            <div className="card-title">Mais trabalho = Dinheiro no bolso</div>
          </div>
        </div>
      </section>

      <hr className="sectionDivider" />

      <section className="section section-gray">
        <div className="content-wrapper">
          <div className="alert">
            <div className="alert-title">⚠️ ATENÇÃO 🚦</div>
            <div className="alert-text">
              Alguns Trabalhadores Não Possuem Endereço Cadastrado na
              Plataforma, outros estão com Endereço Desatualizados.
              <br />
              <br />
              <strong>
                Manter o Endereço Atualizado é Necessário e Garante o Seu
                Sucesso na Plataforma!
              </strong>
              <br />
              <br />É por ali que as empresas vão te encontrar, se liga meu
              chapa!
            </div>
          </div>

          <div className="text-center">
            <div className="card-icon">📱</div>
            <p className="subtitle">
              Abra o seu app CHAPA AMIGO e ATUALIZE-SE!
            </p>
          </div>
        </div>
      </section>

      <hr className="sectionDivider" />

      <section className="section section-white">
        <div className="content-wrapper">
          <h2>O que vem por aí?</h2>

          <div className="bento-container">
            <div className="bento-grid">
              <div className="bento-item">
                <div className="bento-content">
                  <h3>Empresas Verificadas e Comprometidas</h3>
                </div>
              </div>
              <div className="bento-item">
                <div className="bento-content">
                  <h3>Pagamento Garantido pela Plataforma</h3>
                </div>
              </div>
              <div className="bento-item">
                <div className="bento-content">
                  <h3>Sistema Integrado de Gestao de Serviços</h3>
                </div>
              </div>
              <div className="bento-item">
                <div className="bento-content">
                  <h3>Tudo pelo APP que Você Já Tem</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <hr className="sectionDivider" />

      <section className="section section-white no-padding">
        <h1>Obrigado por acreditar Junto com a gente! 🙏</h1>
        <p className="subtitle">
          <strong>Unidos Somos Mais Fortes!</strong>
        </p>

        <Carousel />

        <div className="divider"></div>

        <h2>
          Volta no WhatsApp e Responde SIM, Bora lá fazer parte da equipe que
          mais cresce no Brasil!
        </h2>

        <a
          href="https://api.whatsapp.com/send?phone=5511933058356"
          target="_blank"
          rel="noopener noreferrer"
          className="btnHome btnPrimary btnLarge"
        >
          Voltar ao WhatsApp
        </a>
      </section>
    </div>
  );
};

export default NotificationPage;
