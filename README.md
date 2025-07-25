# 👨‍🍳 Cookpilot

**Cookpilot** is a full-stack web application that helps you generate delicious cooking recipes based on the ingredients you already have at home — powered by Artificial Intelligence ✨

---

## 🚀 Features

* 🧠 Generate unique recipes from a list of ingredients
* 🎨 Choose your cooking style: gourmet, healthy, quick, traditional, etc.
* 📜 View your personal recipe history
* 🗑️ Delete saved recipes easily
* 🔐 Secure authentication system (signup/login with JWT)
* 🌈 Clean and responsive UI using Tailwind CSS
* 🤖 AI-powered recipe generation via OpenAI API (fully integrated)

---

## 🧱 Tech Stack

### Backend – [FastAPI](https://fastapi.tiangolo.com/)

* Python 3.11
* FastAPI framework
* SQLAlchemy + SQLite
* JWT-based auth
* OpenAI API integration
* Pydantic models & validation

### Frontend – [React](https://reactjs.org/)

* React (Create React App)
* Tailwind CSS for styling
* Fetch API with async/await
* Component-based structure

---

## 📂 Project Structure (simplified)

```bash
cookpilot/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── openai_client.py   # OpenAI interaction
│   │   ├── auth.py            # Auth logic (JWT, hash, etc.)
│   │   └── ...
│   ├── .env                   # Environment variables (not committed)
│   └── ...
├── frontend/
│   └── ...                    # React app (CRA)
```

---

## 🔐 Environment Variables

To use the OpenAI API, create a `.env` file in your `backend/` folder:

```env
OPENAI_API_KEY=sk-your-openai-key-here
```

⚠️ **Never commit your real key.**
A `.env.example` file is provided as a reference.

---

## 🛠️ Setup Instructions

### 1. Backend (FastAPI)

```bash
cd backend
poetry install  # or pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`, backend on `http://localhost:8000`.

---

## 🧪 Coming soon

* ✅ Image generation with DALL·E
* ✅ Recipe favorites (likes)
* ✅ Nutrition and calorie estimation
* ✅ Variant generation (vegetarian, quick version…)

---

## 🤝 Contributing

Feel free to open issues, forks, or pull requests.
Ideas, feedback, and stars ⭐ are always welcome!

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---
