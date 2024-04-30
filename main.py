import json
from typing import List, Dict

dispenser_reagents = ["Aluminium",
                      "Carbon",
                      "Chlorine",
                      "Copper",
                      "Ethanol",
                      "Fluorine",
                      "Sugar",
                      "Hydrogen",
                      "Iodine",
                      "Iron",
                      "Lithium",
                      "Mercury",
                      "Nitrogen",
                      "Oxygen",
                      "Phosphorus",
                      "Potassium",
                      "Radium",
                      "Silicon",
                      "Sodium",
                      "Sulfur",
                      "Water"]
def print_separator(sep="#"):
    print(sep * 40)

def get_reagent_name(reagents, reagent_name):
    found_reagent = reagents.get(reagent_name)
    if found_reagent is None:
        return reagent_name
    else:
        return found_reagent["name"]

def get_reagent_id(reagents, reagent_name):

    for reagent in reagents.values():
        if reagent["id"].lower() == reagent_name.lower() or reagent["name"].lower().replace("ё", "е") == reagent_name.lower().replace("ё", "е"):
            return reagent["id"]

    for reagent in reagents.values():
        for reagent_word in reagent["id"].split():
            if reagent_word.lower().startswith(reagent_name.lower()):
                return reagent["id"]
        for reagent_word in reagent["name"].split():
             if reagent_word.lower().replace("ё", "е").startswith(reagent_name.lower().replace("ё", "е")):
                return reagent["id"]

    return None

def get_product_amount(recipe, reagent):
    return recipe["products"].get(reagent)

def fill_out_the_recipe(reagents, recipes: Dict, recipe: List[str], reagent: str, amount: float, have_recipe=None, deep=-1):

    deep += 1

    if have_recipe is None:
        have_recipe = []

    if reagent in dispenser_reagents and deep > 0:
        return

    if reagent in have_recipe:
        return

    have_recipe.append(reagent)

    suitable_recipes = find_recipes(recipes, reagent)

    if len(suitable_recipes) == 0:
        return

    tab = "\t" * deep

    count = 1

    for suitable_recipe in suitable_recipes:

        if len(suitable_recipes) > 1:
            recipe.append(tab + "-" * 40)
            recipe.append(tab + f"Вариант {count}:")

        result_amount = get_product_amount(suitable_recipe, reagent)

        rate = amount / result_amount

        mix_cats = []
        for mix_cat in suitable_recipe["mixingCategories"]:
            mix_cats.append(mix_cat["name"])

        temp_str = ""
        hasMin = suitable_recipe["minTemp"] != 0
        hasMax = suitable_recipe["hasMax"]

        minT = suitable_recipe["minTemp"]
        maxT = suitable_recipe["maxTemp"]

        if hasMax and hasMin:
            temp_str = f" от {minT}K до {maxT}K"
        elif hasMin:
            temp_str = f" от {minT}K"
        elif hasMax:
            temp_str = f" до {maxT}K"


        recipe.append(tab + ", ".join(mix_cats) + temp_str + ":")

        count1 = 1
        for reactant in suitable_recipe["reactants"].keys():
            need_amount = rate * suitable_recipe["reactants"][reactant]["amount"]
            catalyst = suitable_recipe["reactants"][reactant]["catalyst"]

            need_amount_str = f"{need_amount:.2f}"
            need_amount_str = need_amount_str.strip("0").strip(".")

            catalyst_str = ""
            if catalyst:
                catalyst_str = " катализатор"
            recipe.append(tab + f"{count1}) {need_amount_str} {get_reagent_name(reagents, reactant)}" + catalyst_str)

            fill_out_the_recipe(reagents, recipes, recipe, reactant, need_amount, have_recipe.copy(), deep)
            count1 += 1

        count+=1





def find_recipes(recipes: Dict, reagent: str) -> List[Dict]:
    found_recipes = []
    for recipe in recipes.values():
        if reagent in recipe["products"]:
            found_recipes.append(recipe)
    return found_recipes


with open('reactions.txt', encoding="utf-8") as file:
    recipes = json.load(file)

with open('reagents.txt', encoding="utf-8") as file:
    reagents = json.load(file)

while True:

    while True:
        reagent = input("Вещество: ")
        if reagent == "":
            continue
        reagent_id = get_reagent_id(reagents, reagent)
        if reagent_id is not None:
            break

    while True:
        amount_input = input("Количество: ")
        if amount_input == "":
            amount = 90
            break
        try:
            amount = int(amount_input)
        except:
            pass
        else:
            break

    recipe = []

    recipe.append(f"{amount} {get_reagent_name(reagents, reagent_id)}")
    fill_out_the_recipe(reagents, recipes, recipe, reagent_id, amount)
    print_separator()
    print("\n".join(recipe))
    print_separator()
