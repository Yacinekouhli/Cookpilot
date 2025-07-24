from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import Recipe
from app.schemas import RecipeRequest, RecipeResponse, RecipeOut
from app.openai_client import generate_fake_recipe
from app.database import SessionLocal
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/generate-recipe", response_model=RecipeOut)
def generate_recipe(request: RecipeRequest, db: Session = Depends(get_db)):
    response = generate_fake_recipe(request)

    recipe = Recipe(
                ingredients=request.ingredients,
                generated_name=response.generated_name,
                steps=response.steps,
                style=request.style
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe


@app.get("/recipes", response_model=List[RecipeOut])
def list_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return recipes


@app.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recette non trouvée")

    return recipe


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recette non trouvée")

    db.delete(recipe)
    db.commit()

    return {"message": f"Recette avec l'ID {recipe_id} supprimée avec succès."}
