from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Связь многие-ко-многим (рецепты <-> продукты)
recipe_ingredient = Table(
    'recipe_ingredients',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', String, nullable=False)  # количество в граммах/штуках
)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)  # овощи, фрукты, мясо, крупы и т.д.
    calories_per_100g = Column(Float)  # калорий на 100г
    protein_per_100g = Column(Float)   # белки
    fat_per_100g = Column(Float)       # жиры
    carbs_per_100g = Column(Float)     # углеводы
    
    recipes = relationship("Recipe", secondary=recipe_ingredient, back_populates="ingredients")

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    instructions = Column(String)  # пошаговый рецепт
    cooking_time = Column(Integer)  # время приготовления в минутах
    difficulty = Column(String)  # easy, medium, hard
    author = Column(String, default="user")
    image_url = Column(String, nullable=True)
    
    # Питательные вещества на 100г блюда
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    
    ingredients = relationship("Product", secondary=recipe_ingredient, back_populates="recipes")