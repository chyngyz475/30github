// src/components/AdList.tsx
import React, { useEffect, useState } from "react";
import { Ad } from "../types/ad";
import { fetchAds, filterAds } from "../services/firebase";
import { AdCard } from "./AdCard";

interface AdListProps {
  filter: { brand: string; condition: string; minPrice: number; maxPrice: number };
}

export const AdList: React.FC<AdListProps> = ({ filter }) => {
  const [ads, setAds] = useState<Ad[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAds = async () => {
      setLoading(true);
      const filteredAds = await filterAds(filter.brand, filter.condition, filter.minPrice, filter.maxPrice);
      setAds(filteredAds);
      setLoading(false);
    };
    loadAds();
  }, [filter]);

  if (loading) return <div>Загрузка...</div>;
  return (
    <div className="ad-list">
      {ads.length === 0 ? (
        <div className="no-ads">Нет доступных объявлений. Попробуйте позже.</div>
      ) : (
        ads.map((ad) => <AdCard key={ad.id} ad={ad} />)
      )}
    </div>
  );
};