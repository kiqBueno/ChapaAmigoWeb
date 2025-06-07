import React, { useState } from "react";
import "../Button/Button.css";
import "./DownloadButton.css";

interface DownloadButtonProps {
  onClick?: () => void;
  variant?: "home" | "video" | "header";
}

const DownloadButton = ({ onClick, variant }: DownloadButtonProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const handleClick = (e: React.MouseEvent) => {
    if (variant === "header" || variant === "home") {
      document.getElementById("footerContainer")?.scrollIntoView({
        behavior: "smooth",
      });
      onClick?.();
      return;
    }

    e.preventDefault();
    setIsExpanded(!isExpanded);
    onClick?.();
  };

  const getClassName = () => {
    if (variant === "home") return "btnPrimary btn-home-style";
    if (variant === "video") return "btn-home btn-secondary";
    if (variant === "header") return "btnPrimary";
    return "btnPrimary";
  };

  if (variant === "header" || variant === "home") {
    return (
      <a
        href="#footerContainer"
        className={getClassName()}
        onClick={handleClick}
      >
        Download
      </a>
    );
  }
  return (
    <div className="download-button-container">
      <button className={getClassName()} onClick={handleClick}>
        Download
      </button>{" "}
      {variant === "video" ? (
        <div
          className="downloadSection"
          style={{
            maxHeight: isExpanded ? "8rem" : "0",
            opacity: isExpanded ? 1 : 0,
            overflow: "hidden",
            transition: "max-height 0.3s ease, opacity 0.3s ease",
            marginTop: isExpanded ? "0.5rem" : "0",
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
      ) : (
        <div
          className="download-icons-section"
          style={{
            maxHeight: isExpanded ? "8rem" : "0",
            opacity: isExpanded ? 1 : 0,
            overflow: "hidden",
            transition: "max-height 0.3s ease, opacity 0.3s ease",
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

export default DownloadButton;
