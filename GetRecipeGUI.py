import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load API key from .env or hardcoded fallback
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or "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"
openai.api_key = api_key

# Set page config
st.set_page_config(page_title="Recipe Finder", layout="wide")
st.markdown(
    """
    <style>
        .title {
            color: green;
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            font-family: 'Segoe UI', 'Microsoft YaHei UI Light', sans-serif;
        }
        .subtitle {
            font-size: 22px;
            color: gray;
            text-align: center;
        }
        textarea {
            font-size: 18px !important;
            font-family: 'Microsoft YaHei UI Light', sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# UI Layout
st.markdown('<div class="title">Recipe Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter a food name and get a full detailed recipe</div>', unsafe_allow_html=True)
st.write("")

# Input field
food_item = st.text_input("Food Name", value="", placeholder="Enter a food name", label_visibility="collapsed")

# Button
if st.button("🍽️ Get Recipe"):
    if not food_item.strip():
        st.error("Please enter a food item.")
    else:
        with st.spinner("Cooking up your recipe..."):
            try:
                # Prompt
                prompt = (
                    f"Provide a detailed, authentic recipe for {food_item}. "
                    "Include a list of ingredients, step-by-step instructions, prep time, cooking time, servings, and any additional notes. "
                    "If the exact recipe is not found, suggest a similar alternative. "
                    "Do not say it is not a food; instead, provide the closest related recipe."
                )

                # OpenAI request
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional chef and culinary expert. Provide detailed recipes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6
                )

                recipe = response['choices'][0]['message']['content']

                # Format output
                def tag_line(line):
                    if "Prep Time:" in line:
                        return f"<span style='color:green'><b>{line}</b></span><br>"
                    elif "Cooking Time:" in line:
                        return f"<span style='color:purple'><b>{line}</b></span><br>"
                    elif "Servings:" in line:
                        return f"<span style='color:brown'><b>{line}</b></span><br>"
                    elif "Ingredients:" in line:
                        return f"<h4 style='color:darkorange'>{line}</h4>"
                    elif "Instructions:" in line:
                        return f"<h4 style='color:blue'>{line}</h4>"
                    elif "Notes:" in line:
                        return f"<h4 style='color:gray'>{line}</h4>"
                    else:
                        return f"<span style='color:black'>{line}</span><br>"

                styled_recipe = "".join([tag_line(l.strip()) for l in recipe.splitlines() if l.strip()])
                st.markdown(styled_recipe, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Failed to fetch recipe: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using OpenAI + Streamlit", unsafe_allow_html=True)
