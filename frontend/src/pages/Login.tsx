import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/auth/login", new URLSearchParams({
        username,
        password
      }), {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("token", res.data.access_token);
      navigate("/");
    } catch (err) {
      alert("Ошибка входа");
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Вход</h2>
      <input placeholder="Логин" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input placeholder="Пароль" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Войти</button>
    </form>
  );
};

export default Login;
