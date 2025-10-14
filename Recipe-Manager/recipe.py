import json
import os

RECIPE_FILES = 'recipe.json'

class Ingredient:
    """
    Represents a single ingredient for a recipe.
    This class encapsulates the data for an ingredient (name, quantity, unit)
    and provides methods for serialization.
    """
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def to_dict(self):
        """
        Returns the ingredient object to a dictionary for JSON serialization"""
        return {
                "name": self.name,
                "quantity": self.quantity
                "unit": self.unit
                }

    def __str__(self):
        """Provides a user-friendly string representation of the ingredient."""
        return f"{self.quantity} {self.unit} of {self.name}"

class Recipe:
    """
    Represents a single recipe.
    This class is an excellent example of composition, as it "has-a" list of
    ingredient objects. It encapsulates all data and logic related to a recipe.
    """
    def __init__(self, name, steps, ingredients = None):
        self.name = name
        self.steps = steps
        # Thos list holds ingredient objects, demonstrating composition
        self.ingredients = ingredients if ingredients else []

    def to_dict(self):
        """Converts the Recipe object to a dictionary for JSON serialization"""
        return {
                "name": self.name,
                "steps": self.steps,
                "ingredients": [ingredient.to_dict() for ingredient in self.ingredients]

    @staticmethod
    def from_dict(data):
    """Creates a Recipe object from a dictionary (for JSON deserialization)"""
    ingredients = [ingredient(**d) for d in data['ingredients']]
    return Recipe(data['name'], data['steps'], ingredients)

    def __str__(self):
        """Provides a user-frientdly string representation of the recipe."""
        ingredients_list = "\n- ".join([str(ing) for ing in self.ingredients])
        steps_list "\n".join([f"{i+1}. {step}" for i, step in enumerate(self.steps)])
        return (
            f"--- {self.name} ---\n\n"
            f"Ingredients:\n- {ingredients_list}\n\n"
            f"Instrutions:\n{steps_list}\n"
            )

class RecipeManager:
    """
    Manages the collection of recipes.
    This class handles the logic for solving, loading, adding and viewing recipes, separating the management logic form the data itself.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.recipes =[]
        self._load_recipes()

    def _load_recipes(self):
        """Loads recipes from the JSON file into the 'recipes' list."""
        if not os.path.exists(self.file_path):
            print("Recipe file not found, Starting with an empty recipe book.")
            return

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.recipes = [Recipe.from_dict(d) for d in data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading recipe file: {e}. Starting with an empty recipe book.")
            self.recipes = []


    def save_recipes(self):
        """Saves all recipes from the 'recipes' list to the JSON file."""
        data_to_save = [recipe.to_dict() for recipe in self.recipes]
        with open(self.file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print("Recipes saved successfully.")

    def add_recipe(self, recipe):
        """Adds a new recipe object and saves the recipe book."""
        self.recipes.append(recipe)
        self.save_recipes()
        print("\nRecipe added successfully.")

    def view_all_recipes(self):
        """Prints all recipes to the console."""
        if not self.recipes:
            print("\nNo recipes found")
        else:
            print(f"\n-- Showing {len(self.recipes)} Recipes ---")
            for recipe in self.recipes:
                print(recipe)
                print("-" * 20)
    def find_recipe(self, name):
        """Finds and returns a recipe by its name."""
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe
        return None

    def get_recipe_details():
        """Helper function to get recipe details from the user."""
        name = input("Enter recipe name: ")
        num_ingredients = int(input("How many ingredients: "))
        ingredients = []
        for  _ in range(num_ingredients):
            ing_name = input("Ingredient name: ")
            ing_quantity = input("Quantity: ")
            ing_unit = input("Unit (e.g., cups, g, ml): ")
        steps = []
        print("Enter recipe steps (type 'done' on a new line when finished):")
        while True:
            step = input()
            if step.lower() == 'done':
                break
            steps.append(step)

        return Recipe(name, steps, ingredients)

    def main():
        """
        The main function that provides the command-line interface.
        """
        recipe_manager = RecipeManager(RECIPES_FILE)
        print("Welcome to your Recipe Manager!")

        while True:
            print("\nWhat would you like to d?")
            print("1. Add a new recipe")
            print("2. View all recipes")
            print("3. Find a recipe by name")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                new_recipe = get_recipe_details()
                recipe_manager.add_recipe(new_recipe)
            elif choice == '2':
                recipe_manager.view_all_recipes()
            elif choice == '3':
                name = input("Enter the name of the recipe you want to find: ")
                recipe = recipe_manager.find_recipe(name)
                if recipe:
                    print("\nRecipe found: \n")
                    print(recipe)
                else:
                    print(f"\nRecipe '{name}' not found")
            elif choice == '4':
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()
