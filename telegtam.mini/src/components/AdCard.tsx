// src/components/AdCard.tsx
import React from "react";
import { Ad } from "../types/ad";
import { useTelegram } from "../hooks/useTelegram";

interface AdCardProps {
  ad: Ad;
}

export const AdCard: React.FC<AdCardProps> = ({ ad }) => {
  const { openTelegramLink } = useTelegram();

  return (
    <div className="ad-item">
      <strong>{ad.title} ({ad.condition})</strong><br />
      Цена: {ad.price} USD<br />
      {ad.description}<br />
      <button className="contact-btn" onClick={() => openTelegramLink(ad.sellerUsername)}>
        Связаться с продавцом
      </button>
    </div>
  );
};