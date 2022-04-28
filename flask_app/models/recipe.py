from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made'].date()
        self.minutes = data['minutes']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def find_for_user(cls, user_id):
        query = "select * from recipes where user_id = %(user_id)s;"
        data = {
            "user_id": user_id
        }
        results = connectToMySQL('recipes_schema').query_db(query, data)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes where id = %(id)s;"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return (cls(result[0]))

    @classmethod
    def add(cls, data):
        query = "INSERT INTO recipes (name, description, instructions,date_made,minutes,user_id) VALUES (%(name)s, %(description)s, %(instructions)s,%(date_made)s,%(minutes)s, %(user_id)s);"
        connectToMySQL('recipes_schema').query_db(query, data)

    @ classmethod
    def update_info(cls, data):
        query = "update recipes  set name = %(name)s, description=%(description)s, instructions=%(instructions)s,minutes=%(minutes)s,date_made=%(date_made)s ,updated_at = Now() where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @ classmethod
    def delete(cls, data):
        query = "Delete FROM recipes where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("name is required.")
            is_valid = False
        if len(data['description']) < 3:
            flash(" description is required.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash(" instructions is required.")
            is_valid = False
        return is_valid
