import React from "react";
import { useNavigate } from "react-router-dom";
import "./PlansSection.css";

interface PlanCardProps {
  title: string;
  price: string;
  description: string;
  features: string[];
  commonFeatures?: string[];
  hideButton?: boolean;
  showDownloadButtons?: boolean;
  priceUnit: string;
  className?: string;
  extraInfo?: string;
  cardIndex?: number;
  activeDownloadCard?: number | null;
  setActiveDownloadCard?: (index: number | null) => void;
  minHeight?: number;
  maxDescriptionHeight?: number;
}

const PlanCard: React.FC<PlanCardProps> = ({
  title,
  price,
  description,
  features,
  commonFeatures = [],
  hideButton = false,
  showDownloadButtons = false,
  priceUnit,
  className,
  extraInfo,
  cardIndex = 0,
  activeDownloadCard = null,
  setActiveDownloadCard,
  minHeight = 0,
  maxDescriptionHeight = 0,
}) => {
  const navigate = useNavigate();
  const isDownloadExpanded = activeDownloadCard === cardIndex;
  return (
    <div
      className={`pricingPlan ${className || ""}`}
      style={{
        paddingBottom: "1rem",
      }}
    >
      <div
        className="card-content"
        style={{
          minHeight: minHeight > 0 ? `${minHeight}px` : "auto",
        }}
      >
        <div className="card-main-content">
          <h2 className="pricingHeader">{title}</h2>
          <h1>
            <span className="pricingPeriod">R$ {price}</span>
            <span className="pricingPrice"> {priceUnit}</span>
          </h1>
          <hr />{" "}
          <h3
            className="card-description"
            style={{
              minHeight:
                maxDescriptionHeight > 0 ? `${maxDescriptionHeight}px` : "auto",
            }}
          >
            {description}
          </h3>{" "}
          {commonFeatures.length > 0 && (
            <div className="commonFeaturesContainer">
              <ul>
                {commonFeatures.map((feature, index) => (
                  <li key={`common-${index}`}>{feature}</li>
                ))}
              </ul>
            </div>
          )}
          <ul>
            {features.map((feature, index) => (
              <li key={index}>{feature}</li>
            ))}
          </ul>
          {extraInfo && (
            <div className="extraInfoContainer">
              <h4>Mais informações:</h4>
              {extraInfo.split("\n").map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          )}{" "}
        </div>{" "}
        <div className="card-button-container">
          {!hideButton && (
            <button
              className="btn-home btn-plan btn-plan-yellow"
              onClick={() => navigate("/planos")}
            >
              Saiba Mais...
            </button>
          )}{" "}
          {showDownloadButtons && (
            <button
              className="btn-home btn-plan btn-plan-yellow"
              onClick={() =>
                setActiveDownloadCard &&
                setActiveDownloadCard(isDownloadExpanded ? null : cardIndex)
              }
              style={{
                marginBottom: isDownloadExpanded ? "0.5rem" : "0",
              }}
            >
              Download
            </button>
          )}
        </div>
      </div>{" "}
      {showDownloadButtons && (
        <div
          className="download-section"
          style={{
            maxHeight: isDownloadExpanded ? "8rem" : "0",
            opacity: isDownloadExpanded ? 1 : 0,
            overflow: "hidden",
            transition: "max-height 0.3s ease, opacity 0.3s ease",
            marginTop: isDownloadExpanded ? "0.5rem" : "0",
          }}
        >
          <div className="downloadButtonsContainer">
            <a
              href="https://apps.apple.com/br/app/chapa-amigo/id6720754868"
              target="_blank"
              rel="noopener noreferrer"
              className="downloadButton"
            >
              <img src="/AppStore.png" alt="Download na App Store" />
            </a>
            <a
              href="https://play.google.com/store/apps/details?id=com.kxp.chapa_amigo&pcampaignid=web_share"
              target="_blank"
              rel="noopener noreferrer"
              className="downloadButton"
            >
              <img src="/GooglePlay.png" alt="Download no Google Play" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlanCard;
