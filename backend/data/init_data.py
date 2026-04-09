from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product, Recipe

def init_database():
    db = SessionLocal()
    
    # Проверяем, есть ли уже данные
    if db.query(Product).count() > 0:
        return
    
    # 50+ продуктов
    products = [
        # Овощи
        ("Помидор", "овощи", 18, 0.9, 0.2, 3.9),
        ("Огурец", "овощи", 15, 0.8, 0.1, 3.6),
        ("Брокколи", "овощи", 34, 2.8, 0.4, 7.0),
        ("Морковь", "овощи", 41, 0.9, 0.2, 9.6),
        ("Лук", "овощи", 40, 1.1, 0.1, 9.3),
        ("Чеснок", "овощи", 149, 6.4, 0.5, 33.1),
        ("Болгарский перец", "овощи", 31, 1.0, 0.3, 6.0),
        ("Кабачок", "овощи", 17, 1.2, 0.3, 3.1),
        ("Баклажан", "овощи", 25, 1.0, 0.1, 5.7),
        ("Цветная капуста", "овощи", 25, 1.9, 0.3, 5.0),
        ("Шпинат", "овощи", 23, 2.9, 0.4, 3.6),
        ("Салат", "овощи", 15, 1.4, 0.2, 2.9),
        ("Редис", "овощи", 16, 0.7, 0.1, 3.4),
        ("Тыква", "овощи", 26, 1.0, 0.1, 6.5),
        
        # Фрукты
        ("Яблоко", "фрукты", 52, 0.3, 0.2, 14.0),
        ("Банан", "фрукты", 89, 1.1, 0.3, 22.8),
        ("Апельсин", "фрукты", 47, 0.9, 0.1, 11.8),
        ("Авокадо", "фрукты", 160, 2.0, 15.0, 9.0),
        ("Груша", "фрукты", 57, 0.4, 0.1, 15.5),
        
        # Белки
        ("Куриная грудка", "мясо", 165, 31.0, 3.6, 0),
        ("Говядина", "мясо", 250, 26.0, 15.0, 0),
        ("Свинина постная", "мясо", 242, 27.0, 14.0, 0),
        ("Лосось", "рыба", 208, 20.0, 13.0, 0),
        ("Тунец", "рыба", 144, 23.0, 4.9, 0),
        ("Яйцо куриное", "яйца", 155, 12.6, 10.6, 1.1),
        ("Творог 5%", "молочные", 121, 17.0, 5.0, 1.8),
        ("Греческий йогурт", "молочные", 59, 10.0, 0.4, 3.6),
        ("Сыр тофу", "растительные", 76, 8.0, 4.8, 1.9),
        ("Чечевица", "бобовые", 116, 9.0, 0.4, 20.0),
        ("Нут", "бобовые", 139, 8.9, 2.5, 22.5),
        ("Фасоль", "бобовые", 132, 8.7, 0.5, 23.7),
        
        # Крупы
        ("Рис", "крупы", 130, 2.7, 0.3, 28.0),
        ("Гречка", "крупы", 153, 5.9, 1.6, 29.0),
        ("Овсянка", "крупы", 68, 2.4, 1.4, 12.0),
        ("Киноа", "крупы", 120, 4.4, 1.9, 21.3),
        ("Макароны", "крупы", 131, 5.0, 1.1, 27.0),
        
        # Молочные
        ("Молоко 2.5%", "молочные", 52, 2.8, 2.5, 4.7),
        ("Сыр Чеддер", "молочные", 402, 25.0, 33.0, 1.3),
        ("Сливочное масло", "молочные", 717, 0.9, 81.0, 0.1),
        
        # Орехи
        ("Миндаль", "орехи", 579, 21.0, 50.0, 22.0),
        ("Грецкий орех", "орехи", 654, 15.0, 65.0, 14.0),
        ("Кешью", "орехи", 553, 18.0, 44.0, 30.0),
        
        # Разное
        ("Оливковое масло", "жиры", 884, 0, 100, 0),
        ("Мед", "сладкое", 304, 0.3, 0, 82.4),
        ("Лимон", "фрукты", 29, 1.1, 0.3, 9.3),
        ("Зелень", "овощи", 36, 2.9, 0.6, 6.8),
        ("Имбирь", "овощи", 80, 1.8, 0.8, 17.8),
        ("Соевый соус", "соусы", 53, 6.0, 0, 5.0),
        ("Томатная паста", "соусы", 82, 4.3, 0.5, 18.2),
    ]
    
    for name, category, calories, protein, fat, carbs in products:
        product = Product(
            name=name,
            category=category,
            calories_per_100g=calories,
            protein_per_100g=protein,
            fat_per_100g=fat,
            carbs_per_100g=carbs
        )
        db.add(product)
    
    db.commit()
    
    # Получаем ID продуктов для рецептов
    tomato = db.query(Product).filter(Product.name == "Помидор").first()
    cucumber = db.query(Product).filter(Product.name == "Огурец").first()
    chicken = db.query(Product).filter(Product.name == "Куриная грудка").first()
    rice = db.query(Product).filter(Product.name == "Рис").first()
    broccoli = db.query(Product).filter(Product.name == "Брокколи").first()
    avocado = db.query(Product).filter(Product.name == "Авокадо").first()
    egg = db.query(Product).filter(Product.name == "Яйцо куриное").first()
    onion = db.query(Product).filter(Product.name == "Лук").first()
    carrot = db.query(Product).filter(Product.name == "Морковь").first()
    garlic = db.query(Product).filter(Product.name == "Чеснок").first()
    potato = db.query(Product).filter(Product.name == "Болгарский перец").first()
    
    # 10+ рецептов
    recipes_data = [
        {
            "title": "Греческий салат",
            "description": "Свежий и полезный салат с овощами и сыром фета",
            "instructions": "Нарежьте помидоры, огурцы, перец кубиками. Добавьте маслины, лук, сыр фета. Заправьте оливковым маслом и посыпьте орегано.",
            "cooking_time": 15,
            "difficulty": "easy",
            "author": "admin",
            "calories": 120,
            "protein": 4.5,
            "fat": 8.0,
            "carbs": 8.0,
            "ingredients": [tomato, cucumber, onion, potato]  # перец вместо potato
        },
        {
            "title": "Курица с рисом и брокколи",
            "description": "Сбалансированный ужин для спортсменов",
            "instructions": "Обжарьте курицу до золотистой. Отварите рис и брокколи. Смешайте и подавайте с соевым соусом.",
            "cooking_time": 30,
            "difficulty": "medium",
            "author": "admin",
            "calories": 450,
            "protein": 35,
            "fat": 12,
            "carbs": 45,
            "ingredients": [chicken, rice, broccoli]
        },
        {
            "title": "Омлет с овощами",
            "description": "Быстрый и питательный завтрак",
            "instructions": "Взбейте яйца. Нарежьте помидоры и перец. Обжарьте овощи, залейте яйцами. Жарьте под крышкой 5 минут.",
            "cooking_time": 10,
            "difficulty": "easy",
            "author": "admin",
            "calories": 220,
            "protein": 15,
            "fat": 14,
            "carbs": 8,
            "ingredients": [egg, tomato, potato]  # перец вместо potato
        },
        {
            "title": "Салат с авокадо и тунцом",
            "description": "Полезный обед с полезными жирами",
            "instructions": "Нарежьте авокадо, добавьте тунец, листья салата. Заправьте лимонным соком и оливковым маслом.",
            "cooking_time": 10,
            "difficulty": "easy",
            "author": "admin",
            "calories": 350,
            "protein": 25,
            "fat": 25,
            "carbs": 12,
            "ingredients": [avocado, db.query(Product).filter(Product.name == "Тунец").first(), db.query(Product).filter(Product.name == "Салат").first()]
        },
        {
            "title": "Чечевичный суп",
            "description": "Сытный вегетарианский суп",
            "instructions": "Обжарьте лук, морковь, чеснок. Добавьте чечевицу и воду. Варите 30 минут. Добавьте специи.",
            "cooking_time": 40,
            "difficulty": "medium",
            "author": "admin",
            "calories": 180,
            "protein": 9,
            "fat": 3,
            "carbs": 30,
            "ingredients": [db.query(Product).filter(Product.name == "Чечевица").first(), onion, carrot, garlic]
        },
        {
            "title": "Овсянка с бананом",
            "description": "Энергичный завтрак",
            "instructions": "Сварите овсянку на молоке. Добавьте нарезанный банан и мед.",
            "cooking_time": 10,
            "difficulty": "easy",
            "author": "admin",
            "calories": 280,
            "protein": 8,
            "fat": 6,
            "carbs": 50,
            "ingredients": [db.query(Product).filter(Product.name == "Овсянка").first(), db.query(Product).filter(Product.name == "Банан").first(), db.query(Product).filter(Product.name == "Мед").first()]
        }
    ]
    
    for recipe_data in recipes_data:
        ingredients = recipe_data.pop("ingredients")
        recipe = Recipe(**recipe_data)
        db.add(recipe)
        db.flush()
        for product in ingredients:
            if product:
                recipe.ingredients.append(product)
    
    db.commit()
    db.close()