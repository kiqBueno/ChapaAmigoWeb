import "./PlansSection.css";
import PlanCard from "./PlanCard";

const Price = () => {
  return (
    <div id="priceContainer">
      <h1>Nossos planos</h1>
      <div className="pricePlans">
        <PlanCard
          title="Chapa"
          monthlyPrice={33.0}
          annualPrice={396.0}
          annualPriceDiscounted={198.0}
        />
        <PlanCard
          title="Caminhoneiro ou Transportadora"
          monthlyPrice={20.0}
          annualPrice={240.0}
          annualPriceDiscounted={120.0}
        />
      </div>

      <div className="importantInfo">
        <h2>
          Atenção: Informações Importantes Sobre Pagamentos na Plataforma Chapa
          Amigo
        </h2>
        <p>
          <strong>Boletos de Cobrança:</strong> A Chapa Amigo não emite boletos
          sob nenhuma circunstância.
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
        <ul>
          <li>
            Todos os pagamentos e renovações de assinatura devem ser feitos
            exclusivamente através do aplicativo da Chapa Amigo.
          </li>
          <li>
            Utilize as opções de pagamento disponíveis no app para garantir uma
            transação segura.
          </li>
        </ul>
        <p>
          <strong>Suporte e Dúvidas:</strong>
        </p>
        <ul>
          <li>
            Caso receba solicitações de pagamento fora do aplicativo, desconfie.
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
          A Chapa Amigo prioriza sua segurança, oferecendo um ambiente confiável
          para gerenciar suas atividades e pagamentos.
        </p>
        <p>
          Siga estas orientações para se proteger contra fraudes e desfrutar de
          uma experiência tranquila na plataforma.
        </p>
        <p>Mantenha-se informado e seguro!</p>
      </div>
    </div>
  );
};

export default Price;
