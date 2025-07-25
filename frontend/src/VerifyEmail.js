// src/VerifyEmail.jsx
import React, { useEffect, useState } from "react";

export default function VerifyEmail() {
  const [status, setStatus] = useState("loading"); // loading | success | error
  const [message, setMessage] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (!token) {
      setStatus("error");
      setMessage("❌ Token manquant.");
      return;
    }

    const verify = async () => {
      try {
        const res = await fetch(`http://localhost:8000/auth/verify-email?token=${token}`);
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Erreur de vérification");
        }

        setStatus("success");
        setMessage(data.message || "Email vérifié !");
      } catch (err) {
        setStatus("error");
        setMessage(err.message);
      }
    };

    verify();
  }, []);

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-md rounded">
      {status === "loading" && <p className="text-gray-600">Vérification en cours...</p>}
      {status === "success" && (
        <div className="text-green-600 font-semibold">
          ✅ {message}
          <p className="mt-2">Vous pouvez maintenant vous connecter.</p>
        </div>
      )}
      {status === "error" && (
        <div className="text-red-600 font-semibold">
          ❌ {message}
          <p className="mt-2">Si le lien ne fonctionne plus, recommencez l’inscription.</p>
        </div>
      )}
    </div>
  );
}
