from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/recipes/<int:recipe_id>')
def view_one(recipe_id):
    data = {
        "id": recipe_id,
    }
    users = User.get_user_id(session["user_id"])
    recipes = Recipe.get_one(data)
    return render_template("recipe.html", recipes=recipes, logged_user=users)


@app.route('/recipes/new')
def add_recipe():
    return render_template("add_recipe.html")


@app.route('/recipes/create', methods=['post'])
def create_recipes():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "minutes": request.form['minutes'],
        "user_id": session['user_id'],
    }
    Recipe.add(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):

    data = {
        "id": recipe_id
    }
    recipe = Recipe.get_one(data)
    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/recipes/update', methods=['post'])
def update():
    Recipe.update_info(request.form)
    recipe_id = request.form['id']
    return redirect(f'/recipes/{recipe_id}')


@app.route('/recipes/<int:recipe_id>/destroy')
def delete_recipe(recipe_id):
    data = {
        "id": recipe_id,
    }
    Recipe.delete(data)
    return redirect('/dashboard')
