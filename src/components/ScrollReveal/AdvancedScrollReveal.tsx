import React, { useEffect, useRef, useState } from "react";
import "./AdvancedScrollReveal.css";

interface AdvancedScrollRevealProps {
  children: React.ReactNode;
  direction?: "up" | "down" | "left" | "right";
  distance?: number;
  duration?: number;
  delay?: number;
  scale?: number;
  blur?: boolean;
  threshold?: number;
  className?: string;
}

const AdvancedScrollReveal: React.FC<AdvancedScrollRevealProps> = ({
  children,
  direction = "up",
  distance = 50,
  duration = 1000,
  delay = 0,
  scale = 0.95,
  blur = false,
  threshold = 0.1,
  className = "",
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const currentRef = ref.current;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      {
        threshold,
        rootMargin: "0px 0px -50px 0px",
      }
    );

    if (currentRef) {
      observer.observe(currentRef);
    }

    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, [threshold]);

  const getInitialTransform = () => {
    const transforms = [];

    switch (direction) {
      case "up":
        transforms.push(`translateY(${distance}px)`);
        break;
      case "down":
        transforms.push(`translateY(-${distance}px)`);
        break;
      case "left":
        transforms.push(`translateX(${distance}px)`);
        break;
      case "right":
        transforms.push(`translateX(-${distance}px)`);
        break;
    }

    if (scale !== 1) {
      transforms.push(`scale(${scale})`);
    }

    return transforms.join(" ");
  };

  return (
    <div
      ref={ref}
      className={`advanced-scroll-reveal ${className}`}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible
          ? "translateY(0) translateX(0) scale(1)"
          : getInitialTransform(),
        filter: blur && !isVisible ? "blur(5px)" : "none",
        transition: `all ${duration}ms cubic-bezier(0.25, 0.46, 0.45, 0.94)`,
        transitionDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};

export default AdvancedScrollReveal;
