from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='')

def calculate_diet_plan(data):
    try:
        age = int(data.get('age'))
        gender = data.get('gender', '').lower()
        height = float(data.get('height'))
        weight = float(data.get('weight'))
        activity_level = data.get('activity_level', '').lower()
        dietary_restrictions = data.get('dietary_restrictions', '').lower()
        fitness_goal = data.get('fitness_goal', '').lower()

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

        protein_percentage = 0.3 if fitness_goal == 'muscle gain' else 0.25
        carb_percentage = 0.45 if fitness_goal == 'muscle gain' else 0.5
        fat_percentage = 0.25

        protein_calories = calorie_needs * protein_percentage
        carb_calories = calorie_needs * carb_percentage
        fat_calories = calorie_needs * fat_percentage

        protein_grams = protein_calories / 4
        carb_grams = carb_calories / 4
        fat_grams = fat_calories / 9

        diet_plan = {
            'bmi': round(bmi, 2),
            'daily_calorie_needs': round(calorie_needs, 2),
            'macronutrient_goals': {
                'protein_grams': round(protein_grams, 2),
                'carbohydrates_grams': round(carb_grams, 2),
                'fats_grams': round(fat_grams, 2)
            },
            'meal_plan': [],
            'notes': [],
            'exercise_recommendations': []
        }

        if "vegetarian" in dietary_restrictions:
            diet_plan['meal_plan'] = [
                "Breakfast: Oatmeal with fruits and nuts",
                "Lunch: Lentil soup with whole-grain bread",
                "Dinner: Tofu stir-fry with brown rice",
                "Snacks: Fruits, vegetables, yogurt"
            ]
        else:
            diet_plan['meal_plan'] = [
                "Breakfast: Eggs with whole-wheat toast and avocado",
                "Lunch: Grilled chicken salad",
                "Dinner: Baked salmon with roasted vegetables",
                "Snacks: Fruits, nuts, Greek yogurt"
            ]

        if "gluten-free" in dietary_restrictions:
            diet_plan['notes'].append("Please ensure all grains are gluten-free.")
        if "nuts" in dietary_restrictions:
            diet_plan['notes'].append("Please avoid nuts and nut products.")

        if fitness_goal == 'weight loss':
            diet_plan['exercise_recommendations'] = [
                "Cardio: 30-45 minutes of brisk walking, jogging, or cycling most days of the week.",
                "Strength training: 2-3 times per week, focusing on compound exercises."
            ]
        elif fitness_goal == 'muscle gain':
            diet_plan['exercise_recommendations'] = [
                "Strength training: 3-4 times per week, focusing on progressive overload.",
                "Cardio: 1-2 times per week, moderate intensity."
            ]
        else:
            diet_plan['exercise_recommendations'] = [
                "Maintain a balanced routine of cardio and strength training."
            ]

        if activity_level == 'sedentary':
            diet_plan['exercise_recommendations'].append("Start with light activities and gradually increase intensity.")

        diet_plan['disclaimer'] = "This is a basic diet and exercise plan. Consult a professional for personalized advice."

        return diet_plan

    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/api/diet', methods=['POST'])
def api_diet():
    data = request.json
    result = calculate_diet_plan(data)
    return jsonify(result)

@app.route('/personalized-diet')
def personalized_diet():
    return send_from_directory('', 'personalized_diet.html')

if __name__ == '__main__':
    app.run(debug=True)
