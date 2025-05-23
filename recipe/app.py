from flask import Flask, request, render_template
from llm_recipe_project import generate_recipe  # 导入你原来的函数
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form.get("ingredients", "")
        diet = request.form.get("diet", "")
        recipe = generate_recipe(ingredients, diet)  # 调用原有功能
        return render_template("result.html", recipe=recipe)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)