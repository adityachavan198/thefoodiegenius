import streamlit as st
import openai
import os
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def get_recipe_images(recipes):
    img_urls = []
    dish_names = [recipe.split('\n')[0] for recipe in recipes]
    print(recipes)
    for dish_name in dish_names:
        # Replace YOUR_UNSPLASH_ACCESS_KEY with your Unsplash access key
        print("Dish Name\n", dish_name, "Dish Name\n")
        url = f"https://api.unsplash.com/photos/random?query={dish_name}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.json()
            if img_data and 'urls' in img_data:
                img_urls.append(img_data['urls']['regular'])
    return img_urls

# Set page title and favicon
st.set_page_config(
    page_title="Food Recipe Generator",
    page_icon="🍳",
    layout="wide"
)

# Set background color and title
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .title {
        font-size: 36px;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# User inputs
st.title("Food Recipe Generator")
age = st.number_input("Enter your age", min_value=18, step=1)
height = st.number_input("Enter your height (in centimeters)", min_value=120, step=1)
weight = st.number_input("Enter your weight (in kilograms)", min_value=55, step=1)
fitness_goals_options = ["Weight Loss", "Muscle Gain", "Maintaining Weight", "Other"]
selected_fitness_goal = st.selectbox("Select your fitness goal", fitness_goals_options)
protein_preference_options = [ "Vegetarian", "Chicken", "Fish", "Shrimp", "Vegan", "Pork", "Mutton", "Beef"]  # Add more options as needed
selected_protein_preference = st.selectbox("Select food preference", protein_preference_options)
cuisine_type_options = ["Indian", "Italian", "Asian", "Mexican", "Mediterranean", "Other"]
cuisine_type = st.selectbox("Select preferred cuisine type", cuisine_type_options)

dietary_restrictions_options = ["Low-carb", "Nut-free", "Vegan", "Vegetarian", ""]
dietary_restrictions = st.selectbox("Select dietary restrictions or preferences", dietary_restrictions_options)

# Number of recipes to generate
num_recipes = st.number_input("Number of recipes to generate", min_value=1, max_value=10, step=1, value=1)

# Generate button
if st.button("Generate Recipes"):
    recipes = []
    for _ in range(num_recipes):
        # Construct the prompt based on user input
        prompt = f"Generate a recipe suitable for a {age}-year-old"
        if selected_fitness_goal:
            prompt += f" with a goal of {selected_fitness_goal.lower()}"
        if height and weight:
            prompt += f", {height} cm tall, and {weight} kg in weight"
        if selected_protein_preference:
            prompt += f" that is {selected_protein_preference.lower()}"
        if cuisine_type:
            prompt += f" and has a {cuisine_type.lower()} influence"
        if dietary_restrictions:
            prompt += f" while being {dietary_restrictions.lower()}"
        prompt += ". Also, provide the nutritional information."
        
        print(prompt)
        # Make a request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=400  # Adjust the maximum number of tokens based on the desired response length
        )
        
        # Get the generated recipe from the API response
        recipe = response.choices[0].text.strip()
        recipes.append(recipe)
    
    # Display the generated recipes
    for idx, (recipe, img_url) in enumerate(zip(recipes, get_recipe_images(recipes)), start=1):
        st.markdown(f"**Recipe {idx}:** {recipe}")
        st.image(img_url, caption=f"Image for Recipe {idx}", width=300)