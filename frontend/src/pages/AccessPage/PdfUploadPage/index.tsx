import React, { useState, useRef } from "react";
import axios from "axios";
import "./PdfUploadPage.css";
import "../AcessPage.css";

type GroupKeys =
  | "CADASTROS BÁSICOS"
  | "RENDA"
  | "HISTÓRICO DA RECEITA FEDERAL"
  | "DADOS DA CTPS"
  | "TITULO ELEITORAL"
  | "DADOS DO PASSAPORTE"
  | "DADOS SOCIAIS"
  | "CELULARES E TELEFONES FIXO"
  | "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA"
  | "AUXÍLIO EMERGENCIAL"
  | "PROCESSOS";

const defaultCustomizationOptions = {
  useWatermark: true,
  includeContract: true,
  includeDocuments: true,
  selectedGroups: {
    "CADASTROS BÁSICOS": ["defaultKey"],
    RENDA: ["defaultKey"],
    "HISTÓRICO DA RECEITA FEDERAL": ["defaultKey"],
    "TITULO ELEITORAL": ["defaultKey"],
    "DADOS DO PASSAPORTE": ["defaultKey"],
    "DADOS SOCIAIS": ["defaultKey"],
    "CELULARES E TELEFONES FIXO": ["defaultKey"],
    "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": ["defaultKey"],
    "AUXÍLIO EMERGENCIAL": ["defaultKey"],
    PROCESSOS: ["defaultKey"],
  } as Record<GroupKeys, string[]>,
};

const customizationLabels: Record<string, string> = {
  useWatermark: "Usar Marca d'Água",
  includeContract: "Incluir Contrato",
  includeDocuments: "Incluir Documentos",
  "CADASTROS BÁSICOS": "Cadastros Básicos",
  RENDA: "Renda",
  "HISTÓRICO DA RECEITA FEDERAL": "Histórico da Receita Federal",
  "DADOS DA CTPS": "Dados da CTPS",
  "TITULO ELEITORAL": "Título Eleitoral",
  "DADOS DO PASSAPORTE": "Dados do Passaporte",
  "DADOS SOCIAIS": "Dados Sociais",
  "CELULARES E TELEFONES FIXO": "Celulares e Telefones Fixos",
  "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA":
    "Pagamentos do Benefício de Prestação Continuada",
  "AUXÍLIO EMERGENCIAL": "Auxílio Emergencial",
  PROCESSOS: "Processos",
};

const PdfUploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [image, setImage] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [showCustomization, setShowCustomization] = useState(false);
  const [customizationOptions, setCustomizationOptions] = useState(
    defaultCustomizationOptions
  );
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const updateCustomizationOption = (key: string, value: boolean) => {
    setCustomizationOptions((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const updateSelectedGroup = (group: GroupKeys, value: boolean) => {
    setCustomizationOptions((prev) => ({
      ...prev,
      selectedGroups: {
        ...prev.selectedGroups,
        [group]: value ? ["defaultKey"] : [],
      },
    }));
    console.log(`Group '${group}' updated to: ${value ? ["defaultKey"] : []}`);
  };

  const resetFileInput = () => {
    setFile(null);
    setImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    const imageInput = document.querySelector<HTMLInputElement>(
      'input[type="file"][accept="image/*"]'
    );
    if (imageInput) {
      imageInput.value = "";
    }
  };

  interface NameResponse {
    name: string;
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) return setMessage("Selecione um Arquivo.");
    if (!(file instanceof File))
      return setMessage("Formato Invalido de Arquivo");
    if (file.type !== "application/pdf")
      return setMessage("Apenas arquivos .pdf");

    setLoading(true);
    try {
      // Upload PDF
      const pdfFormData = new FormData();
      pdfFormData.append("file", file);

      const nameResponse = await axios.post<NameResponse>(
        "http://127.0.0.1:5000/upload-pdf",
        pdfFormData
      );
      const extractedName = nameResponse.data.name;
      console.log("Extracted Name:", extractedName);

      // Upload Image (if provided)
      if (image) {
        const imageFormData = new FormData();
        imageFormData.append("image", image);

        await axios.post("http://127.0.0.1:5000/upload-image", imageFormData);
        console.log("Image uploaded successfully.");
      }

      // Process PDF
      const processFormData = new FormData();
      processFormData.append("password", "515608");
      Object.entries(customizationOptions).forEach(([key, value]) => {
        processFormData.append(
          key,
          typeof value === "boolean" ? value.toString() : JSON.stringify(value)
        );
      });

      const response = await axios.post(
        "http://127.0.0.1:5000/process-pdf",
        processFormData,
        {
          responseType: "blob",
        }
      );

      const contentDisposition = response.headers["content-disposition"];
      const fileNameMatch = contentDisposition?.match(/filename="(.+)"/);
      const fileName = fileNameMatch
        ? fileNameMatch[1]
        : `Relatorio_${extractedName.replace(/\s+/g, "_")}.pdf`;

      const url = window.URL.createObjectURL(new Blob([response.data as Blob]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setMessage("PDF processed successfully.");
    } catch (error) {
      console.error("Error processing PDF:", error);
      setMessage("Error processing PDF.");
    } finally {
      setLoading(false);
      resetFileInput();
      setTimeout(() => setMessage(""), 10000);
    }
  };

  return (
    <div className="pdfUploadPageContainer">
      <h1>Raspador de Pdf</h1>
      <form onSubmit={handleSubmit}>
        <div className="pdfUploaderForm">
          <label>
            Selecionar PDF:
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              ref={fileInputRef}
            />
          </label>
          <label>
            Selecionar Foto (Optional):
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files?.[0] || null)}
            />
          </label>
          <div className="pdfUploaderButtons">
            <button
              className="button-3d"
              type="button"
              onClick={() => setShowCustomization(true)}
            >
              Customizar Layout
            </button>
            <button className="button-3d" type="submit">
              Enviar
            </button>
          </div>
        </div>
      </form>
      {loading ? <p>Carregando...</p> : message && <p>{message}</p>}

      {showCustomization && (
        <div className="customizationDialog">
          <h2>Customize PDF Layout</h2>
          {["useWatermark", "includeContract", "includeDocuments"].map(
            (key) => (
              <label key={key}>
                <input
                  type="checkbox"
                  checked={
                    customizationOptions[
                      key as keyof typeof customizationOptions
                    ] as boolean
                  }
                  onChange={(e) =>
                    updateCustomizationOption(key, e.target.checked)
                  }
                />
                {customizationLabels[key]}
              </label>
            )
          )}
          {Object.keys(customizationOptions.selectedGroups).map((group) => (
            <label key={group}>
              <input
                type="checkbox"
                checked={
                  customizationOptions.selectedGroups[group as GroupKeys]
                    .length > 0
                }
                onChange={(e) =>
                  updateSelectedGroup(group as GroupKeys, e.target.checked)
                }
              />
              {customizationLabels[group]}
            </label>
          ))}
          <button
            className="button-3d"
            onClick={() => setShowCustomization(false)}
          >
            Fechar
          </button>
        </div>
      )}
    </div>
  );
};

export default PdfUploadPage;
