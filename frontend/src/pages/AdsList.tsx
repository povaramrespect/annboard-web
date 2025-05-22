import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

type Ad = {
  id: number;
  title: string;
  price: number;
};

export default function AdsList() {
  const [ads, setAds] = useState<Ad[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/advertisements")
      .then((res) => res.json())
      .then((data) => {
        console.log("data from server:", data);
        setAds(data);
      })
      .catch(() => setAds([]));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl mb-6">Объявления</h1>
      {ads.length === 0 ? (
        <p>Нет объявлений</p>
      ) : (
        <ul className="space-y-3">
          {ads.map((ad) => (
            <li key={ad.id} className="border p-4 rounded hover:shadow-md">
              <Link to={`/ads/${ad.id}`} className="font-semibold text-blue-600 hover:underline">
                {ad.title}
              </Link>
              <p>Цена: {ad.price} ₽</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
