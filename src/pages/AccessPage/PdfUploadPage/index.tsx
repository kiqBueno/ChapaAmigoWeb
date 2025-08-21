import { useState, useRef } from "react";
import "./PdfUploadPage.css";
import "../AcessPage.css";
import "../../../components/Button/Button.css";
import axios from "axios";
import { BASE_URL } from "../../../config/apiConfig";
import BatchUploadPage from "../BatchUploadPage";

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
  | "PARENTES"
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
    PARENTES: ["defaultKey"],
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
  PARENTES: "Parentes",
  ENDEREÇOS: "Endereços",
  "RESUMO DO RELATÓRIO": "Resumo do Relatório",
};

const PdfUploadPage = () => {
  const [files, setFiles] = useState<FileList | null>(null);
  const [image, setImage] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [showCustomization, setShowCustomization] = useState(false);
  const [showBatchUpload, setShowBatchUpload] = useState(false);
  const [customizationOptions, setCustomizationOptions] = useState(
    defaultCustomizationOptions
  );
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // If batch upload is selected, show the batch upload page
  if (showBatchUpload) {
    return <BatchUploadPage onBack={() => setShowBatchUpload(false)} />;
  }

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
    setFiles(null);
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

  interface MultipleFilesResponse {
    files_count: number;
    extracted_names: string[];
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!files || files.length === 0)
      return setMessage("Selecione pelo menos um arquivo.");

    // Verificar se todos os arquivos são PDFs
    for (let i = 0; i < files.length; i++) {
      if (files[i].type !== "application/pdf") {
        return setMessage(`Arquivo ${files[i].name} não é um PDF válido.`);
      }
    }

    setLoading(true);
    try {
      // Enviar todos os arquivos em uma única requisição
      const multipleFormData = new FormData();
      for (let i = 0; i < files.length; i++) {
        multipleFormData.append("files", files[i]);
      }

      const multipleResponse = await axios.post<MultipleFilesResponse>(
        `${BASE_URL}/upload-multiple-pdfs`,
        multipleFormData
      );

      const { files_count, extracted_names } = multipleResponse.data;
      console.log(`Processed ${files_count} files:`, extracted_names);

      if (image) {
        const imageFormData = new FormData();
        imageFormData.append("image", image);
        await axios.post(`${BASE_URL}/upload-image`, imageFormData);
        console.log("Image uploaded successfully.");
      }

      // Processar usando o primeiro arquivo como referência
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
        : files_count === 1
        ? `Relatorio_${extracted_names[0].replace(/\s+/g, "_")}.pdf`
        : `Relatorios_Multiple_Files.zip`;

      const url = window.URL.createObjectURL(new Blob([response.data as Blob]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();

      // Show appropriate message based on file count
      if (files_count === 1) {
        setMessage(`PDF processado com sucesso: ${extracted_names[0]}`);
      } else {
        setMessage(
          `${files_count} PDFs processados e compactados em ZIP com sucesso.`
        );
      }
    } catch (error) {
      console.error("Error processing multiple PDFs:", error);
      setMessage("Error processing multiple PDFs.");
    } finally {
      setLoading(false);
      resetFileInput();
      setTimeout(() => setMessage(""), 10000);
    }
  };

  return (
    <div className="pdfUploadPageContainer">
      <h1>Gerador de Arquivo</h1>

      {/* Processing Mode Selection */}
      <div className="processingModeSection">
        <h2>Selecione o Modo de Processamento</h2>
        <div className="modeButtons">
          <div className="modeOption">
            <h3>📄 Processamento Individual</h3>
            <p>Para poucos arquivos (até 15-20 PDFs)</p>
            <p>Processamento direto com download imediato</p>
            <button
              className="modeButton"
              onClick={() => setShowBatchUpload(false)}
              disabled={showBatchUpload === false}
            >
              {showBatchUpload === false ? "✓ Selecionado" : "Selecionar"}
            </button>
          </div>

          <div className="modeOption">
            <h3>🚀 Processamento em Lotes</h3>
            <p>Para muitos arquivos (até 50 PDFs)</p>
            <button
              className="modeButton"
              onClick={() => setShowBatchUpload(true)}
            >
              Selecionar
            </button>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="pdfUploaderForm">
          <label>
            Selecionar PDFs (múltiplos arquivos):
            <input
              type="file"
              accept="application/pdf"
              multiple
              onChange={(e) => setFiles(e.target.files)}
              ref={fileInputRef}
            />
          </label>
          {files && files.length > 0 && (
            <div className="selectedFilesPreview">
              <h3>Arquivos selecionados ({files.length}):</h3>
              {files.length > 20 && (
                <div className="largeBatchWarning">
                  ⚠️ Você selecionou {files.length} arquivos. Para melhor
                  performance com muitos arquivos, considere usar o{" "}
                  <strong>Processamento em Lotes</strong>.
                </div>
              )}
              <ul>
                {Array.from(files).map((file, index) => (
                  <li key={index}>
                    {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </li>
                ))}
              </ul>
            </div>
          )}
          <label>
            Selecionar Foto (Opcional):
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files?.[0] || null)}
            />
          </label>{" "}
          <div className="pdfUploaderButtonsContainer">
            <div className="pdfUploaderButtons">
              <button
                className="btnPrimary"
                type="button"
                onClick={() => setShowCustomization(true)}
              >
                Customizar Layout
              </button>
              <button className="btnPrimary" type="submit">
                Raspar
              </button>
            </div>
          </div>
        </div>
      </form>

      {loading ? <p>Carregando...</p> : message && <p>{message}</p>}

      {showCustomization && (
        <div className="customizationDialog">
          {" "}
          <h2>Customizar Layout do .pdf</h2>{" "}
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
          ))}{" "}
          <button
            className="btnPrimary"
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
