import "./PlansSection.css";
import PlanCard from "./PlanCard";
import { useState } from "react";

interface PlansSectionProps {
  hideButton?: boolean; // New prop to control button visibility
}

const PlansSection: React.FC<PlansSectionProps> = ({ hideButton = false }) => {
  const [selectedPlan, setSelectedPlan] = useState<"mensal" | "anual">("anual");

  const calculatePrice = (monthlyPrice: number) =>
    selectedPlan === "mensal"
      ? monthlyPrice.toFixed(2)
      : (monthlyPrice / 2).toFixed(2);

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
          <PlanCard
            title="Chapa"
            price={calculatePrice(27)}
            description="Trabalhe primeiro, assine depois!"
            features={[
              "30 dias trabalhando sem custo",
              "Cadastro Verificado",
              "Perfil disponival para empresas",
              "Melhores posições na plataforma",
              "Acesso a todas as funcionalidades",
            ]}
            hideButton={hideButton} // Pass the prop
          />
          <PlanCard
            title="Caminhoneiro"
            price={calculatePrice(30)}
            description="Acesso aos melhores Chapas!"
            features={[
              "Pedidos ilimitados",
              "1 ano grátis",
              "Solicitações em todo território nacional",
              "Suporte para acesso de portaria",
              "Atendimento via e-mail, telefone e WhatsApp",
            ]}
            hideButton={hideButton} // Pass the prop
          />
          <PlanCard
            title="Cooperativa"
            price={calculatePrice(70)}
            description="Grandes cargas requerem grandes Profissionais."
            features={[
              "Pedidos ilimitados",
              "Solicitações em todo território nacional",
              "Suporte para acesso de portaria",
              "Acesso ao perfil dos contratados",
              "Atendimento prioritário via e-mail, telefone e WhatsApp",
            ]}
            hideButton={hideButton} // Pass the prop
          />
        </div>
        <h3>
          Duvidas sobre segurança empresarial, assinaturas ou contratos
          personalizados?
          <br />
          <a href="/contato" target="_blank" rel="noopener noreferrer">
            Entre em contato Conosco
          </a>
        </h3>
      </div>
    </div>
  );
};

export default PlansSection;
