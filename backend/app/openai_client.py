from app.schemas import RecipeRequest, RecipeResponse


def generate_fake_recipe(request: RecipeRequest) -> RecipeResponse:
    return RecipeResponse(
        generated_name="Spaghetti Aglio e Olio",
        ingredients=request.ingredients,
        steps="1. Fais cuire les pâtes."
    )
