from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
import uuid
from sqlalchemy.orm import configure_mappers



def get_uuid():
    return str(uuid.uuid4())



class Users(Base):
    """
    Represents a Users table in the database.

    Attributes:
        __tablename__ (str): The name of the table.
        id (Column): The primary key of the table.
        username (Column): The username of the user.
        email (Column): The email of the user.
        hashed_password (Column): The hashed password of the user.
        is_active (Column): A boolean indicating if the user is active.
        recipes (relationship): A relationship to the Recipe table.
        ratings (relationship): A relationship to the Rating table.
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=get_uuid)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    recipes = relationship('Recipe', back_populates='creator', cascade="all, delete")
    ratings = relationship('Rating', back_populates='user', cascade="all, delete")



class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, default=get_uuid)
    title = Column(String, index=True)
    ingredients = Column(String)
    instructions = Column(Integer)
    cook_time = Column(String)
    difficulty = Column(String)
    image_url = Column(String)
    creator_id = Column(String, ForeignKey('users.id'))
    creator = relationship('Users', back_populates='recipes')
    ratings = relationship('Rating', back_populates='recipe')

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(String, primary_key=True, default=get_uuid)
    recipe_id = Column(String, ForeignKey('recipes.id'))
    user_id = Column(String, ForeignKey('users.id'))
    score = Column(Float)
    user = relationship('Users', back_populates='ratings')
    recipe = relationship('Recipe', back_populates='ratings')
    
configure_mappers()