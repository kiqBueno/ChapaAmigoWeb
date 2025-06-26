import "../../components/PlansSection/PlansSection.css";
import "../../components/Button/Button.css";
import PlansSection from "../../components/PlansSection";
import Section from "../../components/Section";
import { Link } from "react-router-dom";

const PlansPage = () => {
  return (
    <div id="priceContainer" style={{ padding: "5rem 0 0 0" }}>
      <PlansSection hideButton={true} cardClass="plansPage" />
      <div className="plansPageText">
        <Section title="Chapa" sectionKey="chapa">
          <h4>Trabalhe primeiro, assine depois! Benefícios incluem:</h4>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>90 dias grátis</li>
            <li>Cadastro verificado</li>
            <li>Acesso a todas as funcionalidades</li>
          </ul>
          <h4>
            Por menos de 1 real por dia, você desbloqueia um mundo de
            oportunidades com a Chapa Amigo:
          </h4>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>Fale diretamente com quem interessa, sem intermediários!</li>
            <li>Ambiente seguro para você e suas transações.</li>
            <li>Todas as funcionalidades por um preço acessível.</li>
            <li>Você só paga depois de começar a trabalhar.</li>
          </ul>
        </Section>
        <Section title="Caminhoneiro" sectionKey="caminhoneiro">
          <h4>Acesso aos melhores Chapas! Benefícios incluem:</h4>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>1 solicitação por dia</li>
            <li>1º mês grátis</li>
            <li>Suporte para acesso de portaria</li>
          </ul>
          <h4>
            Amigo Caminhoneiro, chega de imprevistos e insegurança ao
            descarregar:
          </h4>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>
              Nossos chapas passam por uma análise completa de antecedentes para
              sua tranquilidade.
            </li>
            <li>Encontre ajuda confiável sem parar em locais desconhecidos.</li>
            <li>
              Solicite o serviço em apenas 5 passos e acompanhe tudo pelo chat
              exclusivo.
            </li>
            <li>Repita serviços favoritos com um clique.</li>
            <li>Sem taxas escondidas! Apenas uma mensalidade acessível.</li>
          </ul>
        </Section>
        <Section title="Cooperativa" sectionKey="cooperativa">
          <h4>
            Grandes volumes requerem grandes profissionais. Benefícios incluem:
          </h4>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>Pedidos ilimitados</li>
            <li>Atendimento prioritário</li>
          </ul>
          <h4>
            Para cooperativas que buscam escalabilidade e eficiência na
            descarga:
          </h4>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>
              Acesse uma ampla rede de profissionais qualificados, prontos para
              atender suas demandas.
            </li>
            <li>
              Agilize a comunicação com portarias e garanta conformidade nas
              operações.
            </li>
            <li>
              Tenha acesso rápido ao banco de dados completo com fichas e
              documentação dos operários.
            </li>
            <li>
              Consulte históricos de serviços, avaliações e informações
              relevantes dos chapas.
            </li>
          </ul>
          <h4>
            Invista na eficiência logística com um preço justo e transparente.
          </h4>
          <h2>
            <em>
              *Para se tornar uma cooperativa parceira Chapa Amigo, é necessário
              possuir CNPJ ativo.
            </em>
          </h2>
        </Section>
      </div>
      <h3 style={{ color: "#003366" }}>
        Dúvidas sobre segurança empresarial, assinaturas ou contratos
        personalizados?
        <br />
        <Link
          to="/contato"
          rel="noopener noreferrer"
          style={{ color: "#003366" }}
        >
          Entre em contato conosco
        </Link>
      </h3>
    </div>
  );
};

export default PlansPage;
