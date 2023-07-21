import streamlit as st
import pickle
import requests
import numpy as np
import pandas as pd

# Fetch characters data from the API
def fetch_characters_data():
    api_data = requests.get("https://thronesapi.com/api/v2/Characters").json()
    return api_data

# Preprocess the data
def preprocess_data(df):
    character_replacements = {
        'Jaime': 'Jamie',
        'Lord Varys': 'Varys',
        'Bronn': 'Lord Bronn',
        'Sandor Clegane': 'The Hound',
        'Robb Stark': 'Rob Stark',
        'Eddard Stark': 'Ned Stark',
    }
    df['character'] = df['character'].replace(character_replacements)
    return df.head(25)

# Fetch image URL based on character name
def fetch_image_url(character_name, api_data):
    for item in api_data:
        if item['fullName'] == character_name:
            return item['imageUrl']

# Find the recommended character
def find_recommended_character(selected_character, df):
    character_id = np.where(df['character'].values == selected_character)[0][0]
    x = df[['x', 'y']].values
    distances = [np.linalg.norm(x[character_id] - x[i]) for i in range(len(x))]
    recommended_id = sorted(list(enumerate(distances)), key=lambda x: x[1])[1][0]
    recommended_character = df['character'].values[recommended_id]
    return recommended_character

def main():
    st.title("Game Of Thrones Personality Matcher")

    # Load data
    df = pickle.load(open('data_up.pkl', 'rb'))
    df = preprocess_data(df)

    # Fetch characters data from API
    api_data = fetch_characters_data()

    characters = df['character'].values
    selected_character = st.selectbox("Select a character", characters)

    # Find recommended character
    recommended_character = find_recommended_character(selected_character, df)

    image_url = fetch_image_url(selected_character, api_data)
    recommended_character_image_url = fetch_image_url(recommended_character, api_data)

    col1, col2 = st.columns(2)

    with col1:
        st.header(selected_character)
        st.image(image_url)

    with col2:
        st.header(recommended_character)
        st.image(recommended_character_image_url)

if __name__ == "__main__":
    main()
