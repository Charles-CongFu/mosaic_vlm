system_prompt = """
    Your goal is to convert an internet recipe into a json of subtasks with 
    dependencies.
    
    Your first step is to identify subtasks in the recipe. Some examples of the 
    subtasks are below, but you can define more subtasks:
    - "fetch {ingredient}": gather certain ingredient
    - "pour {ingredient} at {location}": pour certain ingredient at a location
    - "stir {location}": stir certain location (such as pots, bowls)
    - "cut {ingredient}": cut certain ingredient
    - "mince {ingredient}": mince certain ingredient
    - "toast {food_item}": toast certain food item
    - "season {food_item} with {condiment}": season a food item with a condiment 
    to the chef’s liking
    - "boil {ingredient}": such as boil water
    - "place {ingredient} into {location}": put ingredient into a location
    - "assemble {food_item}": such as assemble sandwiches
    - "stack {ingredient_1} on top of {ingredient_2/food_item}": such as stacking 
    tomato on top of cheese or stacking tomato on top of the sandwich
    - "melt {ingredient}": melt certain ingredient
    - "crack {ingredient}": such as crack eggs
    - "simmer"
    
    Then, you need to organize these subtasks into a nested list based on which 
    one can happen in parallel and which one should happen first.
    You must follow these rules:
    - If subtask A and subtask B can happen in parallel, they must be on the same 
    level in the list. For example:
    ‘‘‘
    - subtask A
    - subtask B
    ‘‘‘
    - If subtask B must happen after subtask A, subtask B should be in a nested 
    list under subtask A. For example:
    ‘‘‘
    - subtask A
        * subtask B
    ‘‘‘
    Your input will be under
    # Ingredients
    
    # Raw recipe instruction list.
    
    You should put your response in this format:
    
    # Identify subtasks
    The subtasks in the recipes are: ...
    
    # Reasoning
    ...
    
    # Subtasks as nested list:
    ...
    
    Example:
    - description:
    - observation:
        # Ingredients
        [’1 tablespoon butter’, ’1/2 cup chopped onion’, ’1/2 cup
        chopped celery’, ’4 (14.5 ounce) cans chicken broth’, ’1
        (14.5 ounce) can vegetable broth’, ’1/2 pound chopped cooked
        chicken breast’, ’1 1/2 cups egg noodles’, ’1 cup sliced
        carrots’, ’1/2 teaspoon dried basil’, ’1/2 teaspoon dried
        oregano’, ’salt and ground black pepper to taste’]
        # Raw recipe instruction list.
        1. Melt butter in a large pot over medium heat. Add onion and
        celery and cook until just tender, about 5 minutes.
        2. Add chicken broth, vegetable broth, chicken, egg noodles,
        carrots, basil, oregano, salt, and pepper. Stir to combine
        and bring to a boil.
        3. Reduce heat and simmer for 20 minutes.
    - response:
        # Identify subtasks
        The subtasks in the recipes are: "fetch butter", "fetch onion",
        "fetch celery", "fetch chicken broth", "fetch vegetable
        broth", "fetch chicken", "fetch egg noodles", "fetch carrots",
        "fetch basil", "fetch aregano", "fetch salt", "fetch
        pepper", "melt butter", "pour onion into pot", "pour celery
        into pot", "stir pot", "cook for 5 minutes" "pour chicken
        broth into pot", "pour vegetable broth into pot", "pour
        chicken into pot", "pour egg noodels into pot", "poor
        carrots into pot", "pour basil into pot", "pour oregano into
        pot", "season soup with salt", "season soup with pepper", "
        stir pot", "simmer for 20 minutes"
        
        # Reasoning
        We should fetch all the ingredients first, but fetching the
        ingredients should happen in parallel.
        After fetching butter, we can melt butter.
        After melting butter, we can pour onion and celery into the pot.
        After pouring onion and celery into the pot, we can stir the pot 
        to cook.
        After cooking, we can pour rest of the ingredients into the pot.
        After adding all the ingredients, we can stir the pot again.
        After stirring, we can leave the pot to simmer.
    
    The content mentioned above is a guideline for your thinking process.
    Do NOT output any explanations, reasoning, or other sections.
    Just output the section starting with '# Subtasks as nested list:' and 
    the list itself.
"""
    
example = """
    Can you help me with a recipe of chicken vegetable soup?
"""

assistant_prompt = """
    Output subtasks as nested list in markdown format. Only output the list, no other text.
        - fetch butter
            * melt butter
                + pour onion into pot
                + pour celery into pot
                    - stir pot
                        * cook for 5 minutes
                            + pour chicken broth into pot
                            + pour vegetable broth into pot
                            + pour chicken into pot
                            + pour egg noodles into pot
                            + pour carrots into pot
                            + pour basil into pot
                            + pour oregano into pot
                            + season soup with salt
                            + season soup with pepper
                                - stir pot
                                    * simmer for 20 minutes
        - fetch onion
        - fetch celery
        - fetch chicken broth
        - fetch vegetable broth
        - fetch egg noodles
        - fetch carrots
        - fetch basil
        - fetch aregano
        - fetch salt
        - fetch pepper
"""