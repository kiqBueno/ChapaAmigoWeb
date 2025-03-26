import "../../components/PlansSection/PlansSection.css";
import PlansSection from "../../components/PlansSection";
import { useState } from "react";

const PlansPage = () => {
  const [isInfoVisible, setIsInfoVisible] = useState(true);

  const extraInfo = [
    "Por menos que 1 real ao dia, você destrava um mundo de oportunidades assinando com a Chapa Amigo.\nFale direto com quem interessa, sem intermediários!\nAmbiente protegido para você e suas transações.\nTodas as funcionalidades por um preço que cabe no seu bolso e melhor, você só vai pagar depois que já estiver trabalhando.", // Updated text for Chapa
    "Amigo Caminhoneiro chega de imprevistos e insegurança na hora de descarregar!\nNossos chapas passam por uma análise completa de antecedentes para sua tranquilidade.\nAdeus, Estradas Perigosas: Encontre ajuda confiável sem precisar parar em locais desconhecidos.\nAgilidade e Praticidade: Em apenas 5 passos, você solicita o serviço e acompanha tudo pelo chat exclusivo.\nHistórico de pedidos Inteligente: Repita seus serviços favoritos com apenas um clique.\nEconomia de Verdade: Sem taxas escondidas! Apenas uma mensalidade acessível para você aproveitar todas as vantagens.\nNão perca mais tempo nem arrisque sua carga e sua segurança.", // Updated text for Caminhoneiro
    "Para Cooperativas que Buscam Escalabilidade e Eficiência na Descarga.\nEsqueça as preocupações com a disponibilidade de chapas.\nCom o Chapa Amigo Empresas, sua cooperativa tem acesso a uma vasta rede de profissionais qualificados, prontos para atender suas demandas de descarga, sem limite de solicitações mensais.\nAgilize a sua comunicação com as portarias e garanta a conformidade necessária para suas operações.\nCooperativas possuem acesso rápido e fácil ao nosso banco de dados completo com as fichas e documentação dos operários que irão atuar dentro da sua empresa.\nTenha acesso ao histórico de serviços, avaliações e informações relevantes dos chapas, garantindo mais confiança em cada solicitação.\nInvista na eficiência da sua logística com um preço justo e transparente.\n*Para se tornar uma Cooperativa parceira Chapa Amigo, é necessário possuir CNPJ ativo.",
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
            Atenção: Informações Importantes Sobre Pagamentos na Plataforma
            Chapa Amigo
          </h2>
          <p>
            <strong>Boletos de Cobrança:</strong> A Chapa Amigo não emite
            boletos sob nenhuma circunstância.
          </p>
          <p>
            <strong>Contatos Telefônicos:</strong> Não realizamos ligações para
            solicitar pagamentos.
          </p>
          <p>
            <strong>Pagamentos via Pix:</strong> Nunca solicite ou realize
            pagamentos via Pix para contas desconhecidas em nome da nossa
            plataforma.
          </p>
          <p>
            <strong>Pagamentos Seguros no App:</strong>
          </p>
          <ul style={{ listStyleType: "none", paddingLeft: 0 }}>
            <li>
              Todos os pagamentos e renovações de assinatura devem ser feitos
              exclusivamente através do aplicativo da Chapa Amigo.
            </li>
            <li>
              Utilize as opções de pagamento disponíveis no app para garantir
              uma transação segura.
            </li>
          </ul>
          <p>
            <strong>Suporte e Dúvidas:</strong>
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
            <strong>Compromisso com a Segurança:</strong>
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
