import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CreateAd() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState<number | "">("");
  const [categoryId, setCategoryId] = useState<number | "">("");
  const [isPriceNegotiable, setIsPriceNegotiable] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
      if (!title || !description || !price || !categoryId) {
        alert("Заполни все поля!");
        return;
      }
      setLoading(true);

      const token = localStorage.getItem("token");
      if (!token) {
        alert("Пользователь не авторизован");
        setLoading(false);
        return;
      }

      try {
        const res = await fetch("http://localhost:8000/advertisement", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify({
            title,
            description,
            price: Number(price),
            is_price_negotiable: isPriceNegotiable,
            category_id: Number(categoryId),
          }),
        });

        if (!res.ok) throw new Error("Ошибка создания объявления");
        const newAd = await res.json();

        if (file) {
          const formData = new FormData();
          formData.append("file", file);

          const uploadRes = await fetch(`http://localhost:8000/advertisement/${newAd.id}/upload-image`, {
            method: "POST",
            body: formData,
          });

          if (!uploadRes.ok) throw new Error("Ошибка загрузки изображения");
        }

        alert("Объявление создано!");
        navigate(`/ads/${newAd.id}`);
      } catch (e) {
        alert((e as Error).message);
      } finally {
        setLoading(false);
      }
    };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-3xl mb-6">Создать объявление</h1>

      <input
        type="text"
        placeholder="Название"
        className="border p-2 mb-4 w-full"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        disabled={loading}
      />

      <textarea
        placeholder="Описание"
        className="border p-2 mb-4 w-full"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={loading}
      />

      <input
        type="number"
        placeholder="Цена"
        className="border p-2 mb-4 w-full"
        value={price}
        onChange={(e) => setPrice(e.target.value === "" ? "" : Number(e.target.value))}
        disabled={loading}
      />

        <label>
          <input
            type="checkbox"
            checked={isPriceNegotiable}
            onChange={(e) => setIsPriceNegotiable(e.target.checked)}
            disabled={loading}
          />
          Цена обсуждается
        </label>

      <input
        type="number"
        placeholder="ID категории"
        className="border p-2 mb-4 w-full"
        value={categoryId}
        onChange={(e) => setCategoryId(e.target.value === "" ? "" : Number(e.target.value))}
        disabled={loading}
      />

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
        disabled={loading}
        className="mb-4"
      />

      <button
        onClick={submit}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? "Создаём..." : "Создать объявление"}
      </button>
    </div>
  );
}
