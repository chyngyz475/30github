// src/services/firebase.ts
import { addDoc, collection, getDocs, query, where } from "firebase/firestore";
import { Ad } from "../types/ad";
import { db } from "../firebase";

export const fetchAds = async (): Promise<Ad[]> => {
  const adsCollection = collection(db, "ads");
  const snapshot = await getDocs(adsCollection);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Ad));
};

export const addAd = async (ad: Omit<Ad, "id">): Promise<void> => {
  const adsCollection = collection(db, "ads");
  await addDoc(adsCollection, ad);
};

export const filterAds = async (brand?: string, condition?: string, minPrice?: number, maxPrice?: number): Promise<Ad[]> => {
  let q = collection(db, "ads");
  if (brand) q = query(q, where("brand", "==", brand));
  if (condition) q = query(q, where("condition", "==", condition));
  if (minPrice || maxPrice) {
    q = query(q, where("price", ">=", minPrice || 0), where("price", "<=", maxPrice || Infinity));
  }
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Ad));
};