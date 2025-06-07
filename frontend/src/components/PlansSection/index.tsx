import "./PlansSection.css";
import "../Button/Button.css";
import PlanCard from "./PlanCard";
import { useState, useEffect, useRef } from "react";

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
  const [activeDownloadCard, setActiveDownloadCard] = useState<number | null>(
    null
  );
  const [minCardHeight, setMinCardHeight] = useState<number>(0);
  const [maxDescriptionHeight, setMaxDescriptionHeight] = useState<number>(0);
  const cardsContainerRef = useRef<HTMLDivElement>(null);

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
  useEffect(() => {
    let resizeTimeout: NodeJS.Timeout;

    const calculateHeights = () => {
      if (cardsContainerRef.current) {
        const cards =
          cardsContainerRef.current.querySelectorAll(".pricingPlan");
        let maxCardHeight = 0;
        let maxDescHeight = 0;

        setActiveDownloadCard(null);

        const isMobile = window.innerWidth <= 1175;

        cards.forEach((card) => {
          const cardElement = card as HTMLElement;
          const cardContent = cardElement.querySelector(
            ".card-content"
          ) as HTMLElement;
          if (cardContent) {
            cardContent.style.minHeight = "auto";
          }
          const descElement = cardElement.querySelector(
            ".card-description"
          ) as HTMLElement;
          if (descElement) {
            descElement.style.minHeight = "auto";
          }
        });

        if (isMobile) {
          setMaxDescriptionHeight(0);
          setMinCardHeight(0);
          return;
        }

        requestAnimationFrame(() => {
          cards.forEach((card) => {
            const cardElement = card as HTMLElement;
            const descElement = cardElement.querySelector(
              ".card-description"
            ) as HTMLElement;
            if (descElement) {
              const descHeight = descElement.offsetHeight;
              if (descHeight > maxDescHeight) {
                maxDescHeight = descHeight;
              }
            }
          });

          cards.forEach((card) => {
            const cardElement = card as HTMLElement;
            const cardContent = cardElement.querySelector(
              ".card-content"
            ) as HTMLElement;
            const height = cardContent
              ? cardContent.offsetHeight
              : cardElement.offsetHeight;
            if (height > maxCardHeight) {
              maxCardHeight = height;
            }
          });

          setMaxDescriptionHeight(maxDescHeight);
          setMinCardHeight(maxCardHeight);
        });
      }
    };

    calculateHeights();

    const handleResize = () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        calculateHeights();
      }, 150);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      clearTimeout(resizeTimeout);
    };
  }, [selectedPlan]);
  useEffect(() => {
    if (
      cardsContainerRef.current &&
      (minCardHeight > 0 || maxDescriptionHeight > 0)
    ) {
      const cards = cardsContainerRef.current.querySelectorAll(".pricingPlan");
      const isMobile = window.innerWidth <= 1175;

      cards.forEach((card) => {
        const cardElement = card as HTMLElement;
        const cardContent = cardElement.querySelector(
          ".card-content"
        ) as HTMLElement;
        const descElement = cardElement.querySelector(
          ".card-description"
        ) as HTMLElement;

        if (isMobile) {
          if (cardContent) {
            cardContent.style.minHeight = "auto";
          }
          if (descElement) {
            descElement.style.minHeight = "auto";
          }
        } else {
          if (cardContent && minCardHeight > 0) {
            cardContent.style.minHeight = `${minCardHeight}px`;
          }

          if (descElement && maxDescriptionHeight > 0) {
            descElement.style.minHeight = `${maxDescriptionHeight}px`;
          }
        }
      });
    }
  }, [minCardHeight, maxDescriptionHeight]);

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
        <div className="planCardsContainer" ref={cardsContainerRef}>
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
              showDownloadButtons={hideButton}
              className={cardClass}
              cardIndex={index}
              activeDownloadCard={activeDownloadCard}
              setActiveDownloadCard={setActiveDownloadCard}
              minHeight={minCardHeight}
              maxDescriptionHeight={maxDescriptionHeight}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default PlansSection;
