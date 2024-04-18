import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, Request, Form, HTTPException, File, UploadFile
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import uuid
import os

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_recipes(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        # Redirect to login if no user is found
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    try:
        recipes = db.query(models.Recipe).filter(models.Recipe.creator_id == user['id']).all()
        if not recipes:
            # No recipes found, handle gracefully by informing the user
            return templates.TemplateResponse("home.html", {"request": request, "recipes": [], "user": user, "message": "No recipes found. Start by adding some!"})
    except Exception as e:
        # Log the exception or handle it as needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

    # Normal response with recipes
    return templates.TemplateResponse("home.html", {"request": request, "recipes": recipes, "user": user})


@router.get("/add", response_class=HTMLResponse)
async def add_recipe_form(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-recipe.html", {"request": request, "user": user})


# @router.post("/add", response_class=HTMLResponse)
# async def create_recipe(request: Request, title: str = Form(...), description: str = Form(...),
#                         cook_time: str = Form(...), difficulty: str = Form(...),
#                         db: Session = Depends(get_db)):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     recipe = models.Recipe(title=title, description=description, cook_time=cook_time,
#                             difficulty=difficulty, creator_id=user.id)

#     db.add(recipe)
#     db.commit()

#     return RedirectResponse(url="/recipes", status_code=status.HTTP_302_FOUND)

# @router.post("/add", response_class=HTMLResponse)
# async def create_recipe(request: Request, title: str = Form(...), description: str = Form(...),
#                         cook_time: str = Form(...), difficulty: str = Form(...),
#                         image: UploadFile = File(...), db: Session = Depends(get_db)):
#     if image.content_type not in ['image/jpeg', 'image/png']:
#         return templates.TemplateResponse("add-recipe.html", {
#             "request": request, 
#             "user": await get_current_user(request),
#             "error": "Invalid image format. Only JPEG or PNG are accepted."
#         })

#     file_location = f"static/images/{uuid.uuid4()}.{image.filename.split('.')[-1]}"
#     os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
#     with open(file_location, "wb+") as file_object:
#         shutil.copyfileobj(image.file, file_object)
        
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     recipe = models.Recipe(
#         title=title, 
#         description=description, 
#         cook_time=cook_time,
#         difficulty=difficulty, 
#         creator_id=user.id,
#         image_url=file_location
#     )

#     db.add(recipe)
#     db.commit()

#     return RedirectResponse(url="/recipes", status_code=status.HTTP_302_FOUND)

@router.post("/add", response_class=HTMLResponse)
async def create_recipe(
    request: Request, 
    title: str = Form(...), 
    ingredients: str = Form(...),  # Handling ingredients
    instructions: str = Form(...),  # Handling instructions
    cook_time: str = Form(...), 
    difficulty: str = Form(...),
    image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Validate image format
    if image.content_type not in ['image/jpeg', 'image/png']:
        return templates.TemplateResponse("add-recipe.html", {
            "request": request, 
            "user": await get_current_user(request),
            "error": "Invalid image format. Only JPEG or PNG are accepted."
        })

    # Save the image file
    file_location = f"../images/{uuid.uuid4()}.{image.filename.split('.')[-1]}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)

    # Verify user authentication
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    # Create a new recipe object and add it to the database
    new_recipe = models.Recipe(
        title=title, 
        ingredients=ingredients,
        instructions=instructions,
        cook_time=cook_time,
        difficulty=difficulty, 
        creator_id=user['id'],
        image_url=file_location
    )
    db.add(new_recipe)
    db.commit()

    # Redirect to the recipes list page after successful creation
    return RedirectResponse(url="/recipes", status_code=status.HTTP_302_FOUND)


@router.get("/edit/{recipe_id}", response_class=HTMLResponse)
async def edit_recipe_form(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id, models.Recipe.creator_id == user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return templates.TemplateResponse("edit-recipe.html", {"request": request, "recipe": recipe, "user": user})


@router.post("/edit/{recipe_id}", response_class=HTMLResponse)
async def update_recipe(request: Request, recipe_id: int, title: str = Form(...),
                        description: str = Form(...), cook_time: int = Form(...),
                        difficulty: str = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id, models.Recipe.creator_id == user.id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.title = title
    recipe.description = description
    recipe.cook_time = cook_time
    recipe.difficulty = difficulty

    db.commit()

    return RedirectResponse(url="/recipes", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{recipe_id}")
async def delete_recipe(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id, models.Recipe.creator_id == user.id).first()
    if not recipe:
        return RedirectResponse(url="/recipes", status_code=status.HTTP_404_NOT_FOUND)

    db.delete(recipe)
    db.commit()

    return RedirectResponse(url="/recipes", status_code=status.HTTP_302_FOUND)
