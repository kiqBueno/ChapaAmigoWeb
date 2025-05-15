import { useState, useRef } from "react";
import "./PdfUploadPage.css";
import "../AcessPage.css";
import axios from "axios";
import { BASE_URL } from "../../../config/apiConfig";

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
  | "PROCESSOS"
  | "ENDEREÇOS"
  | "RESUMO DO RELATÓRIO";

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
    ENDEREÇOS: ["defaultKey"],
    "RESUMO DO RELATÓRIO": ["defaultKey"],
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
  "CELULARES E TELEFONES FIXO": "Celulares",
  "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA":
    "Pagamentos do Benefício de Prestação Continuada",
  "AUXÍLIO EMERGENCIAL": "Auxílio Emergencial",
  PROCESSOS: "Processos",
  ENDEREÇOS: "Endereços",
  "RESUMO DO RELATÓRIO": "Resumo do Relatório",
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
      const pdfFormData = new FormData();
      pdfFormData.append("file", file);

      const nameResponse = await axios.post<NameResponse>(
        `${BASE_URL}/upload-pdf`,
        pdfFormData
      );
      const extractedName = nameResponse.data.name;
      console.log("Extracted Name:", extractedName);

      if (image) {
        const imageFormData = new FormData();
        imageFormData.append("image", image);

        await axios.post(`${BASE_URL}/upload-image`, imageFormData);
        console.log("Image uploaded successfully.");
      }

      const processFormData = new FormData();
      processFormData.append("password", "515608");
      Object.entries(customizationOptions).forEach(([key, value]) => {
        processFormData.append(
          key,
          typeof value === "boolean" ? value.toString() : JSON.stringify(value)
        );
      });

      const response = await axios.post(
        `${BASE_URL}/process-pdf`,
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

  const handleCrop = async () => {
    if (!file) return setMessage("Selecione um Arquivo.");

    if (!(file instanceof File) || file.type !== "application/pdf") {
      return setMessage("Apenas arquivos .pdf são permitidos.");
    }

    setLoading(true);
    try {
      const uploadFormData = new FormData();
      uploadFormData.append("file", file);

      const uploadResponse = await fetch(`${BASE_URL}/upload-pdf`, {
        method: "POST",
        body: uploadFormData,
        mode: "cors",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
        },
      });

      if (!uploadResponse.ok) {
        throw new Error(`HTTP error! status: ${uploadResponse.status}`);
      }

      const { name: extractedName } = await uploadResponse.json();

      const cropResponse = await fetch(`${BASE_URL}/crop-pdf`, {
        method: "POST",
        mode: "cors",
        credentials: "same-origin",
        headers: {
          Accept: "application/pdf",
        },
      });

      if (!cropResponse.ok) {
        throw new Error(`HTTP error! status: ${cropResponse.status}`);
      }

      const blob = await cropResponse.blob();
      const contentDisposition = cropResponse.headers.get(
        "content-disposition"
      );
      const fileNameMatch = contentDisposition?.match(/filename="(.+)"/);
      const fileName = fileNameMatch
        ? fileNameMatch[1]
        : `${extractedName.replace(/\s+/g, "_")}.pdf`;

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setMessage("PDF cropped successfully.");
    } catch (error) {
      console.error("Error cropping PDF:", error);
      setMessage("Error cropping PDF.");
    } finally {
      setLoading(false);
      resetFileInput();
      setTimeout(() => setMessage(""), 10000);
    }
  };

  return (
    <div className="pdfUploadPageContainer">
      <h1>Gerador de Arquivo</h1>
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
            Selecionar Foto (Opcional):
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files?.[0] || null)}
            />
          </label>
          <div className="pdfUploaderButtonsContainer">
            <div className="pdfUploaderButtons">
              <button
                className="button-3d"
                type="button"
                onClick={() => setShowCustomization(true)}
              >
                Customizar Layout
              </button>
              <button className="button-3d" type="submit">
                Raspar
              </button>
            </div>
            <button className="button-3d" type="button" onClick={handleCrop}>
              Cortar
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
              <label key={key} className="customizationLabel">
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
