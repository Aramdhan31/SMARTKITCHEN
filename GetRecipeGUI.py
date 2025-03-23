import openai
from tkinter import *
from tkinter import scrolledtext, messagebox

# 🔹 ChatGPT API Key
api_key = "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"
openai.api_key = api_key

# Placeholder Text
placeholder_text = "Enter a food name"

# 🔹 Function to get Recipe
def get_recipe():
    food_item = food_entry.get().strip()

    if not food_item or food_item == placeholder_text:
        messagebox.showerror("Error", "Please enter a food item.")
        return

    try:
        prompt = (
            f"Provide a detailed, authentic recipe for {food_item}. "
            "Include a list of ingredients, step-by-step instructions, prep time, cooking time, servings, and any additional notes. "
            "If the exact recipe is not found, suggest a similar alternative. "
            "Do not say it is not a food; instead, provide the closest related recipe."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef and culinary expert. Provide detailed recipes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        # Colour Formatting to Recipe
        recipe_text.delete("1.0", END)
        formatted_text = response['choices'][0]['message']['content']

        recipe_text.tag_configure("title", foreground="blue", font=("Microsoft YaHei UI Light", scale_y(20), "bold"))
        recipe_text.tag_configure("ingredients", foreground="darkorange", font=("Microsoft YaHei UI Light", scale_y(18), "bold"))
        recipe_text.tag_configure("instructions", foreground="black", font=("Microsoft YaHei UI Light", scale_y(18)))
        recipe_text.tag_configure("prep", foreground="green", font=("Microsoft YaHei UI Light", scale_y(18)))
        recipe_text.tag_configure("cooking", foreground="purple", font=("Microsoft YaHei UI Light", scale_y(18)))
        recipe_text.tag_configure("servings", foreground="brown", font=("Microsoft YaHei UI Light", scale_y(18)))
        recipe_text.tag_configure("notes", foreground="gray", font=("Microsoft YaHei UI Light", scale_y(18)))

        # Format Recipe Output
        lines = formatted_text.split("\n")
        prep_line = ""
        cooking_line = ""
        servings_line = ""
        ingredients_start = -1

        for i, line in enumerate(lines):
            line = line.strip()
            if "Prep Time:" in line:
                prep_line = line + "\n"
            elif "Cooking Time:" in line:
                cooking_line = line + "\n"
            elif "Servings:" in line:
                servings_line = line + "\n"
            elif "Ingredients:" in line:
                ingredients_start = i
                break

        if ingredients_start != -1:
            if prep_line:
                recipe_text.insert(END, prep_line, "prep")
            if cooking_line:
                recipe_text.insert(END, cooking_line, "cooking")
            if servings_line:
                recipe_text.insert(END, servings_line, "servings")

            for i in range(ingredients_start, len(lines)):
                line = lines[i].strip()
                if "Ingredients:" in line:
                    recipe_text.insert(END, line + "\n", "ingredients")
                elif "Instructions:" in line:
                    recipe_text.insert(END, line + "\n", "title")
                elif "Notes:" in line:
                    recipe_text.insert(END, line + "\n", "notes")
                else:
                    recipe_text.insert(END, line + "\n", "instructions")
        else:
            for line in lines:
                line = line.strip()
                if "Ingredients:" in line:
                    recipe_text.insert(END, line + "\n", "ingredients")
                elif "Instructions:" in line:
                    recipe_text.insert(END, line + "\n", "title")
                elif "Notes:" in line:
                    recipe_text.insert(END, line + "\n", "notes")
                else:
                    recipe_text.insert(END, line + "\n", "instructions")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch recipe: {str(e)}")

# 🔹 Placeholder Functions
def on_entry_click(event):
    if food_entry.get() == placeholder_text:
        food_entry.delete(0, "end")
        food_entry.config(fg="black")

def on_focus_out(event):
    if food_entry.get() == "":
        food_entry.insert(0, placeholder_text)
        food_entry.config(fg="gray")

# GUI Fullscreen
def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    window.attributes("-fullscreen", is_fullscreen)

# 🔹 GUI Setup
window = Tk()
window.title("Recipe Finder")
window.attributes("-fullscreen", True)  # Start in Fullscreen mode
window.configure(bg="#f5f5f5")  # Light background for better contrast
is_fullscreen = True

# Get screen dimensions for scaling
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

def scale_x(x):
    return int(x * screen_width / 1366)

def scale_y(y):
    return int(y * screen_height / 768)

# 🔹 Title Label (Green for Visibility)
Label(window, text="Recipe Finder", fg="green", bg="#f5f5f5", font=("Microsoft YaHei UI Light", scale_y(30), "bold")).pack(pady=scale_y(20))

# 🔹 Entry Box for Food Name
food_entry = Entry(window, width=40, font=("Microsoft YaHei UI Light", scale_y(15)), border=2, fg="gray")
food_entry.pack(pady=scale_y(10))
food_entry.insert(0, placeholder_text)
food_entry.bind("<FocusIn>", on_entry_click)
food_entry.bind("<FocusOut>", on_focus_out)

# 🔹 Button to Fetch Recipe (Green for Action)
Button(window, text="Get Recipe", font=("Microsoft YaHei UI Light", scale_y(15)), bg="green", fg="black", command=get_recipe).pack(pady=scale_y(10))

# 🔹 Scrollable Text Box for Recipe Output (Color Coded)
recipe_text = scrolledtext.ScrolledText(window, width=scale_x(80), height=scale_y(18), font=("Microsoft YaHei UI Light", scale_y(20)), wrap="word", bg="#ffffff", fg="black")
recipe_text.pack(pady=scale_y(10), padx=scale_x(20), fill="both", expand=True)

# 🔹 Bottom Buttons Frame
bottom_frame = Frame(window, bg="#f5f5f5")
bottom_frame.pack(pady=scale_y(10))

# 🔹 Exit Button (Red for Danger)
Button(bottom_frame, text="Exit", font=("Microsoft YaHei UI Light", scale_y(15)), bg="red", fg="black", command=window.destroy).pack(side=LEFT, padx=scale_x(10))

# 🔹 Run GUI
window.mainloop()