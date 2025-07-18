import React, { useState, useEffect, useCallback } from "react";
import "./Carousel.css";
import { BASE_URL } from "../../config/apiConfig";

interface CarouselItem {
  position: number;
  image: string;
  alt: string;
}

interface CarouselImageData {
  id: number;
  filename: string;
  alt: string;
  isActive: boolean;
  exists: boolean;
}

const Carousel = () => {
  const [carouselItems, setCarouselItems] = useState<CarouselItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const setDefaultImages = useCallback(() => {
    setCarouselItems([
      {
        position: 1,
        image: `${BASE_URL}/carousel-image/carrousel1.jpg`,
        alt: "Carrossel 1",
      },
      {
        position: 2,
        image: `${BASE_URL}/carousel-image/carrousel2.jpg`,
        alt: "Carrossel 2",
      },
      {
        position: 3,
        image: `${BASE_URL}/carousel-image/carrousel3.jpg`,
        alt: "Carrossel 3",
      },
      {
        position: 4,
        image: `${BASE_URL}/carousel-image/carrousel4.jpg`,
        alt: "Carrossel 4",
      },
      {
        position: 5,
        image: `${BASE_URL}/carousel-image/carrousel5.jpg`,
        alt: "Carrossel 5",
      },
      {
        position: 6,
        image: `${BASE_URL}/carousel-image/carrousel6.jpg`,
        alt: "Carrossel 6",
      },
    ]);
  }, []);

  const loadCarouselImages = useCallback(async () => {
    try {
      const timestamp = new Date().getTime();
      const response = await fetch(
        `${BASE_URL}/carousel-images?t=${timestamp}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          cache: "no-cache",
        }
      );

      if (response.ok) {
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          const data = await response.json();
          const activeImages = data.images
            .filter((img: CarouselImageData) => img.isActive && img.exists)
            .map((img: CarouselImageData, index: number) => ({
              position: index + 1,
              image: `${BASE_URL}/carousel-image/${img.filename}?t=${timestamp}`,
              alt: img.alt || `Carrossel ${img.id}`,
            }));

          setCarouselItems(activeImages);
        } else {
          console.warn("Response is not JSON, using defaults");
          setDefaultImages();
        }
      } else {
        console.warn("Failed to load carousel images from API, using defaults");
        setDefaultImages();
      }
    } catch (error) {
      console.error("Error loading carousel images:", error);
      setDefaultImages();
    } finally {
      setIsLoading(false);
    }
  }, [setDefaultImages]);

  useEffect(() => {
    loadCarouselImages();
  }, [loadCarouselImages]);

  useEffect(() => {
    const handleCarouselUpdate = () => {
      loadCarouselImages();
    };
    window.addEventListener("carouselUpdated", handleCarouselUpdate);
    return () =>
      window.removeEventListener("carouselUpdated", handleCarouselUpdate);  }, [loadCarouselImages]);

  if (isLoading) {
    return (
      <div className="carouselContainer">
        <div className="carousel-loading">
          <p>Carregando carrossel...</p>
        </div>
      </div>
    );
  }

  if (carouselItems.length === 0) {
    return null;
  }
  return (
    <div className="carouselContainer">
      <div
        className="slider"
        style={
          {
            "--quantity": carouselItems.length,
          } as React.CSSProperties
        }
      >
        {" "}
        <div className="list">
          {carouselItems.map((item) => (
            <div
              key={`carousel-first-${item.position}`}
              className="item"
              style={{ "--position": item.position } as React.CSSProperties}
            >
              <div className="card">
                <img
                  src={item.image}
                  alt={item.alt}
                  className="carouselImage"
                  loading="lazy"
                />
              </div>
            </div>
          ))}
          {carouselItems.map((item) => (
            <div
              key={`carousel-second-${item.position}`}
              className="item"
              style={{ "--position": item.position } as React.CSSProperties}
            >
              <div className="card">
                <img
                  src={item.image}
                  alt={item.alt}
                  className="carouselImage"
                  loading="lazy"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Carousel;
