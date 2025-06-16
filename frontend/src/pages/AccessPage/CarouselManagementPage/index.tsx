import React, { useState, useEffect, useCallback } from "react";
import "./CarouselManagementPage.css";
import { BASE_URL } from "../../../config/apiConfig";

interface CarouselImage {
  id: number;
  filename: string;
  isActive: boolean;
}

const CarouselManagementPage: React.FC = () => {
  const [images, setImages] = useState<CarouselImage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [reorderingImageId, setReorderingImageId] = useState<number | null>(
    null
  );
  const [totalSlotsToShow, setTotalSlotsToShow] = useState(6);

  const getCurrentImagesCount = useCallback(() => {
    return images.filter((img) => img.filename && img.filename.length > 0)
      .length;
  }, [images]);

  const getMinSlots = useCallback(() => {
    return Math.max(getCurrentImagesCount(), 1);
  }, [getCurrentImagesCount]);
  const getMaxSlots = useCallback(() => {
    return 12;
  }, []);
  useEffect(() => {
    loadCarouselImages();
  }, []);
  useEffect(() => {
    if (images.length > 0) {
      const currentImagesCount = getCurrentImagesCount();
      if (totalSlotsToShow < currentImagesCount) {
        setTotalSlotsToShow(currentImagesCount);
      }
    }
  }, [images, totalSlotsToShow, getCurrentImagesCount]);

  const generateSlots = () => {
    const slots = [];
    for (let i = 1; i <= totalSlotsToShow; i++) {
      const existingImage = images.find((img) => img.id === i);
      if (existingImage) {
        slots.push(existingImage);
      } else {
        slots.push({
          id: i,
          filename: "",
          isActive: false,
        });
      }
    }
    return slots;
  };
  const handleSlotCountChange = useCallback(
    (newCount: number) => {
      const minSlots = getMinSlots();
      const maxSlots = getMaxSlots();

      if (newCount >= minSlots && newCount <= maxSlots) {
        setTotalSlotsToShow(newCount);
      }
    },
    [getMinSlots, getMaxSlots]
  );
  const loadCarouselImages = async () => {
    try {
      setIsLoading(true);
      const timestamp = new Date().getTime();
      const response = await fetch(
        `${BASE_URL}/carousel-images?t=${timestamp}`
      );
      if (response.ok) {
        const data = await response.json();
        setImages(data.images || []);
      } else {
        setMessage("Erro ao carregar imagens do carrossel");
      }
    } catch {
      setMessage("Erro ao conectar com o servidor");
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
    imageId: number
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setMessage("Por favor, selecione apenas arquivos de imagem");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setMessage("Imagem muito grande. Máximo 5MB");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);
    formData.append("imageId", imageId.toString());

    try {
      setIsLoading(true);
      const response = await fetch(`${BASE_URL}/upload-carousel-image`, {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        setMessage(`Imagem ${imageId} atualizada com sucesso!`);
        loadCarouselImages();
        window.dispatchEvent(new CustomEvent("carouselUpdated"));
      } else {
        const errorData = await response.json();
        setMessage(errorData.message || "Erro ao fazer upload da imagem");
      }
    } catch {
      setMessage("Erro ao conectar com o servidor");
    } finally {
      setIsLoading(false);
    }
  };

  const toggleImageActive = async (imageId: number, isActive: boolean) => {
    try {
      const response = await fetch(`${BASE_URL}/toggle-carousel-image`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ imageId, isActive }),
      });
      if (response.ok) {
        setMessage(
          `Imagem ${imageId} ${
            isActive ? "ativada" : "desativada"
          } com sucesso!`
        );
        loadCarouselImages();
        window.dispatchEvent(new CustomEvent("carouselUpdated"));
      } else {
        setMessage("Erro ao alterar status da imagem");
      }
    } catch {
      setMessage("Erro ao conectar com o servidor");
    }
  };
  const moveImageUp = async (imageId: number) => {
    const currentIndex = images.findIndex((img) => img.id === imageId);
    if (currentIndex <= 0) return;

    setReorderingImageId(imageId);

    try {
      const targetImage = images[currentIndex - 1];
      await swapImages(imageId, targetImage.id);
    } catch (error) {
      console.error("Erro ao mover imagem para cima:", error);
    } finally {
      setReorderingImageId(null);
    }
  };

  const moveImageDown = async (imageId: number) => {
    const currentIndex = images.findIndex((img) => img.id === imageId);
    if (currentIndex === -1 || currentIndex >= images.length - 1) return;

    setReorderingImageId(imageId);

    try {
      const targetImage = images[currentIndex + 1];
      await swapImages(imageId, targetImage.id);
    } catch (error) {
      console.error("Erro ao mover imagem para baixo:", error);
    } finally {
      setReorderingImageId(null);
    }
  };
  const swapImages = async (sourceId: number, targetId: number) => {
    try {
      console.log(`Reordenando imagens: ${sourceId} ↔ ${targetId}`);

      const response = await fetch(`${BASE_URL}/reorder-carousel-images`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sourceId, targetId }),
      });

      if (response.ok) {
        setMessage("Ordem das imagens atualizada");
        await loadCarouselImages();

        window.dispatchEvent(new CustomEvent("carouselUpdated"));
      } else {
        const errorData = await response.json();
        setMessage(errorData.error || "Erro ao reordenar imagens");
        await loadCarouselImages();
      }
    } catch (error) {
      console.error("Erro ao conectar com o servidor:", error);
      setMessage("Erro ao conectar com o servidor");
      await loadCarouselImages();
    }
  };
  const deleteImage = async (imageId: number) => {
    if (!window.confirm(`Tem certeza que deseja apagar a imagem ${imageId}?`)) {
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/delete-carousel-image`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ imageId }),
      });
      if (response.ok) {
        setMessage(`Imagem ${imageId} apagada com sucesso!`);
        loadCarouselImages();
        window.dispatchEvent(new CustomEvent("carouselUpdated"));
      } else {
        setMessage("Erro ao apagar a imagem");
      }
    } catch {
      setMessage("Erro ao conectar com o servidor");
    }
  };

  return (
    <div className="carouselManagementContainer">
      <div className="carouselManagementHeader">
        <h1>Carrossel</h1>
      </div>{" "}
      <div className="carouselControlsSection">
        <div className="slotCountControl">
          <label htmlFor="slotCount">Quantidade de slots do carrossel:</label>
          <div className="numberInputWrapper">
            <button
              type="button"
              onClick={() => handleSlotCountChange(totalSlotsToShow - 1)}
              disabled={totalSlotsToShow <= getMinSlots()}
              className="numberBtn decrease"
            >
              -
            </button>
            <input
              id="slotCount"
              type="number"
              min={getMinSlots()}
              max={getMaxSlots()}
              value={totalSlotsToShow}
              onChange={(e) =>
                handleSlotCountChange(parseInt(e.target.value) || getMinSlots())
              }
              className="numberInput"
            />
            <button
              type="button"
              onClick={() => handleSlotCountChange(totalSlotsToShow + 1)}
              disabled={totalSlotsToShow >= getMaxSlots()}
              className="numberBtn increase"
            >
              +
            </button>
          </div>
        </div>
      </div>{" "}
      {message && (
        <div
          className={`message ${
            message.includes("Erro") ? "error" : "success"
          }`}
        >
          {message}
          <button onClick={() => setMessage("")}>×</button>
        </div>
      )}
      {isLoading && <div className="loading">Carregando...</div>}
      <div className="carouselGrid">
        {generateSlots().map((imageData, index) => {
          const imageId = imageData.id;
          const hasImage = imageData.filename && imageData.filename.length > 0;
          return (
            <div
              key={imageId}
              className={`carouselItem ${
                imageData?.isActive ? "active" : "inactive"
              } ${reorderingImageId === imageId ? "reordering" : ""} ${
                !hasImage ? "empty-slot" : ""
              }`}
            >
              <div className="carouselItemHeader">
                <div className="slotNumber">Slot {imageId}</div>
                {hasImage && (
                  <>
                    <div className="reorderControls">
                      <button
                        onClick={() => moveImageUp(imageId)}
                        disabled={index === 0 || reorderingImageId === imageId}
                        className="reorderBtn up"
                        title="Mover para cima"
                      >
                        {reorderingImageId === imageId ? "⏳" : "↑"}
                      </button>
                      <button
                        onClick={() => moveImageDown(imageId)}
                        disabled={
                          index === generateSlots().length - 1 ||
                          reorderingImageId === imageId
                        }
                        className="reorderBtn down"
                        title="Mover para baixo"
                      >
                        {reorderingImageId === imageId ? "⏳" : "↓"}
                      </button>
                    </div>
                    <label className="toggleSwitch">
                      <input
                        type="checkbox"
                        checked={imageData?.isActive || false}
                        onChange={(e) =>
                          toggleImageActive(imageId, e.target.checked)
                        }
                      />
                      <span className="slider"></span>
                    </label>
                  </>
                )}
              </div>
              <div className="imagePreview">
                {" "}
                {hasImage ? (
                  <img
                    key={`img-${imageId}-${imageData.filename}`}
                    src={`${BASE_URL}/carousel-image/${
                      imageData.filename
                    }?v=${Date.now()}`}
                    alt={`Carrossel ${imageId}`}
                    onError={(e) => {
                      (e.target as HTMLImageElement).src =
                        "/placeholder-image.svg";
                    }}
                  />
                ) : (
                  <div className="noImage">
                    <span>🖼️</span>
                    <span>Slot disponível</span>
                    <span>Adicione uma imagem</span>{" "}
                  </div>
                )}
              </div>
              <div className="imageControls">
                <div className="fileInputWrapper">
                  <input
                    type="file"
                    id={`image-${imageId}`}
                    accept="image/*"
                    onChange={(e) => handleImageUpload(e, imageId)}
                    className="fileInput"
                  />
                  <label
                    htmlFor={`image-${imageId}`}
                    className="fileInputLabel"
                  >
                    {hasImage ? "Alterar Imagem" : "Adicionar Imagem"}
                  </label>
                </div>

                {hasImage && (
                  <button
                    onClick={() => deleteImage(imageId)}
                    className="deleteButton"
                    title="Apagar imagem"
                  >
                    Apagar
                  </button>
                )}
              </div>{" "}
            </div>
          );
        })}
      </div>
      <div className="instructions">
        <h3>Instruções:</h3>
        <ul>
          <li>
            Use o controle numérico acima para ajustar quantos slots de imagem
            mostrar (mínimo: quantidade atual, máximo: 12)
          </li>
          <li>
            Slots vazios aparecem quando você aumenta a quantidade - adicione
            imagens neles
          </li>
          <li>Use os botões ↑ e ↓ para reordenar as imagens existentes</li>
          <li>
            Use o botão de ativação para mostrar/ocultar imagens do carrossel
          </li>
          <li>
            Apenas imagens ativas aparecerão no carrossel da página inicial
          </li>
          <li>Use o botão "Apagar" para remover uma imagem permanentemente</li>
          <li>Formatos aceitos: JPG, PNG, GIF (máximo 5MB)</li>
          <li>
            Recomendação: imagens com proporção 16:9 para melhor visualização
          </li>
        </ul>
      </div>
    </div>
  );
};

export default CarouselManagementPage;
