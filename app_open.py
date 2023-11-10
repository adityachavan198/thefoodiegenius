import streamlit as st
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

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
weight = st.number_input("Enter your weight (in kilograms)", min_value=50, step=1)
fitness_goals_options = ["Weight Loss", "Muscle Gain", "Maintaining Weight", "Other"]
selected_fitness_goal = st.selectbox("Select your fitness goal", fitness_goals_options)
food_preference_options = ["Hindu", "Jain", "Vegetarian", "Vegan", "Gluten-free"]  # Add more options as needed
selected_food_preference = st.selectbox("Select food preference", food_preference_options)
cuisine_type_options = ["Italian", "Asian", "Mexican", "Mediterranean", "Other"]
cuisine_type = st.selectbox("Select preferred cuisine type", cuisine_type_options)

dietary_restrictions_options = ["Low-carb", "Nut-free", "Vegan", "Vegetarian", "Other"]
dietary_restrictions = st.selectbox("Select dietary restrictions or preferences", dietary_restrictions_options)

# Number of recipes to generate
num_recipes = st.number_input("Number of recipes to generate", min_value=1, max_value=10, step=1, value=1)

# Generate button
if st.button("Generate Recipes"):
    recipes = []
    for _ in range(num_recipes):
        # Construct the prompt based on user input
        prompt = f"Recipe for a {age}-year-old"
        if selected_fitness_goal:
            prompt += f" with a goal of {selected_fitness_goal.lower()} -"
        if height and weight:
            prompt += f" {height} cm tall and {weight} kg -"
        if selected_food_preference:
            prompt += f" {selected_food_preference} -"
        if cuisine_type:
            prompt += f" {cuisine_type} influenced -"
        if dietary_restrictions:
            prompt += f" {dietary_restrictions} -"
        prompt += "Ingredients:"

        # Tokenize and generate text using GPT-2
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=400, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
        
        # Decode the generated text
        recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
        recipes.append(recipe)

    
    # Display the generated recipes
    for idx, recipe in enumerate(recipes, start=1):
        st.markdown(f"**Recipe {idx}:** {recipe}")