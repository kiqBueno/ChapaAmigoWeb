import React from "react";
import { useNavigate } from "react-router-dom";
import "./PlansSection.css";

interface PlanCardProps {
  title: string;
  price: string;
  description: string;
  features: string[];
  hideButton?: boolean;
  priceUnit: string;
  className?: string; // New prop for custom class
  extraInfo?: string; // New prop for extra information
}

const PlanCard: React.FC<PlanCardProps> = ({
  title,
  price,
  description,
  features,
  hideButton = false,
  priceUnit,
  className,
  extraInfo,
}) => {
  const navigate = useNavigate();

  return (
    <div className={`pricingPlan ${className || ""}`}>
      <h2 className="pricingHeader">{title}</h2>
      <h1>
        <span className="pricingPeriod">R$ {price}</span>
        <span className="pricingPrice"> {priceUnit}</span>
      </h1>
      <hr />
      <h3>{description}</h3>
      <ul>
        {features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>
      {extraInfo && (
        <div className="extraInfoContainer">
          <h4>Mais Informações:</h4>
          {extraInfo.split("\n").map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
      )}
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
