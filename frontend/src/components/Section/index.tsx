import { useState, ReactNode } from "react";
import { FaPlus, FaTimes } from "react-icons/fa";
import "./Section.css";

interface SectionProps {
  title: string;
  sectionKey: string;
  children: ReactNode;
}

const Section = ({ title, sectionKey, children }: SectionProps) => {
  const [openSections, setOpenSections] = useState<{ [key: string]: boolean }>(
    {}
  );

  const toggleSection = (section: string) => {
    setOpenSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  return (
    <div className="sectionContainer">
      <h3 onClick={() => toggleSection(sectionKey)}>
        {title}
        {openSections[sectionKey] ? (
          <FaTimes className="icon" />
        ) : (
          <FaPlus className="icon" />
        )}
      </h3>
      {openSections[sectionKey] && (
        <div className="sectionContent">{children}</div>
      )}
    </div>
  );
};

export default Section;
