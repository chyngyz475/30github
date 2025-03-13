// src/hooks/useTelegram.ts
import { useEffect } from "react";

export const useTelegram = () => {
const tg = (window as any).Telegram?.WebApp;
  useEffect(() => {
    if (tg) {
      tg.ready();
      tg.MainButton.setText("Показать все").show();
    }
  }, [tg]);

  const updateTheme = () => {
    if (tg) {
      const themeParams = tg.themeParams;
      document.body.style.backgroundColor = themeParams.bg_color || "#f0f0f0";
      document.documentElement.style.color = themeParams.text_color || "#333";
    }
  };

  useEffect(() => {
    if (tg) {
      updateTheme();
      tg.onEvent("themeChanged", updateTheme);
    }
  }, [tg]);

  const close = () => tg?.close();
  const openTelegramLink = (username: string) => tg?.openTelegramLink(`https://t.me/${username}`);

  return { tg, close, openTelegramLink, user: tg?.initDataUnsafe?.user };
};