import streamlit as st
from openai import OpenAI

# ✅ OpenAI API Key
api_key = "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"
client = OpenAI(api_key=api_key)

# ✅ Page setup to mimic Tkinter app
st.set_page_config(page_title="Recipe Finder", layout="centered")

# ✅ Custom CSS to match your layout
st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            font-size: 32px;
            color: green;
            font-weight: bold;
            font-family: 'Segoe UI', 'Microsoft YaHei UI Light', sans-serif;
        }
        .input-style {
            text-align: center;
        }
        .text-box {
            border: 1px solid black;
            padding: 1rem;
            background-color: white;
            height: 400px;
            overflow-y: auto;
            font-family: 'Microsoft YaHei UI Light', sans-serif;
            font-size: 16px;
        }
        .button-container {
            text-align: center;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ UI: Title
st.markdown("<div class='centered-title'>Recipe Finder</div>", unsafe_allow_html=True)
st.write("")

# ✅ UI: Input field
food_item = st.text_input("", placeholder="Enter a food name", label_visibility="collapsed")

# ✅ Button
get_recipe = st.button("Get Recipe")

# ✅ Recipe Output Area
if get_recipe and food_item.strip():
    with st.spinner("Fetching recipe..."):
        try:
            prompt = (
                f"Provide a detailed, authentic recipe for {food_item}. "
                "Include a list of ingredients, step-by-step instructions, prep time, cooking time, servings, and any additional notes. "
                "If the exact recipe is not found, suggest a similar alternative. "
                "Do not say it is not a food; instead, provide the closest related recipe."
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional chef and culinary expert. Provide detailed recipes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )

            recipe = response.choices[0].message.content

            # ✅ Styled text output box
            st.markdown("<div class='text-box'>", unsafe_allow_html=True)
            for line in recipe.split("\n"):
                st.markdown(line)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.markdown("<div class='text-box'></div>", unsafe_allow_html=True)

# ✅ Exit button look-alike (for browser version)
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
if st.button("Exit"):
    st.stop()
st.markdown("</div>", unsafe_allow_html=True)
