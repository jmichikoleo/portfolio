import streamlit as st
import pandas as pd
import requests

API_KEY = "BbaE4PsYR9sR1FKDkwZi6WJG6ZG4kNntBu6f0mUt"

def fetch_calorie_data(food_name):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={food_name}&pageSize=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("foods"):
            food = data["foods"][0]
            nutrients = {n['nutrientName']: n['value'] for n in food.get("foodNutrients", [])}
            return {
                "description": food.get("description", "Unknown"),
                "calories": nutrients.get("Energy", "N/A"),
            }
    return None

if 'food_log' not in st.session_state:
    st.session_state['food_log'] = []

st.title("Calorie Counter -- USDA API")

st.subheader("Search Food")
food_name = st.text_input("Enter a food name (e.g., Apple, Rice):")
if st.button("Search"):
    if food_name:
        result = fetch_calorie_data(food_name)
        if result:
            st.write(f"**{result['description']}**: {result['calories']} kcal per 100g")
        else:
            st.error("No data found. Try another food.")
    else:
        st.error("Please enter a food name.")

st.subheader("Log Your Meal")
with st.form("calorie_form"):
    meal_name = st.text_input("Meal Name (e.g., Breakfast, Lunch)")
    food_item = st.text_input("Food Item (use search results or custom)")
    calories = st.number_input("Calories (kcal per serving)", min_value=0, step=1)
    quantity = st.number_input("Quantity (servings)", min_value=1, step=1)
    submitted = st.form_submit_button("Add to Log")

if submitted:
    if meal_name and food_item:
        total_calories = calories * quantity
        st.session_state['food_log'].append({
            "Meal": meal_name,
            "Food Item": food_item,
            "Calories per Serving": calories,
            "Quantity": quantity,
            "Total Calories": total_calories,
        })
        st.success(f"Added {food_item} to {meal_name} with {total_calories} kcal.")
    else:
        st.error("Please fill out all fields.")

# Display the food log
st.subheader("Food Log")
if st.session_state['food_log']:
    df = pd.DataFrame(st.session_state['food_log'])
    st.table(df)
    st.write(f"**Total Calories for the Day:** {df['Total Calories'].sum()}")
else:
    st.write("No meals logged yet.")

if st.button("Clear Log"):
    st.session_state['food_log'] = []
    st.success("Log cleared!")
