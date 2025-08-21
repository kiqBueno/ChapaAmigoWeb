import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { BASE_URL } from "../../../config/apiConfig";
import "./BatchUploadPage.css";

interface BatchJob {
  batch_id: string;
  total_files: number;
  processed_files: number;
  failed_files: number;
  status: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  progress_percentage: number;
  result_zip_path?: string;
}

interface BatchUploadResponse {
  batch_id: string;
  files_count: number;
  total_size_mb: number;
  status: string;
  message: string;
}

interface BatchListResponse {
  jobs: BatchJob[];
  total: number;
}

interface BatchUploadProps {
  onBack: () => void;
}

const BatchUploadPage: React.FC<BatchUploadProps> = ({ onBack }) => {
  const [files, setFiles] = useState<FileList | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentBatch, setCurrentBatch] = useState<BatchJob | null>(null);
  const [batchJobs, setBatchJobs] = useState<BatchJob[]>([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const statusCheckInterval = useRef<NodeJS.Timeout | null>(null);

  const MAX_FILES_PER_BATCH = 50;
  const MAX_FILE_SIZE_MB = 10;
  const RECOMMENDED_BATCH_SIZE = 30;

  useEffect(() => {
    loadBatchJobs();
    return () => {
      if (statusCheckInterval.current) {
        clearInterval(statusCheckInterval.current);
      }
    };
  }, []);

  const loadBatchJobs = async () => {
    try {
      const response = await axios.get<BatchListResponse>(
        `${BASE_URL}/list-batch-jobs?limit=20`
      );
      setBatchJobs(response.data.jobs || []);
    } catch (error) {
      console.error("Error loading batch jobs:", error);
    }
  };

  const validateFiles = (
    fileList: FileList
  ): { valid: boolean; message: string } => {
    if (fileList.length === 0) {
      return { valid: false, message: "Selecione pelo menos um arquivo." };
    }

    if (fileList.length > MAX_FILES_PER_BATCH) {
      return {
        valid: false,
        message: `Máximo de ${MAX_FILES_PER_BATCH} arquivos por lote. Selecione menos arquivos ou divida em múltiplos lotes.`,
      };
    }

    let totalSize = 0;
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];

      if (file.type !== "application/pdf") {
        return {
          valid: false,
          message: `Arquivo ${file.name} não é um PDF válido.`,
        };
      }

      const fileSizeMB = file.size / 1024 / 1024;
      if (fileSizeMB > MAX_FILE_SIZE_MB) {
        return {
          valid: false,
          message: `Arquivo ${file.name} é muito grande (${fileSizeMB.toFixed(
            1
          )}MB). Máximo permitido: ${MAX_FILE_SIZE_MB}MB.`,
        };
      }

      totalSize += file.size;
    }

    const totalSizeMB = totalSize / 1024 / 1024;
    if (totalSizeMB > 500) {
      return {
        valid: false,
        message: `Tamanho total muito grande (${totalSizeMB.toFixed(
          1
        )}MB). Máximo permitido: 500MB por lote.`,
      };
    }

    return { valid: true, message: "" };
  };

  const getBatchRecommendation = (fileCount: number): string => {
    if (fileCount <= RECOMMENDED_BATCH_SIZE) {
      return `✅ Tamanho de lote recomendado (${fileCount} arquivos)`;
    } else if (fileCount <= MAX_FILES_PER_BATCH) {
      return `⚠️ Lote grande (${fileCount} arquivos). Considere dividir em lotes menores para melhor performance.`;
    } else {
      return `❌ Lote muito grande (${fileCount} arquivos). Máximo permitido: ${MAX_FILES_PER_BATCH}`;
    }
  };

  const handleFileSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    setFiles(selectedFiles);

    if (selectedFiles && selectedFiles.length > 0) {
      const validation = validateFiles(selectedFiles);
      if (!validation.valid) {
        setMessage(validation.message);
      } else {
        setMessage("");
      }
    }
  };

  const handleBatchUpload = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!files || files.length === 0) {
      setMessage("Selecione pelo menos um arquivo.");
      return;
    }

    const validation = validateFiles(files);
    if (!validation.valid) {
      setMessage(validation.message);
      return;
    }

    setLoading(true);
    setUploadProgress(0);

    try {
      // Upload files to create batch
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }

      // Add processing options
      formData.append("password", "515608");
      formData.append("useWatermark", "true");
      formData.append("includeContract", "true");
      formData.append("includeDocuments", "true");
      formData.append("selectedGroups", "{}");
      formData.append("summaryTexts", "[]");

      const uploadResponse = await axios.post<BatchUploadResponse>(
        `${BASE_URL}/upload-batch-pdfs`,
        formData
      );

      const { batch_id, files_count, total_size_mb } = uploadResponse.data;

      setMessage(
        `Lote criado com sucesso! ${files_count} arquivos (${total_size_mb}MB). Iniciando processamento...`
      );

      // Start processing
      await axios.post(`${BASE_URL}/start-batch-processing`, { batch_id });

      // Create batch job object for tracking
      const newBatch: BatchJob = {
        batch_id,
        total_files: files_count,
        processed_files: 0,
        failed_files: 0,
        status: "processing",
        created_at: new Date().toISOString(),
        progress_percentage: 0,
      };

      setCurrentBatch(newBatch);
      startStatusChecking(batch_id);

      // Reset form
      setFiles(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (error) {
      console.error("Error uploading batch:", error);
      let errorMessage = "Erro ao fazer upload do lote.";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      setMessage(`Erro: ${errorMessage}`);
    } finally {
      setLoading(false);
      setUploadProgress(0);
    }
  };

  const startStatusChecking = (batchId: string) => {
    if (statusCheckInterval.current) {
      clearInterval(statusCheckInterval.current);
    }

    statusCheckInterval.current = setInterval(async () => {
      try {
        const response = await axios.get<BatchJob>(
          `${BASE_URL}/batch-status?batch_id=${batchId}`
        );
        const updatedBatch = response.data;

        setCurrentBatch(updatedBatch);

        if (
          updatedBatch.status === "completed" ||
          updatedBatch.status === "failed" ||
          updatedBatch.status === "cancelled"
        ) {
          if (statusCheckInterval.current) {
            clearInterval(statusCheckInterval.current);
            statusCheckInterval.current = null;
          }

          if (updatedBatch.status === "completed") {
            setMessage(
              `✅ Processamento concluído! ${updatedBatch.processed_files} arquivos processados com sucesso.`
            );
          } else if (updatedBatch.status === "failed") {
            setMessage(
              `❌ Processamento falhou. Verifique os logs para mais detalhes.`
            );
          } else {
            setMessage(`⚠️ Processamento cancelado.`);
          }

          // Reload batch jobs list
          loadBatchJobs();
        }
      } catch (error) {
        console.error("Error checking batch status:", error);
      }
    }, 2000); // Check every 2 seconds
  };

  const downloadBatchResult = async (batchId: string) => {
    try {
      const response = await axios.get(
        `${BASE_URL}/download-batch-result?batch_id=${batchId}`,
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([response.data as Blob]));
      const link = document.createElement("a");
      link.href = url;

      const contentDisposition = response.headers["content-disposition"];
      const fileNameMatch = contentDisposition?.match(/filename="(.+)"/);
      const fileName = fileNameMatch
        ? fileNameMatch[1]
        : `batch_${batchId}.zip`;

      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage(`Download iniciado: ${fileName}`);
    } catch (error) {
      console.error("Error downloading batch result:", error);
      let errorMessage = "Erro ao baixar resultado do lote.";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      setMessage(`Erro: ${errorMessage}`);
    }
  };

  const formatFileSize = (bytes: number): string => {
    const mb = bytes / 1024 / 1024;
    return `${mb.toFixed(1)} MB`;
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case "completed":
        return "#28a745";
      case "processing":
        return "#007bff";
      case "failed":
        return "#dc3545";
      case "cancelled":
        return "#6c757d";
      default:
        return "#ffc107";
    }
  };

  const getStatusIcon = (status: string): string => {
    switch (status) {
      case "completed":
        return "✅";
      case "processing":
        return "⏳";
      case "failed":
        return "❌";
      case "cancelled":
        return "⚠️";
      default:
        return "📋";
    }
  };

  return (
    <div className="batchUploadPageContainer">
      <div className="headerSection">
        <button className="backButton" onClick={onBack}>
          ← Voltar
        </button>
        <h1>Processamento em Lotes</h1>
        <p className="subtitle">
          Processe até {MAX_FILES_PER_BATCH} PDFs por lote. Para{" "}
          {files?.length || 0} arquivos, recomenda-se dividir em lotes de{" "}
          {RECOMMENDED_BATCH_SIZE} arquivos.
        </p>
      </div>

      {/* Upload Form */}
      <div className="uploadSection">
        <form onSubmit={handleBatchUpload}>
          <div className="fileUploadArea">
            <label className="fileLabel">
              📁 Selecionar PDFs para Processamento em Lote:
              <input
                type="file"
                accept="application/pdf"
                multiple
                onChange={handleFileSelection}
                ref={fileInputRef}
                disabled={loading}
              />
            </label>

            {files && files.length > 0 && (
              <div className="selectedFilesPreview">
                <h3>
                  Arquivos Selecionados ({files.length}/{MAX_FILES_PER_BATCH})
                </h3>

                <div className="batchRecommendation">
                  {getBatchRecommendation(files.length)}
                </div>

                <div className="filesGrid">
                  {Array.from(files)
                    .slice(0, 10)
                    .map((file, index) => (
                      <div key={index} className="fileItem">
                        <span className="fileName">{file.name}</span>
                        <span className="fileSize">
                          {formatFileSize(file.size)}
                        </span>
                      </div>
                    ))}
                  {files.length > 10 && (
                    <div className="moreFiles">
                      ... e mais {files.length - 10} arquivos
                    </div>
                  )}
                </div>

                <div className="totalSize">
                  Total:{" "}
                  {formatFileSize(
                    Array.from(files).reduce((sum, file) => sum + file.size, 0)
                  )}
                </div>
              </div>
            )}
          </div>

          <div className="actionButtons">
            <button
              type="submit"
              className="btnPrimary"
              disabled={loading || !files || files.length === 0}
            >
              {loading ? "Processando..." : "Iniciar Processamento em Lote"}
            </button>
          </div>
        </form>

        {/* Upload Progress */}
        {loading && uploadProgress > 0 && (
          <div className="progressSection">
            <div className="progressBar">
              <div
                className="progressFill"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <span>Upload: {uploadProgress}%</span>
          </div>
        )}
      </div>

      {/* Current Batch Status */}
      {currentBatch && (
        <div className="currentBatchSection">
          <h2>Lote Atual em Processamento</h2>
          <div className="batchCard">
            <div className="batchHeader">
              <span className="batchId">
                ID: {currentBatch.batch_id.slice(0, 8)}...
              </span>
              <span
                className="batchStatus"
                style={{ color: getStatusColor(currentBatch.status) }}
              >
                {getStatusIcon(currentBatch.status)} {currentBatch.status}
              </span>
            </div>

            <div className="batchProgress">
              <div className="progressInfo">
                <span>
                  Progresso: {currentBatch.processed_files}/
                  {currentBatch.total_files}
                </span>
                <span>{currentBatch.progress_percentage.toFixed(1)}%</span>
              </div>
              <div className="progressBar">
                <div
                  className="progressFill"
                  style={{ width: `${currentBatch.progress_percentage}%` }}
                ></div>
              </div>
            </div>

            {currentBatch.failed_files > 0 && (
              <div className="failedFiles">
                ⚠️ {currentBatch.failed_files} arquivos falharam
              </div>
            )}

            {currentBatch.status === "completed" && (
              <button
                className="downloadButton"
                onClick={() => downloadBatchResult(currentBatch.batch_id)}
              >
                📥 Baixar Resultado
              </button>
            )}
          </div>
        </div>
      )}

      {/* Previous Batch Jobs */}
      {batchJobs.length > 0 && (
        <div className="batchHistorySection">
          <h2>Histórico de Lotes</h2>
          <div className="batchList">
            {batchJobs.map((job) => (
              <div key={job.batch_id} className="batchCard">
                <div className="batchHeader">
                  <span className="batchId">
                    ID: {job.batch_id.slice(0, 8)}...
                  </span>
                  <span
                    className="batchStatus"
                    style={{ color: getStatusColor(job.status) }}
                  >
                    {getStatusIcon(job.status)} {job.status}
                  </span>
                </div>

                <div className="batchInfo">
                  <span>Arquivos: {job.total_files}</span>
                  <span>Processados: {job.processed_files}</span>
                  {job.failed_files > 0 && (
                    <span>Falhas: {job.failed_files}</span>
                  )}
                </div>

                <div className="batchDate">
                  Criado: {new Date(job.created_at).toLocaleString("pt-BR")}
                </div>

                {job.status === "completed" && (
                  <button
                    className="downloadButton"
                    onClick={() => downloadBatchResult(job.batch_id)}
                  >
                    📥 Baixar
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      {message && (
        <div
          className={`messageArea ${
            message.includes("Erro") || message.includes("❌")
              ? "error"
              : "success"
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
};

export default BatchUploadPage;
