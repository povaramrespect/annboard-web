import { useState } from "react";

export default function ImageUpload({
  adId,
  onUploaded,
}: {
  adId: string;
  onUploaded: () => void;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) return alert("Выберите файл");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`http://localhost:8000/advertisement/${adId}/upload-image`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Ошибка загрузки");

      setFile(null);
      onUploaded();
    } catch (err) {
      alert("Не удалось загрузить файл");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
        disabled={loading}
      />
      <button onClick={upload} disabled={loading} className="ml-2 px-3 py-1 bg-blue-600 text-white rounded">
        {loading ? "Загрузка..." : "Загрузить"}
      </button>
    </div>
  );
}
