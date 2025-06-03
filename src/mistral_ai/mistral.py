# import os
# import base64
# from datetime import datetime
# from mistralai import Mistral

# class MistralVLM:
#     def __init__(self):
#         self.api_key = os.environ.get("MISTRAL_API_KEY")
#         if not self.api_key:
#             raise ValueError("MISTRAL_API_KEY not found in environment variables")
#         self.client = Mistral(api_key=self.api_key)
#         self.text_model = "mistral-large-latest"
#         self.vision_model = "pixtral-12b-2409"
    
#     def encode_image(self, image_path):
#         """Encode image to base64 format"""
#         try:
#             with open(image_path, "rb") as image_file:
#                 return base64.b64encode(image_file.read()).decode('utf-8')
#         except FileNotFoundError:
#             print(f"❌ Error: File {image_path} not found")
#             return None
#         except Exception as e:
#             print(f"❌ Image encoding error: {e}")
#             return None
    
#     def get_image_mime_type(self, image_path):
#         """Determine MIME type based on file extension"""
#         file_ext = os.path.splitext(image_path)[1].lower()
#         mime_types = {
#             '.png': 'image/png',
#             '.gif': 'image/gif',
#             '.bmp': 'image/bmp',
#             '.webp': 'image/webp',
#             '.jpg': 'image/jpeg',
#             '.jpeg': 'image/jpeg'
#         }
#         return mime_types.get(file_ext, 'image/jpeg')
    
#     def chat_with_text(self, text, save_to_file=None):
#         """Text-only conversation"""
#         try:
#             system_prompt = """
#                         Your goal is to convert an internet recipe into a json of subtasks with 
#                         dependencies.
                        
#                         Your first step is to identify subtasks in the recipe. Some examples of the 
#                         subtasks are below, but you can define more subtasks:
#                         - "fetch {ingredient}": gather certain ingredient
#                         - "pour {ingredient} at {location}": pour certain ingredient at a location
#                         - "stir {location}": stir certain location (such as pots, bowls)
#                         - "cut {ingredient}": cut certain ingredient
#                         - "mince {ingredient}": mince certain ingredient
#                         - "toast {food_item}": toast certain food item
#                         - "season {food_item} with {condiment}": season a food item with a condiment 
#                         to the chef’s liking
#                         - "boil {ingredient}": such as boil water
#                         - "place {ingredient} into {location}": put ingredient into a location
#                         - "assemble {food_item}": such as assemble sandwiches
#                         - "stack {ingredient_1} on top of {ingredient_2/food_item}": such as stacking 
#                         tomato on top of cheese or stacking tomato on top of the sandwich
#                         - "melt {ingredient}": melt certain ingredient
#                         - "crack {ingredient}": such as crack eggs
#                         - "simmer"
                        
#                         Then, you need to organize these subtasks into a nested list based on which 
#                         one can happen in parallel and which one should happen first.
#                         You must follow these rules:
#                         - If subtask A and subtask B can happen in parallel, they must be on the same 
#                         level in the list. For example:
#                         ‘‘‘
#                         - subtask A
#                         - subtask B
#                         ‘‘‘
#                         - If subtask B must happen after subtask A, subtask B should be in a nested 
#                         list under subtask A. For example:
#                         ‘‘‘
#                         - subtask A
#                             * subtask B
#                         ‘‘‘
#                         Your input will be under
#                         # Ingredients
                        
#                         # Raw recipe instruction list.
                        
#                         You should put your response in this format:
                        
#                         # Identify subtasks
#                         The subtasks in the recipes are: ...
                        
#                         # Reasoning
#                         ...
                        
#                         # Subtasks as nested list:
#                         ...
                        
#                         Example:
#                         - description:
#                         - observation:
#                             # Ingredients
#                             [’1 tablespoon butter’, ’1/2 cup chopped onion’, ’1/2 cup
#                             chopped celery’, ’4 (14.5 ounce) cans chicken broth’, ’1
#                             (14.5 ounce) can vegetable broth’, ’1/2 pound chopped cooked
#                             chicken breast’, ’1 1/2 cups egg noodles’, ’1 cup sliced
#                             carrots’, ’1/2 teaspoon dried basil’, ’1/2 teaspoon dried
#                             oregano’, ’salt and ground black pepper to taste’]
#                             # Raw recipe instruction list.
#                             1. Melt butter in a large pot over medium heat. Add onion and
#                             celery and cook until just tender, about 5 minutes.
#                             2. Add chicken broth, vegetable broth, chicken, egg noodles,
#                             carrots, basil, oregano, salt, and pepper. Stir to combine
#                             and bring to a boil.
#                             3. Reduce heat and simmer for 20 minutes.
#                         - response:
#                             # Identify subtasks
#                             The subtasks in the recipes are: "fetch butter", "fetch onion",
#                             "fetch celery", "fetch chicken broth", "fetch vegetable
#                             broth", "fetch chicken", "fetch egg noodles", "fetch carrots
#                             ", "fetch basil", "fetch aregano", "fetch salt", "fetch
#                             pepper", "melt butter", "pour onion into pot", "pour celery
#                             into pot", "stir pot", "cook for 5 minutes" "pour chicken
#                             broth into pot", "pour vegetable broth into pot", "pour
#                             chicken into pot", "pour egg noodels into pot", "poor
#                             carrots into pot", "pour basil into pot", "pour oregano into
#                             pot", "season soup with salt", "season soup with pepper", "
#                             stir pot", "simmer for 20 minutes"
                            
#                             # Reasoning
#                             We should fetch all the ingredients first, but fetching the
#                             ingredients should happen in parallel.
#                             After fetching butter, we can melt butter.
#                             After melting butter, we can pour onion and celery into the pot.
#                             After pouring onion and celery into the pot, we can stir the pot 
#                             to cook.
#                             After cooking, we can pour rest of the ingredients into the pot.
#                             After adding all the ingredients, we can stir the pot again.
#                             After stirring, we can leave the pot to simmer.
                        
#                         The content mentioned above is a guideline for your thinking process.
#                         Do NOT output any explanations, reasoning, or other sections.
#                         Just output the section starting with '# Subtasks as nested list:' and 
#                         the list itself.
#                         """
#             assistant_prompt = """
#                             # Subtasks as nested list:
#                                 - fetch butter
#                                     * melt butter
#                                         + pour onion into pot
#                                         + pour celery into pot
#                                             - stir pot
#                                                 * cook for 5 minutes
#                                                     + pour chicken broth into pot
#                                                     + pour vegetable broth into pot
#                                                     + pour chicken into pot
#                                                     + pour egg noodles into pot
#                                                     + poor carrots into pot
#                                                     + pour basil into pot
#                                                     + pour oregano into pot
#                                                     + season soup with salt
#                                                     + season soup with pepper
#                                                         - stir pot
#                                                             * simmer for 20 minutes
#                                 - fetch onion
#                                 - fetch celery
#                                 - fetch chicken broth
#                                 - fetch vegetable broth
#                                 - fetch egg noodles
#                                 - fetch carrots
#                                 - fetch basil
#                                 - fetch aregano
#                                 - fetch salt
#                                 - fetch pepper
#                             """

#             chat_response = self.client.chat.complete(
#                 model=self.text_model,
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": system_prompt
#                     },
#                     # Example
#                     {
#                         "role": "user",
#                         "content": "Can you help me with a recipe of chicken vegetable soup?"
#                     },
#                     {
#                         "role": "assistant",
#                         "content": assistant_prompt
#                     },
#                     {
#                         "role": "user",
#                         "content": text,
#                     },
#                 ]
#             )
            
#             response_text = chat_response.choices[0].message.content
#             print(f"🤖 LLM Response:")
#             print(f"{response_text}")
#             print()
            
#             # Save to file (if specified)
#             if save_to_file:
#                 self._save_response_to_file(response_text, save_to_file, text)
            
#             return response_text
            
#         except Exception as e:
#             print(f"❌ Text model call error: {e}")
#             return None
    
#     def chat_with_vision(self, text, image_path, save_to_file=None):
#         """Image + text conversation (using vision model)"""
#         try:
#             print(f"🖼️  Encoding image: {os.path.basename(image_path)}")
#             base64_image = self.encode_image(image_path)
            
#             if not base64_image:
#                 print("❌ Image encoding failed, switching to text-only mode")
#                 return self.chat_with_text(text, save_to_file)
            
#             mime_type = self.get_image_mime_type(image_path)
            
#             # Prepare message content
#             content = [
#                 {
#                     "type": "text",
#                     "text": text
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": f"data:{mime_type};base64,{base64_image}"
#                 }
#             ]
            
#             print("🤖 Calling vision model...")
#             chat_response = self.client.chat.complete(
#                 model=self.vision_model,
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": content
#                     }
#                 ]
#             )
            
#             response_text = chat_response.choices[0].message.content
#             print(f"🤖 VLM Response:")
#             print(f"{response_text}")
#             print()
            
#             # Save to file (if specified)
#             if save_to_file:
#                 image_info = f" (with image: {os.path.basename(image_path)})"
#                 self._save_response_to_file(response_text, save_to_file, text, image_info)
            
#             return response_text
            
#         except Exception as e:
#             print(f"❌ Vision model call error: {e}")
#             return None
    
#     def _save_response_to_file(self, response, file_path, original_text, image_info=""):
#         """Save response to file"""
#         try:
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             with open(file_path, "a", encoding="utf-8") as f:
#                 f.write(f"[{timestamp}] LLM Response{image_info}: {response}\n")
#         except Exception as e:
#             print(f"❌ Error saving response to file: {e}")
    
#     def get_latest_transcription_text(self, file_path):
#         """Get the latest transcription text from file"""
#         try:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 lines = f.readlines()
#                 if not lines:
#                     return ""
#                 last_line = lines[-1].strip()
#                 if "]" in last_line:
#                     return last_line.split("]", 1)[1].strip()
#                 return last_line
#         except Exception as e:
#             print(f"❌ Error reading transcription file: {e}")
#             return ""

# def select_image_file():
#     """Select image file"""
#     try:
#         print("📁 Please enter the path to your image file:")
#         print("   (Supported formats: jpg, jpeg, png, gif, bmp, webp)")
#         print("   Enter the full path)")
        
#         file_path = input("🖼️  Image path: ").strip()
        
#         # Check if file exists and is an image
#         if file_path and os.path.exists(file_path):
#             # Check file extension
#             valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
#             if file_path.lower().endswith(valid_extensions):
#                 print(f"✅ Image selected: {os.path.basename(file_path)}")
#                 return file_path
#             else:
#                 print(f"❌ Error: {file_path} is not a supported image format")
#                 return None
#         elif file_path:
#             print(f"❌ Error: File not found: {file_path}")
#             return None
#         else:
#             print("❌ No file path provided")
#             return None
        
#     except Exception as e:
#         print(f"❌ Error selecting image: {e}")
#         return None

# def ask_image_selection(text):
#     """Ask user whether to add an image"""
#     # Check if transcribed text mentions image-related keywords
#     choice = input("🖼️  Do you want to add an image for analysis? (y/n): ").strip()
    
#     # Check if user input looks like a file path instead of y/n
#     if choice.startswith('/') or choice.startswith('./') or choice.startswith('~'):
#         print(f"🤖 I detected a file path in your input: {choice}")
#         print("   Let me use this as the image file...")
#         # Validate path (don't convert file paths to lowercase!)
#         if os.path.exists(choice):
#             valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
#             if choice.lower().endswith(valid_extensions):
#                 print(f"✅ Using image: {os.path.basename(choice)}")
#                 return choice
#             else:
#                 print(f"❌ Error: {choice} is not a supported image format")
#                 return None
#         else:
#             print(f"❌ Error: File not found: {choice}")
#             return None
#     elif choice.lower() in ['y', 'yes', '是', '好']:  # Only convert to lowercase for y/n comparison
#         return select_image_file()
#     else:
#         print("📝 Proceeding with text-only analysis...")
#         return None

import os
import base64
from datetime import datetime
from mistralai import Mistral

class Mistralmodel:
    def __init__(self):
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        self.client = Mistral(api_key=self.api_key)
        self.text_model = "mistral-large-latest"
        self.vision_model = "pixtral-large-latest" # "pixtral-12b-2409"
    
    def encode_image(self, image_path):
        """Encode image to base64 format"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"❌ Error: File {image_path} not found")
            return None
        except Exception as e:
            print(f"❌ Image encoding error: {e}")
            return None
    
    def get_image_mime_type(self, image_path):
        """Determine MIME type based on file extension"""
        file_ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg'
        }
        return mime_types.get(file_ext, 'image/jpeg')
    
    def chat_with_text(self, text, system_prompt, example, assistant_prompt):
        """Text-only conversation"""
        try:
            chat_response = self.client.chat.complete(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    # Example
                    {
                        "role": "user",
                        "content": example
                    },
                    {
                        "role": "assistant",
                        "content": assistant_prompt
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ]
            )
            
            response_text = chat_response.choices[0].message.content
            
            return response_text
            
        except Exception as e:
            print(f"❌ Text model call error: {e}")
            return None
    
    def chat_with_vision(self, text, image_path, system_prompt, example, assistant_prompt):
        """Image + text conversation (using vision model)"""
        try:
            print(f"🖼️  Encoding image: {os.path.basename(image_path)}")
            base64_image = self.encode_image(image_path)
            
            mime_type = self.get_image_mime_type(image_path)
            
            # Prepare message content
            content = [
                {
                    "type": "text",
                    "text": text
                },
                {
                    "type": "image_url",
                    "image_url": f"data:{mime_type};base64,{base64_image}"
                }
            ]
            
            print("🤖 Calling vision model...")
            chat_response = self.client.chat.complete(
                model=self.vision_model,
                messages=[
                    
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    # Example
                    {
                        "role": "user",
                        "content": example
                    },
                    {
                        "role": "assistant",
                        "content": assistant_prompt
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            
            response_text = chat_response.choices[0].message.content
            
            return response_text
            
        except Exception as e:
            print(f"❌ Vision model call error: {e}")
            return None
    

    


