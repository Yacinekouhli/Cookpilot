import React, { useState, useEffect } from "react";

function App() {
  const [ingredients, setIngredients] = useState("");
  const [style, setStyle] = useState("");
  const [recipe, setRecipe] = useState(null);
  const [recipes, setRecipes] = useState([]);

  const fetchRecipes = async () => {
    const res = await fetch("http://localhost:8000/recipes");
    const data = await res.json();
    setRecipes(data);
  };

  useEffect(() => {
    fetchRecipes();
  }, []);

  const handleGenerate = async () => {
    const res = await fetch("http://localhost:8000/generate-recipe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients, style }),
    });

    const data = await res.json();
    setRecipe(data);
    fetchRecipes();
  };

  const handleDelete = async (id) => {
    await fetch(`http://localhost:8000/recipes/${id}`, {
      method: "DELETE",
    });
    fetchRecipes();
  };

  return (
    <div className="min-h-screen bg-light px-4 py-8">
      <div className="flex items-center justify-center space-x-4 mb-8">
  <img src="/logo.png" alt="logo" className="w-12 h-12" />
  <h1 className="text-3xl font-bold text-dark">Cookpilot</h1>
</div>

      <div className="max-w-xl mx-auto bg-white shadow-lg rounded-xl p-6 mb-8 space-y-4">
        <label className="block">
          <span className="text-gray-700 font-semibold">Ingrédients :</span>
          <input
            type="text"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
            placeholder="pâtes, tomates, ail..."
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}
          />
        </label>

        <label className="block">
          <span className="text-gray-700 font-semibold">Style de cuisine (optionnel) :</span>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
          >
            <option value="">-- Choisir un style --</option>
            <option value="italienne">Italienne</option>
            <option value="healthy">Healthy</option>
            <option value="rapide">Rapide</option>
            <option value="traditionnelle">Traditionnelle</option>
          </select>
        </label>

        <button
          onClick={handleGenerate}
          className="w-full bg-primary text-white font-semibold py-2 px-4 rounded-md hover:bg-emerald-600"
        >
          Générer une recette
        </button>
      </div>

      {recipe && (
        <div className="max-w-xl mx-auto bg-white shadow-md rounded-xl p-6 mb-8 border border-primary">
          <h2 className="text-xl font-bold text-primary mb-2">{recipe.generated_name}</h2>
          <p><strong>Ingrédients :</strong> {recipe.ingredients}</p>
          <p className="mt-2 whitespace-pre-line"><strong>Étapes :</strong> {recipe.steps}</p>
        </div>
      )}

      <div className="max-w-3xl mx-auto">
        <h3 className="text-xl font-bold text-dark mb-4">📜 Historique des recettes :</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {recipes.map((r) => (
            <div key={r.id} className="bg-white shadow rounded-lg p-4 border border-gray-200 relative">
              <h4 className="text-lg font-semibold text-primary mb-1">{r.generated_name}</h4>
              <p className="text-sm text-gray-500 mb-1"><strong>Style :</strong> {r.style || "—"}</p>
              <p className="text-sm text-gray-600 mb-2"><strong>Ingrédients :</strong> {r.ingredients}</p>
              <p className="text-sm text-gray-700 whitespace-pre-line">{r.steps}</p>
              <button
                onClick={() => handleDelete(r.id)}
                className="absolute top-2 right-2 text-red-500 hover:text-red-700"
              >
                ✖
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
