import { useEffect, useState } from 'react';

export default function Home() {
  const [status, setStatus] = useState('loading');

  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus('error'));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-xl font-bold">AnnBoard</h1>
      </header>
      <main className="flex-grow p-6">
        <h2 className="text-2xl mb-4">Добро пожаловать в AnnBoard</h2>
        <p>Status API: {status}</p>
      </main>
      <footer className="bg-gray-200 text-center p-4">
        © 2025 AnnBoard. All rights reserved.
      </footer>
    </div>
  );
}
