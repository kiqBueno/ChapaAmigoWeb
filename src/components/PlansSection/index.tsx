import "./PlansSection.css";
import PlanCard from "./PlanCard";
import { useState } from "react";
import { Link } from "react-router-dom";

interface PlansSectionProps {
  hideButton?: boolean;
  cardClass?: string; // New prop to pass custom class to PlanCard
  extraInfo?: string[]; // New prop for extra information
}

const PlansSection: React.FC<PlansSectionProps> = ({
  hideButton = false,
  cardClass,
  extraInfo = [],
}) => {
  const [selectedPlan, setSelectedPlan] = useState<"mensal" | "anual">("anual");

  const calculatePrice = (monthlyPrice: number) => {
    const isMensal = selectedPlan === "mensal";
    return {
      price: (isMensal ? monthlyPrice : monthlyPrice * 12 * 0.5).toFixed(2),
      unit: isMensal ? "/mês" : "/ano",
    };
  };

  const plans = [
    {
      title: "Chapa",
      price: 27,
      description: "Trabalhe primeiro, assine depois!",
      features: [
        "30 dias trabalhando sem custo",
        "Cadastro Verificado",
        "Perfil disponival para empresas",
        "Melhores posições na plataforma",
        "Acesso a todas as funcionalidades",
      ],
    },
    {
      title: "Caminhoneiro",
      price: 30,
      description: "Acesso aos melhores Chapas!",
      features: [
        "Pedidos ilimitados",
        "1 ano grátis",
        "Solicitações em todo território nacional",
        "Suporte para acesso de portaria",
        "Atendimento via e-mail, telefone e WhatsApp",
      ],
    },
    {
      title: "Cooperativa",
      price: 70,
      description: "Grandes volumes requerem grandes Profissionais.",
      features: [
        "Pedidos ilimitados",
        "Solicitações em todo território nacional",
        "Suporte para acesso de portaria",
        "Acesso ao perfil dos contratados",
        "Atendimento prioritário via e-mail, telefone e WhatsApp",
      ],
    },
  ];

  return (
    <div id="priceContainer">
      <h1>Planos</h1>
      <div className="buttonGroup">
        <button
          style={{
            borderRadius: "7.5px 0 0 7.5px",
            backgroundColor: selectedPlan === "mensal" ? "#e6b800" : "#003366",
            color: selectedPlan === "mensal" ? "#003366" : "#ffffff",
          }}
          onClick={() => setSelectedPlan("mensal")}
        >
          MENSAL
        </button>
        <button
          style={{
            borderRadius: "0 7.5px 7.5px 0",
            backgroundColor: selectedPlan === "anual" ? "#e6b800" : "#003366",
            color: selectedPlan === "anual" ? "#003366" : "#ffffff",
          }}
          onClick={() => setSelectedPlan("anual")}
        >
          ANUAL (50% OFF)
        </button>
      </div>
      <div className="pricingTable">
        <h2>{selectedPlan === "mensal" ? "Plano Mensal" : "Plano Anual"}</h2>
        <div className="planCardsContainer">
          {plans.map((plan, index) => (
            <PlanCard
              key={index}
              title={plan.title}
              price={calculatePrice(plan.price).price}
              priceUnit={calculatePrice(plan.price).unit}
              description={plan.description}
              features={plan.features}
              hideButton={hideButton}
              className={cardClass} // Pass the custom class
              extraInfo={extraInfo[index]} // Pass extra information
            />
          ))}
        </div>
        <h3>
          Duvidas sobre segurança empresarial, assinaturas ou contratos
          personalizados?
          <br />
          <Link to="/contato" target="_blank" rel="noopener noreferrer">
            Entre em contato Conosco
          </Link>
        </h3>
      </div>
    </div>
  );
};

export default PlansSection;
