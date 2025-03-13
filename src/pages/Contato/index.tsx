import React, { useState } from "react";
import { FaWhatsapp, FaEnvelope } from "react-icons/fa";
import IconWithText from "../../components/IconWithText";
import "./Contato.css";

const Contato = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
  };

  return (
    <div id="contatoContainer">
      <h1>Contato</h1>
      <div className="iconsWithText">
        <IconWithText
          href="https://api.whatsapp.com/send?phone=5512982882941"
          icon={FaWhatsapp}
          title="WhatsApp:"
          text="+55 12 98288-2941"
        />
        <IconWithText
          href="mailto:contato@chapaamigo.com.br"
          icon={FaEnvelope}
          title="E-Mail:"
          text="contato@chapaamigo.com.br"
        />
      </div>
      <form onSubmit={handleSubmit}>
        <div className="formGroup">
          <label htmlFor="name">Nome:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="message">Mensagem:</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="submitBtn">
          Enviar
        </button>
      </form>
    </div>
  );
};

export default Contato;
