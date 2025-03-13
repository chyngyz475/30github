import { useState } from "react";
import './App.css';
import { AdFilters } from "./components/AdFilters";
import { AdList } from "./components/AdList";
import { useTelegram } from "./hooks/useTelegram";
import "./styles/App.css";


const [filter, setFilter] = useState({ brand: "", condition: "", minPrice: 0, maxPrice: Infinity });
  const { tg, close, user } = useTelegram();

  const handleFilter = (brand: string, condition: string, minPrice: number, maxPrice: number) => {
    setFilter({ brand, condition, minPrice, maxPrice });
    if (tg) tg.MainButton.hide();
  };

  const handleShowAll = () => {
    setFilter({ brand: "", condition: "", minPrice: 0, maxPrice: Infinity });
    if (tg) tg.MainButton.hide();
  };

  if (tg) {
    tg.MainButton.setText("Показать все").onClick(handleShowAll);
    if (filter.brand || filter.condition || filter.minPrice || filter.maxPrice !== Infinity) {
      tg.MainButton.show();
    }
  }

function App() {
  return (
    <div className="app">
      {user && <h2>Привет, {user.first_name}! Добро пожаловать в приложение объявлений.</h2>}
      <AdFilters onFilter={handleFilter} />
      <AdList filter={filter} />
      <button id="backButton" onClick={close}>
        Назад
      </button>
    </div>
  );
};


export default App;
