import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import Login from "./pages/Login";
import AdsList from "./pages/AdsList";
import AdDetails from "./pages/AdDetails";
import Profile from "./pages/Profile";
import CreateAd from "./pages/CreateAd";

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
      <header>
        {user ? <p>Привет, {user.username} (ID: {user.id})</p> : <p>Гость</p>}
      </header>
       <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<AdsList />} />
        <Route path="/ads/:id" element={<AdDetails />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/create" element={<CreateAd />} />
      </Routes>
    </Router>
    </div>
  );
}

export default App;
