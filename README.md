# 🧑‍🍳 Cookpilot

**Ton assistant IA de cuisine** : entre les ingrédients que tu as dans ton frigo, et Cookpilot te génère une recette complète, claire et appétissante 🍝

---

## 🚀 Fonctionnalités

- 🔍 Génère une recette à partir d'ingrédients
- 📜 Historique des recettes générées
- 🧹 Suppression de recettes
- 🧠 Possibilité de choisir un style de cuisine (à venir)
- 🤖 Génération par OpenAI (à venir)

---

## 🛠️ Stack technique

### Backend

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Poetry** pour la gestion d’environnement

### Frontend (à venir)

- **React + Vite** (ou Create React App)
- **TailwindCSS** pour le style

---

## 📦 Installation backend (FastAPI)

```bash
# Cloner le repo
git clone git@github.com:Yacinekouhli/Cookpilot.git
cd Cookpilot

# Installer les dépendances Python
poetry install

# Lancer le shell virtuel
poetry shell

# Lancer le serveur
uvicorn app.main:app --reload
