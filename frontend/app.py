import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Адрес backend API
API_URL = "http://127.0.0.1:8000"

def parse_error(response):
    """Преобразует ошибку FastAPI в понятный текст"""
    try:
        detail = response.json().get("detail", [])
        if isinstance(detail, list):
            messages = []
            for error in detail:
                field = error.get("loc", ["неизвестное поле"])[-1]
                msg = error.get("msg", "неизвестная ошибка")
                # Переводим названия полей на русский
                field_names = {
                    "name": "Название",
                    "category": "Категория",
                    "price": "Цена",
                    "quantity": "Количество",
                    "farm": "Ферма",
                    "organic": "Органик"
                }
                field_ru = field_names.get(field, field)

                # Переводим сообщения
                if "greater than" in msg or "greater than or equal to" in msg:
                    msg = "должно быть не меньше 50 руб."
                elif "string" in msg.lower():
                    msg = "должно быть текстом"
                elif "integer" in msg.lower():
                    msg = "должно быть целым числом"
                elif "number" in msg.lower():
                    msg = "должно быть числом"

                messages.append(f"{field_ru}: {msg}")
            return ", ".join(messages)
        return str(detail)
    except:
        return "Ошибка в данных"

# ========== ГЛАВНАЯ: список продуктов ==========
@app.route("/")
def index():
    """Главная страница со списком всех продуктов"""
    try:
        response = requests.get(f"{API_URL}/products")
        products = response.json()
    except:
        products = []
    return render_template("index.html", products=products)


# ========== ДОБАВЛЕНИЕ ==========
@app.route("/create", methods=["GET", "POST"])
def create():
    """Добавление нового продукта"""
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "category": request.form.get("category"),
            "price": float(request.form.get("price")),
            "quantity": int(request.form.get("quantity")),
            "farm": request.form.get("farm"),
            "organic": request.form.get("organic") == "on"
        }
        response = requests.post(f"{API_URL}/products", json=data)
        if response.status_code == 201:
            return redirect("/")
        return render_template("form.html", error=parse_error(response))
    return render_template("form.html")


# ========== ПРОСМОТР ОДНОГО ПРОДУКТА ==========
@app.route("/detail/<int:product_id>")
def detail(product_id):
    """Просмотр одного продукта"""
    response = requests.get(f"{API_URL}/products/{product_id}")
    if response.status_code == 200:
        product = response.json()
        return render_template("detail.html", product=product)
    return "Продукт не найден", 404


# ========== РЕДАКТИРОВАНИЕ (PUT) ==========
@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit(product_id):
    """Полное редактирование продукта"""
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "category": request.form.get("category"),
            "price": float(request.form.get("price")),
            "quantity": int(request.form.get("quantity")),
            "farm": request.form.get("farm"),
            "organic": request.form.get("organic") == "on"
        }
        response = requests.put(f"{API_URL}/products/{product_id}", json=data)
        if response.status_code == 200:
            return redirect("/")
        return render_template("form.html", error=parse_error(response), product=data)

    # GET: показать форму с текущими данными
    response = requests.get(f"{API_URL}/products/{product_id}")
    if response.status_code == 200:
        product = response.json()
        return render_template("form.html", product=product)
    return "Продукт не найден", 404


# ========== ЧАСТИЧНОЕ РЕДАКТИРОВАНИЕ (PATCH) ==========
@app.route("/patch/<int:product_id>", methods=["GET", "POST"])
def patch(product_id):
    """Частичное обновление продукта"""
    if request.method == "POST":
        data = {}
        if request.form.get("name"):
            data["name"] = request.form.get("name")
        if request.form.get("category"):
            data["category"] = request.form.get("category")
        if request.form.get("price"):
            data["price"] = float(request.form.get("price"))
        if request.form.get("quantity"):
            data["quantity"] = int(request.form.get("quantity"))
        if request.form.get("farm"):
            data["farm"] = request.form.get("farm")
        data["organic"] = request.form.get("organic") == "on"

        response = requests.patch(f"{API_URL}/products/{product_id}", json=data)
        if response.status_code == 200:
            return redirect("/")
        return render_template("patch_form.html", error=parse_error(response))

    response = requests.get(f"{API_URL}/products/{product_id}")
    if response.status_code == 200:
        product = response.json()
        return render_template("patch_form.html", product=product)
    return "Продукт не найден", 404


# ========== УДАЛЕНИЕ ==========
@app.route("/delete/<int:product_id>")
def delete(product_id):
    """Удаление продукта"""
    requests.delete(f"{API_URL}/products/{product_id}")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)