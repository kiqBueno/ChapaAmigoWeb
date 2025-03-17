import React from "react";
import "./PlansSection.css";

interface PlanCardProps {
  title: string;
  monthlyPrice: number;
  annualPrice: number;
  annualPriceDiscounted: number;
}

const PlanCard: React.FC<PlanCardProps> = ({
  title,
  monthlyPrice,
  annualPrice,
  annualPriceDiscounted,
}) => {
  return (
    <div className="planCard">
      <h2>{title}</h2>
      <h3>Plano Mensal</h3>
      <p>
        <strong>Valor: </strong>R$ {monthlyPrice.toFixed(2)}
      </p>
      <h3>Plano Anual</h3>
      <p>
        <strong>De: </strong>R$ {annualPrice.toFixed(2)}
        <br />
        <strong>Por:</strong> R$
        {annualPriceDiscounted.toFixed(2)}
      </p>
    </div>
  );
};

export default PlanCard;
