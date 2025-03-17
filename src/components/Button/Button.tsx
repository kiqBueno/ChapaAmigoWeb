import React from 'react';
import './Button.css';

interface ButtonProps {
  color: string;
  padding: string;
  children: React.ReactNode;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({ color, padding, children, onClick }) => {
  return (
    <button className="customButton" style={{ backgroundColor: color, padding: padding }} onClick={onClick}>
      {children}
    </button>
  );
};

export default Button;
