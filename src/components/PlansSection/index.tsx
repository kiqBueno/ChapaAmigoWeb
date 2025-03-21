import "./PlansSection.css";
import PlanCard from "./PlanCard";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

interface PlansSectionProps {
  showMoreButton?: boolean;
}

const PlansSection: React.FC<PlansSectionProps> = ({
  showMoreButton = true,
}) => {
  const navigate = useNavigate();
  const [selectedPlan, setSelectedPlan] = useState<"mensal" | "anual">("anual");

  return (
    <div id="priceContainer">
      <h1>Nossos planos</h1>
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
        <p>30 dias Grátis!</p>
        <div className="planCardsContainer">
          <PlanCard
            title="Caminhoneiro ou Transportadora"
            selectedPlan={selectedPlan}
          />
          <PlanCard title="Chapa" selectedPlan={selectedPlan} />
        </div>
      </div>
      {showMoreButton && (
        <button
          className="importantInfoToggle"
          onClick={() => navigate("/planos")}
        >
          Saiba Mais...
        </button>
      )}
    </div>
  );
};

export default PlansSection;
