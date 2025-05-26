import { Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import Login from "./pages/Login";
import AdsList from "./pages/AdsList";
import AdDetails from "./pages/AdDetails";
import Profile from "./pages/Profile";
import CreateAd from "./pages/CreateAd";
import Home from "./pages/Home";

function App() {
  const [user, setUser] = useState<{ id: string; username: string } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    fetch("http://localhost:8000/users/me", {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    })
      .then(res => {
        if (!res.ok) throw new Error("Unauthorized");
        return res.json();
      })
      .then(data => setUser(data))
      .catch(() => setUser(null));
  }, []);

  return (
    <div>
      <header className="p-4 bg-gray-100 flex justify-between items-center">
        {user ? <p>{user.username}</p> : <p>Гость</p>}
        <nav className="flex gap-4">
          <Link to="/" className="text-blue-600 hover:underline">#</Link>
          <Link to="/home" className="text-blue-600 hover:underline">Home</Link>
          <Link to="/ads" className="text-blue-600 hover:underline">Все объявления</Link>
          <Link to="/create" className="text-green-600 hover:underline">Создать</Link>
          <Link to="/login" className="text-blue-600 hover:underline">Войти</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/ads" element={<AdsList />} />
        <Route path="/ads/:id" element={<AdDetails />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/create" element={<CreateAd />} />
      </Routes>
    </div>
  );
}

export default App;
