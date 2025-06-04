import "./PlansSection.css";
import PlanCard from "./PlanCard";
import { useState } from "react";

interface PlansSectionProps {
  hideButton?: boolean;
  cardClass?: string;
}

const PlansSection: React.FC<PlansSectionProps> = ({
  hideButton = false,
  cardClass,
}) => {
  const [selectedPlan, setSelectedPlan] = useState<"mensal" | "anual">(
    "mensal"
  );

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
        "90 dias grátis",
        "Cadastro Verificado",
        "Perfil disponivel para empresas",
        "Melhores posições na plataforma",
        "Acesso a todas as funcionalidades",
      ],
      commonFeatures: [],
    },
    {
      title: "Caminhoneiro",
      price: 30,
      description: "Acesso aos melhores Chapas!",
      commonFeatures: [
        "60 dias grátis",
        "Solicitações em todo território nacional",
        "Suporte para acesso de portaria",
        "Atendimento via e-mail, telefone e WhatsApp",
        "Acesso ao perfil dos contratados",
      ],
      features: ["1 solicitação por dia"],
    },
    {
      title: "Cooperativa",
      price: 70,
      description: "Grandes volumes, grandes Profissionais.",
      commonFeatures: [
        "60 dias grátis",
        "Solicitações em todo território nacional",
        "Suporte para acesso de portaria",
        "Atendimento prioritário via e-mail, telefone e WhatsApp",
        "Acesso ao perfil dos contratados",
      ],
      features: ["Solicitações ilimitadas"],
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
        <h2>{selectedPlan === "mensal" ? "Plano Mensal" : "Plano Anual"}</h2>{" "}
        <div className="planCardsContainer">
          {plans.map((plan, index) => (
            <PlanCard
              key={index}
              title={plan.title}
              price={calculatePrice(plan.price).price}
              priceUnit={calculatePrice(plan.price).unit}
              description={plan.description}
              features={plan.features}
              commonFeatures={plan.commonFeatures}
              hideButton={hideButton}
              className={cardClass}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default PlansSection;
