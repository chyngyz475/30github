// src/types/ad.ts
export interface Ad {
    id: string;
    title: string;
    brand: string;
    condition: "new" | "used";
    price: number;
    description: string;
    sellerUsername: string;
  }