import "./DownloadButton.css";

interface DownloadButtonProps {
  variant?: "default" | "home";
  className?: string;
  onClick?: () => void;
}

const DownloadButton = ({
  variant = "default",
  className = "",
  onClick,
}: DownloadButtonProps) => {
  const handleClick = () => {
    document.getElementById("footerContainer")?.scrollIntoView({
      behavior: "smooth",
    });
    if (onClick) {
      onClick();
    }
  };

  const buttonClasses =
    variant === "home"
      ? `btn-home btn-secondary ${className}`
      : `downloadBtn ${className}`;

  return (
    <a href="#footerContainer" className={buttonClasses} onClick={handleClick}>
      Download
    </a>
  );
};

export default DownloadButton;
