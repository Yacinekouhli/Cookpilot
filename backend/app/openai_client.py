import os
from openai import OpenAI
from app.schemas import RecipeRequest, RecipeResponse
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fake_recipe(request: RecipeRequest) -> RecipeResponse:
    prompt = (
        f"Tu es un chef cuisinier créatif. "
        f"Crée une recette originale de style {request.style or 'libre'} "
        f"avec les ingrédients suivants : {request.ingredients}. "
        f"Donne-moi un nom de recette et les étapes de préparation."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant culinaire expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        content = completion.choices[0].message.content.strip()

        # Découper le nom et les étapes
        lines = content.split("\n")
        generated_name = lines[0].strip()
        steps = "\n".join(lines[1:]).strip()

        return RecipeResponse(
            generated_name=generated_name,
            ingredients=request.ingredients,
            steps=steps
        )

    except Exception as e:
        print("Erreur OpenAI :", e)
        raise
