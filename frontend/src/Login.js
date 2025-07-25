import React, { useState } from "react";

function Login({ onLogin, switchToSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erreur lors de la connexion");
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      onLogin();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-20 bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-bold mb-4 text-center">Connexion</h2>
      <input
        type="email"
        placeholder="Email"
        className="block w-full mb-3 p-2 border rounded"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Mot de passe"
        className="block w-full mb-4 p-2 border rounded"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {error && <p className="text-red-500 mb-3">{error}</p>}
      <button
        onClick={handleLogin}
        className="bg-primary text-white w-full py-2 rounded hover:bg-emerald-600"
      >
        Se connecter
      </button>
      <p className="mt-4 text-sm text-center">
        Pas encore de compte ?{" "}
        <button onClick={switchToSignup} className="text-primary underline">
          S'inscrire
        </button>
      </p>
    </div>
  );
}

export default Login;
