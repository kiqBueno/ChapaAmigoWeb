import "../../components/PlansSection/PlansSection.css";
import PlansSection from "../../components/PlansSection";
import { useState } from "react";

const PlansPage = () => {
  const [isInfoVisible, setIsInfoVisible] = useState(true);

  const extraInfo = [
    "Por menos de 1 real por dia, você desbloqueia um mundo de oportunidades com a Chapa Amigo.\nFale diretamente com quem interessa, sem intermediários!\nAmbiente seguro para você e suas transações.\nTodas as funcionalidades por um preço acessível, e o melhor: você só paga depois de começar a trabalhar.",
    "Amigo Caminhoneiro, chega de imprevistos e insegurança ao descarregar!\nNossos chapas passam por uma análise completa de antecedentes para sua tranquilidade.\nAdeus estradas perigosas: encontre ajuda confiável sem parar em locais desconhecidos.\nAgilidade e praticidade: em apenas 5 passos, solicite o serviço e acompanhe tudo pelo chat exclusivo.\nHistórico inteligente: repita serviços favoritos com um clique.\nEconomia real: sem taxas escondidas! Apenas uma mensalidade acessível para aproveitar todas as vantagens.\nNão perca tempo nem arrisque sua carga e segurança.",
    "Para cooperativas que buscam escalabilidade e eficiência na descarga.\nEsqueça preocupações com a disponibilidade de chapas.\nCom o Chapa Amigo Empresas, sua cooperativa acessa uma ampla rede de profissionais qualificados, prontos para atender suas demandas sem limite de solicitações mensais.\nAgilize a comunicação com portarias e garanta conformidade nas operações.\nCooperativas têm acesso rápido ao banco de dados completo com fichas e documentação dos operários.\nAcesse históricos de serviços, avaliações e informações relevantes dos chapas, garantindo confiança em cada solicitação.\nInvista na eficiência logística com um preço justo e transparente.\n*Para se tornar uma cooperativa parceira Chapa Amigo, é necessário possuir CNPJ ativo.",
  ];

  return (
    <div id="priceContainer" style={{ marginTop: "5rem" }}>
      <PlansSection
        hideButton={true}
        cardClass="plansPage"
        extraInfo={extraInfo}
      />
      <h3
        className="importantInfoToggle"
        onClick={() => setIsInfoVisible(!isInfoVisible)}
        style={{ margin: "0.5rem auto 2rem" }}
      >
        Informações Importantes
        <span>{isInfoVisible ? "▲" : "▼"}</span>
      </h3>
      {isInfoVisible && (
        <div className="importantInfo">
          <h2>
            Atenção: Informações importantes sobre pagamentos na plataforma
            Chapa Amigo
          </h2>
          <p>
            <strong>Boletos de cobrança:</strong> A Chapa Amigo não emite
            boletos em nenhuma circunstância.
          </p>
          <p>
            <strong>Contatos telefônicos:</strong> Não realizamos ligações para
            solicitar pagamentos.
          </p>
          <p>
            <strong>Pagamentos via Pix:</strong> Nunca realize pagamentos via
            Pix para contas desconhecidas em nome da nossa plataforma.
          </p>
          <p>
            <strong>Pagamentos seguros no app:</strong>
          </p>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>
              Todos os pagamentos e renovações de assinatura devem ser feitos
              exclusivamente pelo aplicativo Chapa Amigo.
            </li>
            <li>
              Utilize as opções de pagamento disponíveis no app para garantir
              transações seguras.
            </li>
          </ul>
          <p>
            <strong>Suporte e dúvidas:</strong>
          </p>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>
              Caso receba solicitações de pagamento fora do aplicativo,
              desconfie.
            </li>
            <li>
              Entre em contato imediatamente com nosso suporte para esclarecer
              dúvidas e garantir sua segurança.
            </li>
          </ul>
          <p>
            <strong>Compromisso com a segurança:</strong>
          </p>
          <p>
            A Chapa Amigo prioriza sua segurança, oferecendo um ambiente
            confiável para gerenciar suas atividades e pagamentos.
          </p>
          <p>
            Siga estas orientações para se proteger contra fraudes e desfrutar
            de uma experiência tranquila na plataforma.
          </p>
          <p>Mantenha-se informado e seguro!</p>
        </div>
      )}
    </div>
  );
};

export default PlansPage;
