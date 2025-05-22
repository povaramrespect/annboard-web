import { useEffect, useState } from "react";

type User = {
  id: number;
  name: string;
  email: string;
  photoUrl?: string;
};

export default function Profile() {
  const [user, setUser] = useState<User | null>(null);
  const [name, setName] = useState("");
  const [photo, setPhoto] = useState<File | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/profile")
      .then((res) => res.json())
      .then((data) => {
        setUser(data);
        setName(data.name);
      });
  }, []);

  const handleUpdate = async () => {
    alert("Обновление профиля пока не реализовано)))))");
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-3xl mb-6">Профиль</h1>
      {user && (
        <>
          <img
            src={user.photoUrl || "https://via.placeholder.com/150"}
            alt="Фото профиля"
            className="w-32 h-32 rounded-full mb-4 object-cover"
          />
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full p-2 mb-4 border rounded"
            placeholder="Имя"
          />
          <input
            type="file"
            onChange={(e) => setPhoto(e.target.files?.[0] || null)}
            className="mb-4"
          />
          <button
            onClick={handleUpdate}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Обновить профиль
          </button>
        </>
      )}
    </div>
  );
}
