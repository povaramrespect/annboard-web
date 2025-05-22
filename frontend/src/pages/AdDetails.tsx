import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

type CategoryWithParents = {
  id: number;
  name: string;
  parents: { id: number; name: string }[];
};

type AdDetails = {
  id: string;
  title: string;
  description: string;
  price: number;
  created_at: string;
  updated_at: string | null;
  owner: {
    id: string;
    username: string;
    email?: string;
    phone?: string;
  };
  categories: CategoryWithParents;
  values: {
    id: number;
    field_id: number;
    name: string;
    value: string;
    property: {
      id: number;
      name: string;
    };
  }[];
};

export default function AdDetailsPage() {
  const { id } = useParams();
  const [ad, setAd] = useState<AdDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/advertisement/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setAd(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="p-6">Загрузка...</p>;
  if (!ad) return <p className="p-6">Объявление не найдено</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">{ad.title}</h1>
      <p className="text-lg mb-2">Цена: {ad.price} ₽</p>
      <p className="mb-4">{ad.description}</p>

      <h2 className="font-semibold">Категория:</h2>
      <p className="mb-4">
        {[...(ad.categories?.parents ?? []).map(p => p.name), ad.categories.name].join(" > ")}
      </p>

      <h2 className="font-semibold">Характеристики:</h2>
      <ul className="mb-4 list-disc list-inside">
        {ad.values.map((v) => (
          <li key={v.id}>
            {v.property?.name || v.name}: {v.value}
          </li>
        ))}
      </ul>

      <h2 className="font-semibold">Продавец:</h2>
      <p className="mb-1">Имя: {ad.owner.username || ad.owner.email}</p>
      {ad.owner.phone && <p className="mb-1">Телефон: {ad.owner.phone}</p>}
    </div>
  );
}
