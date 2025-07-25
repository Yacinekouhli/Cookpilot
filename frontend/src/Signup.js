import React, { useState } from "react";

function Signup({ onSignup, switchToLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSignup = async () => {
    try {
      const res = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erreur lors de l'inscription");
      }

      setError("");
      onSignup(); // Retour à l'écran de login
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-20 bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-bold mb-4 text-center">Créer un compte</h2>
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
        onClick={handleSignup}
        className="bg-primary text-white w-full py-2 rounded hover:bg-emerald-600"
      >
        S'inscrire
      </button>
      <p className="mt-4 text-sm text-center">
        Déjà un compte ?{" "}
        <button onClick={switchToLogin} className="text-primary underline">
          Se connecter
        </button>
      </p>
    </div>
  );
}

export default Signup;
