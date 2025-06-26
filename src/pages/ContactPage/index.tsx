import React, { useState } from "react";
import { FaWhatsapp, FaEnvelope } from "react-icons/fa";
import IconWithText from "../../components/IconWithText";
import "./ContactPage.css";
import emailjs from "emailjs-com";

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
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
    const templateParams = {
      name: formData.name,
      email: formData.email,
      phone: formData.phone,
      message: formData.message,
    };

    console.log("Sending email with the following parameters:", templateParams);

    emailjs
      .send(
        "service_lm11h9t",
        "template_hsa87k6",
        templateParams,
        "lnGsmbVan2r2qtWjJ"
      )
      .then(
        (result) => {
          console.log("Email successfully sent!", result.text, templateParams);
          setFormData({
            name: "",
            email: "",
            phone: "",
            message: "",
          });
        },
        (error) => {
          console.error("Error sending email:", error.text, templateParams);
        }
      );
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
      <h1>Fale Conosco</h1>
      <form onSubmit={handleSubmit}>
        <div className="formGroup">
          <label htmlFor="name">Nome:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Digite seu nome"
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
            placeholder="email@email.com"
            required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="phone">Telefone:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            placeholder="00 00000000"
            pattern="[0-9]*"
          />
        </div>
        <div className="formGroup">
          <label htmlFor="message">Mensagem:</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="Digite sua mensagem"
            required
          />
        </div>{" "}
        <div className="submitBtnContainer">
          <button
            type="submit"
            className="btnHome btnPrimary btnLarge btnContact"
          >
            Enviar
          </button>
        </div>
      </form>
    </div>
  );
};

export default ContactPage;
