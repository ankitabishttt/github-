import tkinter as tk
from tkinter import ttk, messagebox

# --- GUI Setup ---
root = tk.Tk()
root.title("Personalized Diet and Fitness Planner")
root.geometry("600x600")

# --- Input Fields ---
tk.Label(root, text="Age:").grid(row=0, column=0, sticky='e')
age_entry = tk.Entry(root)
age_entry.grid(row=0, column=1)

tk.Label(root, text="Gender:").grid(row=1, column=0, sticky='e')
gender_var = tk.StringVar()
gender_combo = ttk.Combobox(root, textvariable=gender_var, values=["Male", "Female"])
gender_combo.grid(row=1, column=1)

tk.Label(root, text="Height (in meters):").grid(row=2, column=0, sticky='e')
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

tk.Label(root, text="Weight (in kg):").grid(row=3, column=0, sticky='e')
weight_entry = tk.Entry(root)
weight_entry.grid(row=3, column=1)

tk.Label(root, text="Activity Level:").grid(row=4, column=0, sticky='e')
activity_var = tk.StringVar()
activity_combo = ttk.Combobox(root, textvariable=activity_var, values=["Sedentary", "Moderate", "Active"])
activity_combo.grid(row=4, column=1)

tk.Label(root, text="Dietary Restrictions:").grid(row=5, column=0, sticky='e')
restrictions_entry = tk.Entry(root)
restrictions_entry.grid(row=5, column=1)

tk.Label(root, text="Fitness Goal:").grid(row=6, column=0, sticky='e')
goal_var = tk.StringVar()
goal_combo = ttk.Combobox(root, textvariable=goal_var, values=["Weight Loss", "Muscle Gain", "Maintain"])
goal_combo.grid(row=6, column=1)

# --- Output Text Widget with Scrollbar ---
output_frame = tk.Frame(root)
output_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

output_text = tk.Text(output_frame, height=20, width=70, wrap=tk.WORD)
scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
output_text.configure(yscrollcommand=scrollbar.set)

output_text.grid(row=0, column=0)
scrollbar.grid(row=0, column=1, sticky='ns')

# --- Logic Functions (Your Existing Code) ---
def run_program():
    try:
        age = int(age_entry.get())
        gender = gender_var.get().lower()
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        activity_level = activity_var.get().lower()
        dietary_restrictions = restrictions_entry.get().lower()
        fitness_goal = goal_var.get().lower()

        bmi = weight / (height ** 2)

        if gender == 'male':
            bmr = (10 * weight) + (6.25 * height * 100) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height * 100) - (5 * age) - 161

        activity_multipliers = {
            'sedentary': 1.2,
            'moderate': 1.55,
            'active': 1.725
        }
        calorie_needs = bmr * activity_multipliers.get(activity_level, 1.2)

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"BMI: {bmi:.2f}\n")
        output_text.insert(tk.END, f"Daily Calorie Needs: {calorie_needs:.2f} calories\n\n")
        output_text.insert(tk.END, "Generating your diet plan...\n")
        output_text.update_idletasks()

        run_program.bmi = bmi
        run_program.calorie_needs = calorie_needs
        run_program.goal = fitness_goal
        run_program.restrictions = dietary_restrictions
        run_program.activity = activity_level

        root.after(1000, generate_macros)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values for age, height, and weight.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def generate_macros():
    calorie_needs = run_program.calorie_needs
    goal = run_program.goal

    protein_percentage = 0.3 if goal == 'muscle gain' else 0.25
    carb_percentage = 0.45 if goal == 'muscle gain' else 0.5
    fat_percentage = 0.25

    protein_grams = (calorie_needs * protein_percentage) / 4
    carb_grams = (calorie_needs * carb_percentage) / 4
    fat_grams = (calorie_needs * fat_percentage) / 9

    output_text.insert(tk.END, f"Macronutrient goals:\n")
    output_text.insert(tk.END, f"Protein: {protein_grams:.2f} grams\n")
    output_text.insert(tk.END, f"Carbohydrates: {carb_grams:.2f} grams\n")
    output_text.insert(tk.END, f"Fats: {fat_grams:.2f} grams\n\n")
    output_text.insert(tk.END, "Sample Meal Plan:\n")
    output_text.update_idletasks()

    root.after(1000, generate_meal_plan)

def generate_meal_plan():
    restrictions = run_program.restrictions

    if "vegetarian" in restrictions:
        output_text.insert(tk.END, "- Breakfast: Oatmeal with fruits and nuts\n")
        output_text.insert(tk.END, "- Lunch: Lentil soup with whole-grain bread\n")
        output_text.insert(tk.END, "- Dinner: Tofu stir-fry with brown rice\n")
        output_text.insert(tk.END, "- Snacks: Fruits, vegetables, yogurt\n")
    else:
        output_text.insert(tk.END, "- Breakfast: Eggs with whole-wheat toast and avocado\n")
        output_text.insert(tk.END, "- Lunch: Grilled chicken salad\n")
        output_text.insert(tk.END, "- Dinner: Baked salmon with roasted vegetables\n")
        output_text.insert(tk.END, "- Snacks: Fruits, nuts, Greek yogurt\n")

    if "gluten-free" in restrictions:
        output_text.insert(tk.END, "\nNote: Please ensure all grains are gluten-free.\n")
    if "nuts" in restrictions:
        output_text.insert(tk.END, "\nNote: Please avoid nuts and nut products.\n")

    output_text.insert(tk.END, "\nGenerating your exercise recommendations...\n")
    output_text.update_idletasks()
    root.after(1000, generate_exercise)

def generate_exercise():
    goal = run_program.goal
    activity = run_program.activity

    output_text.insert(tk.END, "\nExercise Recommendations:\n")
    if goal == 'weight loss':
        output_text.insert(tk.END, "- Cardio: 30-45 minutes of brisk walking, jogging, or cycling most days of the week.\n")
        output_text.insert(tk.END, "- Strength training: 2-3 times per week, focusing on compound exercises.\n")
    elif goal == 'muscle gain':
        output_text.insert(tk.END, "- Strength training: 3-4 times per week, focusing on progressive overload.\n")
        output_text.insert(tk.END, "- Cardio: 1-2 times per week, moderate intensity.\n")
    else:
        output_text.insert(tk.END, "- Maintain a balanced routine of cardio and strength training.\n")

    if activity == 'sedentary':
        output_text.insert(tk.END, "\nStart with light activities and gradually increase intensity.\n")

    output_text.insert(tk.END, "\nDisclaimer: This is a basic diet and exercise plan. Consult a professional for personalized advice.")
    output_text.update_idletasks()

# --- Button ---
run_button = tk.Button(root, text="Generate Plan", command=run_program)
run_button.grid(row=8, column=0, columnspan=2, pady=10)


root.mainloop()
