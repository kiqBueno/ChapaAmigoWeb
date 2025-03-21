import React from "react";
import "./PlansSection.css";

interface PlanCardProps {
  title: "Chapa" | "Caminhoneiro ou Transportadora";
  selectedPlan: "mensal" | "anual";
}

const PlanCard: React.FC<PlanCardProps> = ({ title, selectedPlan }) => {
  const prices: Record<
    PlanCardProps["title"],
    {
      mensal: { price: number; total: number };
      anual: { price: number; total: number };
    }
  > = {
    Chapa: {
      mensal: { price: 10, total: 120 },
      anual: { price: 5, total: 60 },
    },
    "Caminhoneiro ou Transportadora": {
      mensal: { price: 25, total: 300 },
      anual: { price: 12.5, total: 150 },
    },
  };

  const monthlyPrice = prices[title].mensal.price;
  const annualPrice = prices[title].anual.price;
  const monthlyTotal = prices[title].mensal.total;
  const annualTotal = prices[title].anual.total;

  return (
    <div className="pricingPlan">
      <div className="pricingPlan2">
        <h2 className="pricingHeader" style={{ margin: "0 0 1rem" }}>
          {title}
        </h2>
        <hr />
        <div>
          <p className="pricingPrice">
            {selectedPlan === "mensal" ? (
              <>
                <strong>MENSAL:</strong> <br />
                <strong>R$ {monthlyPrice.toFixed(2)}</strong> / mês <br />
                <strong>R$ {monthlyTotal.toFixed(2)}</strong> / ano
              </>
            ) : (
              <>
                MENSAL: <br />
                R$ {monthlyPrice.toFixed(2)} / mês <br />
                R$ {monthlyTotal.toFixed(2)} / ano
              </>
            )}
          </p>
          <p className="pricingPrice">
            {selectedPlan === "anual" ? (
              <>
                <strong>ANUAL:</strong> <br />
                <strong>R$ {annualPrice.toFixed(2)}</strong> / mês <br />
                <strong>R$ {annualTotal.toFixed(2)}</strong> / ano
              </>
            ) : (
              <>
                ANUAL: <br />
                R$ {annualPrice.toFixed(2)} / mês <br />
                R$ {annualTotal.toFixed(2)} / ano
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PlanCard;
