import React from "react";
import { IconType } from "react-icons";
import "./IconWithText.css";

interface IconWithTextProps {
  href: string;
  icon: IconType;
  title: string;
  text: string;
}

const IconWithText: React.FC<IconWithTextProps> = ({
  href,
  icon: Icon,
  title,
  text,
}) => (
  <div className="iconWithText">
    <a href={href} target="_blank" rel="noreferrer">
      <div className="iconContainer">
        <Icon className="icon" />
      </div>
    </a>
    <h3>{title}</h3>
    <p>{text}</p>
  </div>
);

export default IconWithText;
