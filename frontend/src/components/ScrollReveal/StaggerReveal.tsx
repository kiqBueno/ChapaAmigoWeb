import React, { useEffect, useRef, useState } from "react";
import "./StaggerReveal.css";

interface StaggerRevealProps {
  children: React.ReactNode;
  staggerDelay?: number;
  className?: string;
  threshold?: number;
}

const StaggerReveal: React.FC<StaggerRevealProps> = ({
  children,
  staggerDelay = 150,
  className = "",
  threshold = 0.1,
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
        rootMargin: "0px 0px -30px 0px",
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

  useEffect(() => {
    if (isVisible && ref.current) {
      const children = ref.current.children;
      Array.from(children).forEach((child, index) => {
        const element = child as HTMLElement;
        element.style.transitionDelay = `${index * staggerDelay}ms`;
        element.classList.add("stagger-item-visible");
      });
    }
  }, [isVisible, staggerDelay]);

  return (
    <div
      ref={ref}
      className={`stagger-reveal ${
        isVisible ? "stagger-reveal-visible" : ""
      } ${className}`}
    >
      {React.Children.map(children, (child, index) => (
        <div className="stagger-item" key={index}>
          {child}
        </div>
      ))}
    </div>
  );
};

export default StaggerReveal;
