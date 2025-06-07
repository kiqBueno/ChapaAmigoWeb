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

  return (
    <a
      href="#footerContainer"
      className={`downloadBtn ${
        variant === "home" ? "downloadBtn--home" : ""
      } ${className}`}
      onClick={handleClick}
    >
      Download
    </a>
  );
};

export default DownloadButton;
