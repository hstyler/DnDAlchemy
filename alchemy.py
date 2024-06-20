"""
    Performs alchemy automagically :)
"""

from typing import List, Tuple, Optional
from enum import IntEnum
import sys

base_ingredients = [
    "DF", "CT", "BL", "AP", 
    "OB", "PM", "HB", "GL", 
    "BH", "VM", "TF", "ST", 
    "SP", "RL", "MM", "MD", 
    "LS", "IF", "CE", "IW", 
    "FP", "CC", "EE", "FR", 
    "DR", "ZW", "SB", "MR", 
    "DW", "KM"
]

class Direction(IntEnum):
    """
    Recipe crafting direction
    """
    COMBINE = 0
    SPLIT = 1

class Recipe():
    """
    Representation of recipe that can be performed in either direction, i.e.
    Reagent + Reagent = Result
    or
    Result -> Reagent + Reagent
    """
    reagents: List[str]
    result: str
    no_split: bool

    def __init__(self, reagants: List[str], result: str, no_split: bool = False):
        self.reagents = reagants
        self.result = result
        self.no_split = no_split

    def get_recipe_string(self, direction: Direction = Direction.COMBINE) -> str:
        """
        Return string representation of recipe based on crafting direction
        :param direction: crafting direction
        :returns: string representation of recipe
        """
        if direction == Direction.COMBINE:
            return f"{' + '.join(self.reagents)} = {self.result}"

        return f"{self.result} -> {' + '.join(self.reagents)}"

    def get_all_elements(self) -> List[str]:
        """
        Get all elements involved in recipe (result + reagents)
        :returns: list of elements in recipe
        """
        return self.reagents + self.result

    def is_trivial(self, direction: Direction = Direction.COMBINE) -> bool:
        """
        Returns if the recipe can be performed with the basic set of ingredients
        :param direction: crafting direction
        :returns: whether recipe can be trivially crafted
        """
        if direction == Direction.COMBINE:
            return set(self.reagents).issubset(base_ingredients)

        return self.result in base_ingredients

    def get_inputs(self, direction: Direction = Direction.COMBINE) -> List[str]:
        """
        Returns the inputs for the recipe, based on crafting direction
        :param direction: crafting direction
        :returns: recipe inputs for provided direction
        """
        return [self.result] if direction == Direction.SPLIT else self.reagents

    def get_outputs(self, direction: Direction = Direction.COMBINE) -> List[str]:
        """
        Returns the outputs for the recipe, based on crafting direction
        :param direction: crafting direction
        :returns: recipe outputs for provided direction
        """
        return self.reagents if direction == Direction.SPLIT else [self.result]

    def get_required_recipe_direction(self, target: str) -> Direction:
        """
        Returns the crafting direction to reach a given target element
        :param target: target element
        :returns: required direction
        """
        return Direction.SPLIT if target in self.reagents else Direction.COMBINE

    def can_make(self, target: str) -> bool:
        """
        Returns True if the target element can be made with this recipe
        :param target: target element
        :returns: whether target can be produced with this recipe
        """
        if target == self.result and target not in self.reagents:
            return True
        elif target != self.result and target in self.reagents and not self.no_split:
            return True
        return False

recipes: List[Recipe] = [
    Recipe(["SI", "WV"], "AC"),
    Recipe(["AC", "SB"], "DB"),
    Recipe(["ZW", "AC"], "BW"),
    Recipe(["WV"], "PW"),
    Recipe(["MR", "MR"], "RS"),
    Recipe(["DW", "WV"], "US"),
    Recipe(["KM", "US"], "WE"),
    Recipe(["PW", "RS"], "CW"),
    Recipe(["LT", "PF"], "PF"),
    Recipe(["PF", "FT"], "EA"),
    Recipe(["LT", "EA"], "FE"),
    Recipe(["FP", "IW"], "SI"),
    Recipe(["CC"], "HC"),
    Recipe(["HC", "SI"], "AH"),
    Recipe(["EA", "FS"], "HC"),
    Recipe(["HC", "FS"], "PS"),
    Recipe(["FR", "EE"], "GC"),
    Recipe(["DR"], "CS"),
    Recipe(["GC", "CS"], "ES"),
    Recipe(["DW"], "WV"),
    Recipe(["FE", "AH"], "RF", no_split=True),
    Recipe(["PS", "ES"], "RE", no_split=True),
    Recipe(["BW", "DB"], "RA", no_split=True),
    Recipe(["CW", "WE"], "RW", no_split=True),
]

def get_valid_recipes(target: str) -> List[Recipe]:
    """
    Returns a list of recipes from the list that can be used to produce the target element
    :param target: target element
    :returns: list of recipes to reach target
    """
    valid_recipes: List[Recipe] = []

    for recipe in recipes:
        if recipe.can_make(target):
            valid_recipes.append(recipe)

    return valid_recipes


def get_recipe_path(target: str, previous_recipe: Recipe = None) -> Tuple[bool, Optional[List[str]]]:
    """
    Recursively resolves a path of recipes that produces the target

    :param target: target element
    :param previous_recipe: recipe being resolved in previous recursion step
    :returns: tuple representing whether recipe path was found, and the recipe path
    """
    recipes_to_target = get_valid_recipes(target)

    if len(recipes_to_target) == 0:
        return False, []

    # Don't consider the previous recipe
    if previous_recipe in recipes_to_target:
        recipes_to_target.remove(previous_recipe)

    for recipe in recipes_to_target:
        direction = recipe.get_required_recipe_direction(target)

        if recipe.is_trivial(direction):
            return True, [recipe.get_recipe_string(direction)]
        else:
            reagent_recipe_list: List[Recipe] = []

            solved_all_reagents = True

            for reagent in recipe.get_inputs(direction):
                if reagent not in base_ingredients:
                    solved, recipe_path = get_recipe_path(reagent, recipe)

                    if solved:
                        reagent_recipe_list = reagent_recipe_list + recipe_path
                    else:
                        solved_all_reagents = False
                        break

            if solved_all_reagents:
                return True, reagent_recipe_list + [recipe.get_recipe_string(direction)]

    return False, []


def print_recipe_path(target: str) -> None:
    """
    Print recipe path to reach target element
    :param target: target element
    """
    solved, recipe_path = get_recipe_path(target)

    if solved:
        for recipe in recipe_path:
            print(recipe)
    else:
        print(f"Failed to solve for {target}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: alchemy.py [target element]")
    else:
        print_recipe_path(sys.argv[1])
