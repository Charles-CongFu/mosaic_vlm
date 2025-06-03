system_prompt = """
            Your goal is to analyze an image and identify all the objects in it. 
            If there are text labels on the objects, please list them as well and output in JSON format.
            
            You should follow these steps:
            1. Analyze the image to identify objects.
            2. If there are text labels on the objects, extract them.
            3. Output the identified objects and their labels in a structured JSON format.
            
            Example:
            - description: "A kitchen with various ingredients."
            - observation:
                {
                    "objects": [
                        {"name": "apple", "label": "red apple"},
                        {"name": "bowl", "label": "ceramic bowl"},
                        {"name": "knife", "label": "kitchen knife"}
                    ]
                }
            
            Your input will be under
            # Image
            [Image data here]
            
            You should put your response in this format:
            
            # Identified objects
            The identified objects in the image are: ...
            
            # Reasoning
            ...
            
            # Objects as JSON:
            ...
"""
example = """
            Tell me what objects are in this image.
"""

assistant_prompt = """
            The identified objects in the image are: 
            {
                "objects": [
                    {"name": "apple", "label": "red apple", "color": "red"},
                    {"name": "bowl", "label": "ceramic bowl", "color": "white"},
                    {"name": "knife", "label": "kitchen knife", "color": "silver"}
                ]
            }
            Remember, name, label and color are the only fields you need to fill in for each object.
"""

user_prompt = """
            Analyze the image and identify all the objects in it. If there are text labels on the objects, please list them as well and output in JSON format.
"""