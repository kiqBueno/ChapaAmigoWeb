import React from "react";
import { useNavigate } from "react-router-dom";
import "./PlansSection.css";

interface PlanCardProps {
  title: string;
  price: string;
  description: string;
  features: string[];
  hideButton?: boolean; // Prop to control button visibility
}

const PlanCard: React.FC<PlanCardProps> = ({
  title,
  price,
  description,
  features,
  hideButton = false, // Default to false
}) => {
  const navigate = useNavigate();

  return (
    <div className="pricingPlan">
      <h2 className="pricingHeader">{title}</h2>
      <h1>
        <span className="pricingPeriod">R$ {price}</span>
        <span className="pricingPrice"> /mês</span>
      </h1>
      <hr />
      <h3>{description}</h3>
      <ul>
        {features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>
      {!hideButton && (
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

export default PlanCard;
