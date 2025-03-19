import React from "react";
import "./PlansSection.css";

interface PlanCardProps {
  title: string;
  monthlyPrice: number;
  annualPrice: number;
  annualPriceDiscounted: number;
  originalPrice: number;
}

const PlanCard: React.FC<PlanCardProps> = ({
  title,
  monthlyPrice,
  annualPrice,
  annualPriceDiscounted,
}) => {
  return (
    <div className="pricing-plan">
      <h2 className="pricing-header">{title}</h2>
      <ul className="pricing-features">
        <li className="pricing-features-item">
          <h3>PLANO MENSAL:</h3>
          <p>R$ {monthlyPrice.toFixed(2)}</p>
        </li>
        <li className="pricing-features-item">
          <h3>PLANO ANUAL:</h3>
          <p>
            De:{" "}
            <span className="priceOriginal">R$ {annualPrice.toFixed(2)}</span>
            <br />
            Por: R$ {annualPriceDiscounted.toFixed(2)}
          </p>
        </li>
      </ul>
      <span className="pricing-price">R$ {monthlyPrice.toFixed(2)}/mês</span>
    </div>
  );
};

export default PlanCard;
