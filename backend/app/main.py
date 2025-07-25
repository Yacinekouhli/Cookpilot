from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Recipe, User
from app.schemas import RecipeRequest, RecipeOut, UserCreate
from app.openai_client import generate_fake_recipe
from app.database import SessionLocal, get_db
from app.auth import hash_password, get_current_user
from app.auth_routes import router as auth_router
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autorise le frontend React en dev
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # en dev tu peux mettre ["*"] si tu veux aller vite
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, DELETE, OPTIONS, ...
    allow_headers=["*"],          # Content-Type, Authorization, ...
)

app.include_router(auth_router)


@app.post("/generate-recipe", response_model=RecipeOut)
def generate_recipe(
    request: RecipeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 protection par token
):
    response = generate_fake_recipe(request)

    recipe = Recipe(
                ingredients=request.ingredients,
                generated_name=response.generated_name,
                steps=response.steps,
                style=request.style,
                user_id=current_user.id
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe


@app.get("/recipes", response_model=List[RecipeOut])
def list_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 seulement si connecté
):
    recipes = db.query(Recipe).filter(Recipe.user_id == current_user.id).all()
    return recipes


@app.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recette non trouvée")

    return recipe


@app.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == current_user.id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recette non trouvée")

    db.delete(recipe)
    db.commit()

    return {"message": f"Recette avec l'ID {recipe_id} supprimée avec succès."}
