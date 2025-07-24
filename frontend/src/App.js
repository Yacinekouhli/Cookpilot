import React, { useState, useEffect } from 'react';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [style, setStyle] = useState('classique');
  const [recipe, setRecipe] = useState(null);
  const [allRecipes, setAllRecipes] = useState([]);

  // Charger toutes les recettes à l'initialisation
  useEffect(() => {
    fetch("http://localhost:8000/recipes")
      .then((res) => res.json())
      .then((data) => setAllRecipes(data))
      .catch((err) => console.error("Erreur lors du chargement :", err));
  }, []);

  // Générer une nouvelle recette
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/generate-recipe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ingredients,
          style,
        }),
      });

      const data = await response.json();
      setRecipe(data);
      setAllRecipes((prev) => [...prev, data]);
    } catch (error) {
      console.error("Erreur de génération :", error);
    }
  };

  // Supprimer une recette
  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/recipes/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setAllRecipes((prev) => prev.filter((r) => r.id !== id));
      } else {
        console.error("Erreur lors de la suppression");
      }
    } catch (error) {
      console.error("Erreur réseau :", error);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>🍝 Cookpilot</h1>
      <p>Entre tes ingrédients et choisis un style de cuisine :</p>

      {/* Formulaire */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ex : pâtes, ail, tomates"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          style={{ width: '300px', padding: '0.5rem' }}
        />

        <select
          value={style}
          onChange={(e) => setStyle(e.target.value)}
          style={{ marginLeft: '1rem', padding: '0.5rem' }}
        >
          <option value="classique">Classique</option>
          <option value="italien">Italien</option>
          <option value="rapide">Rapide</option>
          <option value="healthy">Healthy</option>
          <option value="vegan">Vegan</option>
          <option value="gourmand">Gourmand</option>
        </select>

        <button
          type="submit"
          style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}
        >
          Générer
        </button>
      </form>

      {/* Affichage de la recette générée */}
      {recipe && (
        <div style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #ccc' }}>
          <h2>{recipe.generated_name}</h2>
          <p><strong>Ingrédients :</strong> {recipe.ingredients}</p>
          <p><strong>Style :</strong> {recipe.style}</p>
          <p><strong>Préparation :</strong></p>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{recipe.steps}</pre>
        </div>
      )}

      {/* Historique */}
      <div style={{ marginTop: '3rem' }}>
        <h2>📜 Historique des recettes</h2>
        <ul>
          {allRecipes.map((r) => (
            <li key={r.id} style={{ marginBottom: '0.5rem' }}>
              <strong>{r.generated_name}</strong> — {r.ingredients}
              <button
                onClick={() => handleDelete(r.id)}
                style={{
                  marginLeft: '1rem',
                  backgroundColor: '#f44336',
                  color: 'white',
                  border: 'none',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                🗑️ Supprimer
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
