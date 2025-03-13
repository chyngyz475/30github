// src/components/AdFilters.tsx
import React, { useState } from "react";

interface AdFiltersProps {
  onFilter: (brand: string, condition: string, minPrice: number, maxPrice: number) => void;
}

export const AdFilters: React.FC<AdFiltersProps> = ({ onFilter }) => {
  const [brand, setBrand] = useState("");
  const [condition, setCondition] = useState("");
  const [minPrice, setMinPrice] = useState<number | "">("");
  const [maxPrice, setMaxPrice] = useState<number | "">("");

  const handleFilter = () => {
    onFilter(brand, condition, minPrice as number, maxPrice as number);
  };

  return (
    <div className="filters">
      <select value={brand} onChange={(e) => setBrand(e.target.value)}>
        <option value="">Все бренды</option>
        <option value="Apple">Apple</option>
        <option value="Samsung">Samsung</option>
        <option value="Xiaomi">Xiaomi</option>
      </select>
      <select value={condition} onChange={(e) => setCondition(e.target.value)}>
        <option value="">Все состояния</option>
        <option value="new">Новый</option>
        <option value="used">Б/У</option>
      </select>
      <input
        type="number"
        placeholder="Мин. цена (USD)"
        value={minPrice}
        onChange={(e) => setMinPrice(e.target.value ? parseInt(e.target.value) : "")}
      />
      <input
        type="number"
        placeholder="Макс. цена (USD)"
        value={maxPrice}
        onChange={(e) => setMaxPrice(e.target.value ? parseInt(e.target.value) : "")}
      />
      <button onClick={handleFilter}>Фильтровать</button>
    </div>
  );
};