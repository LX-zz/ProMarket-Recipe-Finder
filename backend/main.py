from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("eatwell.db")
    cursor = conn.cursor()
    
    # Создаем таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            category TEXT,
            calories_per_100g REAL,
            protein_per_100g REAL,
            fat_per_100g REAL,
            carbs_per_100g REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            instructions TEXT,
            cooking_time INTEGER,
            difficulty TEXT,
            author TEXT,
            image_url TEXT,
            calories REAL,
            protein REAL,
            fat REAL,
            carbs REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipe_products (
            recipe_id INTEGER,
            product_id INTEGER,
            quantity TEXT
        )
    ''')
    
    conn.commit()
    
    # Проверяем, есть ли продукты
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Добавляем продукты
        products = [
            ("Помидор", "овощи", 18, 0.9, 0.2, 3.9),
            ("Огурец", "овощи", 15, 0.8, 0.1, 3.6),
            ("Куриная грудка", "мясо", 165, 31.0, 3.6, 0),
            ("Рис", "крупы", 130, 2.7, 0.3, 28.0),
            ("Брокколи", "овощи", 34, 2.8, 0.4, 7.0),
            ("Морковь", "овощи", 41, 0.9, 0.2, 9.6),
            ("Лук", "овощи", 40, 1.1, 0.1, 9.3),
            ("Чеснок", "овощи", 149, 6.4, 0.5, 33.1),
            ("Яйцо", "яйца", 155, 12.6, 10.6, 1.1),
            ("Гречка", "крупы", 153, 5.9, 1.6, 29.0),
            ("Авокадо", "фрукты", 160, 2.0, 15.0, 9.0),
            ("Банан", "фрукты", 89, 1.1, 0.3, 22.8),
            ("Яблоко", "фрукты", 52, 0.3, 0.2, 14.0),
            ("Лосось", "рыба", 208, 20.0, 13.0, 0),
            ("Творог", "молочные", 121, 17.0, 5.0, 1.8),
            ("Сыр", "молочные", 402, 25.0, 33.0, 1.3),
            ("Картофель", "овощи", 77, 2.0, 0.1, 17.0),
            ("Макароны", "крупы", 131, 5.0, 1.1, 27.0),
            ("Бекон", "мясо", 541, 37.0, 42.0, 1.4),
            ("Сливки", "молочные", 345, 2.8, 35.0, 2.9),
            ("Молоко", "молочные", 52, 2.8, 2.5, 4.7),
            ("Мед", "сладкое", 304, 0.3, 0, 82.4),
            ("Лимон", "фрукты", 29, 1.1, 0.3, 9.3),
            ("Болгарский перец", "овощи", 31, 1.0, 0.3, 6.0),
            ("Кабачок", "овощи", 17, 1.2, 0.3, 3.1),
            ("Баклажан", "овощи", 25, 1.0, 0.1, 5.7),
            ("Тыква", "овощи", 26, 1.0, 0.1, 6.5),
            ("Спаржа", "овощи", 20, 2.2, 0.1, 3.9),
            ("Говядина", "мясо", 250, 26.0, 15.0, 0),
            ("Свинина", "мясо", 242, 27.0, 14.0, 0),
            ("Креветки", "рыба", 99, 24.0, 0.3, 0),
            ("Тунец", "рыба", 144, 23.0, 4.9, 0),
            ("Форель", "рыба", 190, 20.0, 12.0, 0),
            ("Греческий йогурт", "молочные", 59, 10.0, 0.4, 3.6),
            ("Оливковое масло", "жиры", 884, 0, 100, 0),
            ("Соевый соус", "соусы", 53, 6.0, 0, 5.0),
        ]
        
        for p in products:
            cursor.execute("INSERT INTO products (name, category, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g) VALUES (?,?,?,?,?,?)", p)
        
        # Получаем ID продуктов для связывания
        cursor.execute("SELECT id, name FROM products")
        products_map = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Добавляем рецепты
        recipes_data = [
            ("Паста Карбонара", "Классическая итальянская паста с беконом и яйцом", 
             "1. Отварите пасту до состояния аль денте.\n2. Обжарьте бекон до хруста.\n3. Смешайте яйца с тертым сыром.\n4. Соедините горячую пасту с беконом, добавьте яичную смесь.\n5. Перемешивайте пока соус не загустеет.\n6. Подавайте с черным перцем.", 
             20, "medium", "admin", None, 480, 18, 22, 52,
             ["Макароны", "Яйцо", "Бекон", "Сыр"]),
            
            ("Греческий салат", "Свежий средиземноморский салат с овощами и сыром фета", 
             "1. Нарежьте помидоры и огурцы крупно.\n2. Добавьте болгарский перец.\n3. Добавьте красный лук.\n4. Добавьте маслины.\n5. Посыпьте сыром фета.\n6. Заправьте оливковым маслом.", 
             15, "easy", "admin", None, 180, 6, 14, 8,
             ["Помидор", "Огурец", "Болгарский перец", "Сыр"]),
            
            ("Томатный суп", "Кремовый томатный суп с базиликом", 
             "1. Обжарьте лук и чеснок.\n2. Добавьте помидоры и бульон.\n3. Варите 20 минут.\n4. Пюрируйте блендером.\n5. Добавьте сливки.\n6. Подавайте с базиликом.", 
             35, "medium", "admin", None, 120, 3, 5, 15,
             ["Помидор", "Лук", "Чеснок", "Сливки"]),
            
            ("Курица с рисом", "Сочная курица с ароматным рисом", 
             "1. Обжарьте курицу до золотистого цвета.\n2. Добавьте лук и морковь.\n3. Добавьте рис и воду.\n4. Тушите 20 минут.\n5. Добавьте специи.\n6. Подавайте с зеленью.", 
             30, "medium", "admin", None, 380, 22, 12, 45,
             ["Куриная грудка", "Рис", "Лук", "Морковь"]),
            
            ("Омлет с овощами", "Пышный омлет с помидорами и сыром", 
             "1. Взбейте яйца с молоком.\n2. Нарежьте овощи.\n3. Обжарьте овощи на сковороде.\n4. Залейте яйцами.\n5. Посыпьте сыром.\n6. Готовьте под крышкой 5 минут.", 
             15, "easy", "admin", None, 220, 14, 16, 5,
             ["Яйцо", "Помидор", "Сыр", "Молоко"]),
            
            ("Лосось с брокколи", "Полезный ужин с рыбой и овощами", 
             "1. Замаринуйте лосось в лимонном соке.\n2. Обжарьте лосось с каждой стороны.\n3. Отварите брокколи на пару.\n4. Подавайте с лимоном.\n5. Посыпьте зеленью.\n6. Добавьте оливковое масло.", 
             25, "medium", "admin", None, 350, 28, 22, 8,
             ["Лосось", "Брокколи", "Лимон", "Оливковое масло"]),
            
            ("Борщ", "Традиционный украинский суп", 
             "1. Сварите мясной бульон.\n2. Обжарьте свеклу, морковь, лук.\n3. Добавьте в бульон картофель и капусту.\n4. Добавьте зажарку.\n5. Варите 15 минут.\n6. Подавайте со сметаной.", 
             90, "medium", "admin", None, 150, 8, 5, 18,
             ["Говядина", "Картофель", "Морковь", "Лук"]),
            
            ("Панкейки с бананом", "Пышные американские блинчики", 
             "1. Смешайте муку, яйца, молоко.\n2. Добавьте разрыхлитель.\n3. Жарьте на сухой сковороде.\n4. Нарежьте банан.\n5. Подавайте с медом.\n6. Посыпьте сахарной пудрой.", 
             25, "easy", "admin", None, 280, 8, 10, 40,
             ["Яйцо", "Молоко", "Банан", "Мед"]),
            
            ("Цезарь с курицей", "Знаменитый салат с курицей и сухариками", 
             "1. Обжарьте курицу.\n2. Нарежьте салат.\n3. Приготовьте соус.\n4. Смешайте все.\n5. Добавьте сухарики.\n6. Посыпьте пармезаном.", 
             25, "medium", "admin", None, 380, 28, 24, 15,
             ["Куриная грудка", "Сыр", "Яйцо", "Лимон"]),
            
            ("Овсяная каша", "Полезный завтрак", 
             "1. Сварите овсянку на молоке.\n2. Добавьте нарезанный банан.\n3. Добавьте мед.\n4. Посыпьте орехами.\n5. Добавьте корицу.\n6. Подавайте теплой.", 
             10, "easy", "admin", None, 320, 10, 8, 55,
             ["Овсянка", "Молоко", "Банан", "Мед"]),
        ]
        
        for recipe in recipes_data:
            title, desc, instructions, time, diff, author, img, cal, prot, fat, carbs, ingredients = recipe
            cursor.execute('''
                INSERT INTO recipes (title, description, instructions, cooking_time, difficulty, author, image_url, calories, protein, fat, carbs)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ''', (title, desc, instructions, time, diff, author, img, cal, prot, fat, carbs))
            recipe_id = cursor.lastrowid
            
            # Связываем с продуктами
            for ing_name in ingredients:
                if ing_name in products_map:
                    cursor.execute("INSERT INTO recipe_products (recipe_id, product_id, quantity) VALUES (?,?,?)", 
                                  (recipe_id, products_map[ing_name], "100г"))
    
    conn.commit()
    
    # Проверяем, есть ли рецепты
    cursor.execute("SELECT COUNT(*) FROM recipes")
    if cursor.fetchone()[0] == 0:
        print("Рецепты не добавились!")
    
    conn.close()

init_db()

@app.get("/api/products")
def get_products(category: Optional[str] = None):
    conn = sqlite3.connect("eatwell.db")
    cursor = conn.cursor()
    
    if category and category != "все":
        cursor.execute("SELECT id, name, category, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g FROM products WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT id, name, category, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g FROM products")
    
    products = [{"id": row[0], "name": row[1], "category": row[2], "calories_per_100g": row[3], "protein_per_100g": row[4], "fat_per_100g": row[5], "carbs_per_100g": row[6]} for row in cursor.fetchall()]
    conn.close()
    return products

@app.get("/api/categories")
def get_categories():
    conn = sqlite3.connect("eatwell.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

@app.get("/api/recipes")
def get_recipes(search: Optional[str] = None):
    conn = sqlite3.connect("eatwell.db")
    cursor = conn.cursor()
    
    if search:
        cursor.execute("SELECT id, title, description, instructions, cooking_time, difficulty, author, image_url, calories, protein, fat, carbs FROM recipes WHERE title LIKE ? OR description LIKE ?", 
                      (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT id, title, description, instructions, cooking_time, difficulty, author, image_url, calories, protein, fat, carbs FROM recipes")
    
    recipes_data = cursor.fetchall()
    
    result = []
    for r in recipes_data:
        cursor.execute('''
            SELECT p.id, p.name, rp.quantity FROM recipe_products rp
            JOIN products p ON rp.product_id = p.id
            WHERE rp.recipe_id = ?
        ''', (r[0],))
        ingredients_list = [{"id": row[0], "name": row[1], "quantity": row[2]} for row in cursor.fetchall()]
        
        result.append({
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "instructions": r[3],
            "cooking_time": r[4],
            "difficulty": r[5],
            "author": r[6],
            "image_url": r[7],
            "calories": r[8],
            "protein": r[9],
            "fat": r[10],
            "carbs": r[11],
            "ingredients": ingredients_list
        })
    
    conn.close()
    return result

@app.post("/api/recipes")
def create_recipe(recipe: dict):
    conn = sqlite3.connect("eatwell.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO recipes (title, description, instructions, cooking_time, difficulty, author, image_url, calories, protein, fat, carbs)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    ''', (recipe['title'], recipe['description'], recipe['instructions'], recipe['cooking_time'], 
          recipe['difficulty'], recipe['author'], recipe.get('image_url'), recipe['calories'], 
          recipe['protein'], recipe['fat'], recipe['carbs']))
    
    recipe_id = cursor.lastrowid
    
    for ing in recipe.get('ingredients', []):
        cursor.execute("INSERT INTO recipe_products (recipe_id, product_id, quantity) VALUES (?,?,?)", 
                      (recipe_id, ing['product_id'], ing.get('quantity', '100г')))
    
    conn.commit()
    conn.close()
    return {"message": "Рецепт добавлен", "id": recipe_id}

@app.delete("/api/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, user: str):
    conn = sqlite3.connect("eatwell.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT author FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    
    if user != "admin" and recipe[0] != user:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
    
    cursor.execute("DELETE FROM recipe_products WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Рецепт удален"}