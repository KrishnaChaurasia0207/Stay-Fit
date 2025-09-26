#!/usr/bin/env python3
"""
Standalone Demo - Direct meal planning without complex imports
"""

import json
import random
from datetime import datetime

def calculate_bmr_tdee(age, sex, weight_kg, height_cm, activity_level):
    """Calculate BMR and TDEE"""
    # Mifflin-St Jeor formula
    if sex.lower() in ['m', 'male']:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375, 
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extremely_active': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    return bmr, tdee

def get_food_database():
    """Get nutrition database with dietary classifications"""
    return {
        "oatmeal": {"calories": 150, "protein": 5, "carbs": 27, "fat": 3, "cost": 0.35, "allergens": ["gluten"], "dietary_type": "vegan"},
        "banana": {"calories": 90, "protein": 1, "carbs": 23, "fat": 0, "cost": 0.40, "allergens": [], "dietary_type": "vegan"},
        "greek_yogurt": {"calories": 130, "protein": 15, "carbs": 9, "fat": 0, "cost": 1.50, "allergens": ["dairy"], "dietary_type": "vegetarian"},
        "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 4, "cost": 2.50, "allergens": ["chicken"], "dietary_type": "non_vegetarian"},
        "quinoa": {"calories": 110, "protein": 4, "carbs": 20, "fat": 2, "cost": 0.80, "allergens": [], "dietary_type": "vegan"},
        "broccoli": {"calories": 25, "protein": 3, "carbs": 5, "fat": 0, "cost": 0.80, "allergens": [], "dietary_type": "vegan"},
        "salmon": {"calories": 145, "protein": 22, "carbs": 0, "fat": 6, "cost": 4.00, "allergens": ["fish"], "dietary_type": "non_vegetarian"},
        "sweet_potato": {"calories": 90, "protein": 2, "carbs": 21, "fat": 0, "cost": 0.65, "allergens": [], "dietary_type": "vegan"},
        "spinach": {"calories": 7, "protein": 1, "carbs": 1, "fat": 0, "cost": 1.10, "allergens": [], "dietary_type": "vegan"},
        "brown_rice": {"calories": 110, "protein": 3, "carbs": 22, "fat": 1, "cost": 0.45, "allergens": [], "dietary_type": "vegan"},
        "turkey_breast": {"calories": 135, "protein": 25, "carbs": 0, "fat": 3, "cost": 3.20, "allergens": [], "dietary_type": "non_vegetarian"},
        "eggs": {"calories": 70, "protein": 6, "carbs": 1, "fat": 5, "cost": 0.25, "allergens": ["eggs"], "dietary_type": "vegetarian"},
        "avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15, "cost": 1.20, "allergens": [], "dietary_type": "vegan"},
        "almonds": {"calories": 160, "protein": 6, "carbs": 6, "fat": 14, "cost": 2.00, "allergens": ["nuts"], "dietary_type": "vegan"},
        "tofu": {"calories": 80, "protein": 8, "carbs": 2, "fat": 4, "cost": 1.80, "allergens": ["soy"], "dietary_type": "vegan"},
        "lentils": {"calories": 115, "protein": 9, "carbs": 20, "fat": 0, "cost": 0.60, "allergens": [], "dietary_type": "vegan"},
        "cottage_cheese": {"calories": 100, "protein": 12, "carbs": 5, "fat": 2, "cost": 1.30, "allergens": ["dairy"], "dietary_type": "vegetarian"},
        "beans": {"calories": 125, "protein": 8, "carbs": 23, "fat": 1, "cost": 0.50, "allergens": [], "dietary_type": "vegan"},
        "whole_wheat_bread": {"calories": 80, "protein": 4, "carbs": 14, "fat": 1, "cost": 0.30, "allergens": ["gluten"], "dietary_type": "vegan"},
        "peanut_butter": {"calories": 190, "protein": 8, "carbs": 8, "fat": 16, "cost": 0.40, "allergens": ["nuts"], "dietary_type": "vegan"},
        "milk": {"calories": 60, "protein": 3, "carbs": 5, "fat": 3, "cost": 0.50, "allergens": ["dairy"], "dietary_type": "vegetarian"},
        "cheese": {"calories": 113, "protein": 7, "carbs": 1, "fat": 9, "cost": 2.00, "allergens": ["dairy"], "dietary_type": "vegetarian"},
        "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "cost": 5.00, "allergens": [], "dietary_type": "non_vegetarian"},
        "pork": {"calories": 242, "protein": 27, "carbs": 0, "fat": 14, "cost": 4.50, "allergens": [], "dietary_type": "non_vegetarian"},
        "tuna": {"calories": 144, "protein": 30, "carbs": 0, "fat": 1, "cost": 3.50, "allergens": ["fish"], "dietary_type": "non_vegetarian"},
        "chickpeas": {"calories": 164, "protein": 8, "carbs": 27, "fat": 3, "cost": 0.70, "allergens": [], "dietary_type": "vegan"},
        "mushrooms": {"calories": 22, "protein": 3, "carbs": 3, "fat": 0, "cost": 1.50, "allergens": [], "dietary_type": "vegan"}
    }

def filter_foods_by_dietary_preferences(foods, dietary_preference, allergies):
    """Filter foods by dietary preference and allergies"""
    safe_foods = {}
    
    for name, info in foods.items():
        # Check allergies first
        food_allergens = info.get('allergens', [])
        if any(allergen.lower() in [a.lower() for a in allergies] for allergen in food_allergens):
            continue  # Skip if contains allergens
        
        # Check dietary preference
        food_type = info.get('dietary_type', 'vegan')
        
        if dietary_preference == 'vegan':
            # Vegans only eat vegan foods
            if food_type == 'vegan':
                safe_foods[name] = info
        elif dietary_preference == 'vegetarian':
            # Vegetarians eat vegan and vegetarian foods (no meat/fish)
            if food_type in ['vegan', 'vegetarian']:
                safe_foods[name] = info
        elif dietary_preference == 'non_vegetarian':
            # Non-vegetarians can eat everything
            safe_foods[name] = info
        else:
            # Default to including all foods
            safe_foods[name] = info
    
    return safe_foods

def create_meal(foods, target_calories, meal_type):
    """Create a single meal"""
    available_foods = list(foods.keys())
    
    # Define meal patterns
    meal_patterns = {
        'breakfast': ['oatmeal', 'banana', 'greek_yogurt', 'eggs', 'whole_wheat_bread'],
        'lunch': ['chicken_breast', 'turkey_breast', 'salmon', 'tofu', 'quinoa', 'brown_rice', 'broccoli', 'spinach'],
        'dinner': ['chicken_breast', 'turkey_breast', 'salmon', 'tofu', 'sweet_potato', 'broccoli', 'spinach', 'lentils']
    }
    
    # Get foods suitable for this meal type
    preferred_foods = [f for f in meal_patterns.get(meal_type, available_foods) if f in available_foods]
    if not preferred_foods:
        preferred_foods = available_foods
    
    # Select 2-4 foods for the meal
    num_foods = random.randint(2, min(4, len(preferred_foods)))
    selected_foods = random.sample(preferred_foods, num_foods)
    
    meal_foods = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_cost = 0
    
    for food in selected_foods:
        # Base portion (100g)
        portion = 100
        food_info = foods[food]
        
        # Calculate nutrition for this portion
        calories = food_info['calories'] * (portion / 100)
        protein = food_info['protein'] * (portion / 100)
        carbs = food_info['carbs'] * (portion / 100)
        fat = food_info['fat'] * (portion / 100)
        cost = food_info['cost'] * (portion / 100)
        
        meal_foods.append({
            'name': food.replace('_', ' ').title(),
            'portion': portion,
            'unit': 'g'
        })
        
        total_calories += calories
        total_protein += protein
        total_carbs += carbs
        total_fat += fat
        total_cost += cost
    
    return {
        'type': meal_type,
        'foods': meal_foods,
        'nutrition': {
            'calories': total_calories,
            'protein': total_protein,
            'carbs': total_carbs,
            'fat': total_fat
        },
        'cost': total_cost
    }

def generate_meal_plan(name, age, sex, weight_kg, height_cm, activity_level, budget, allergies, meal_count, days, dietary_preference='non_vegetarian'):
    """Generate complete meal plan"""
    
    # Calculate metabolic needs
    bmr, tdee = calculate_bmr_tdee(age, sex, weight_kg, height_cm, activity_level)
    target_calories_per_day = tdee
    calories_per_meal = target_calories_per_day / meal_count
    
    # Get safe foods (filter by dietary preference and allergies)
    all_foods = get_food_database()
    safe_foods = filter_foods_by_dietary_preferences(all_foods, dietary_preference, allergies)
    
    if not safe_foods:
        return {
            'error': f'No safe foods available with your {dietary_preference} diet and allergy restrictions: {allergies}',
            'success': False
        }
    
    # Meal types
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack_1', 'snack_2', 'snack_3'][:meal_count]
    
    # Generate meals for each day
    meal_plan = {}
    all_meals = []
    total_weekly_cost = 0
    
    for day in range(1, days + 1):
        day_key = f"day_{day}"
        day_meals = {}
        daily_calories = 0
        daily_protein = 0
        daily_carbs = 0
        daily_fat = 0
        daily_cost = 0
        
        for meal_type in meal_types:
            meal = create_meal(safe_foods, calories_per_meal, meal_type)
            day_meals[meal_type] = meal
            all_meals.append(meal)
            
            daily_calories += meal['nutrition']['calories']
            daily_protein += meal['nutrition']['protein']
            daily_carbs += meal['nutrition']['carbs']
            daily_fat += meal['nutrition']['fat']
            daily_cost += meal['cost']
        
        # Add daily totals
        day_meals['daily_totals'] = {
            'calories': daily_calories,
            'protein': daily_protein,
            'carbs': daily_carbs,
            'fat': daily_fat,
            'cost': daily_cost
        }
        
        meal_plan[day_key] = day_meals
        total_weekly_cost += daily_cost
    
    # Generate shopping list
    shopping_items = {}
    for meal in all_meals:
        for food in meal['foods']:
            name = food['name'].lower().replace(' ', '_')
            if name in shopping_items:
                shopping_items[name]['quantity'] += food['portion']
            else:
                original_name = name
                if name in all_foods:
                    shopping_items[name] = {
                        'food': food['name'],
                        'quantity': food['portion'],
                        'unit': food['unit'],
                        'estimated_cost': all_foods[name]['cost'] * (food['portion'] / 100)
                    }
    
    shopping_list = {
        'items': list(shopping_items.values()),
        'total_estimated_cost': sum(item['estimated_cost'] for item in shopping_items.values())
    }
    
    return {
        'success': True,
        'user_info': {
            'name': name,
            'bmr': bmr,
            'tdee': tdee,
            'target_calories': target_calories_per_day
        },
        'meal_plan': meal_plan,
        'shopping_list': shopping_list,
        'adaptations': [],
        'optimization_notes': [
            f"Optimized for {target_calories_per_day:.0f} calories/day",
            f"Dietary preference: {dietary_preference.replace('_', ' ').title()}",
            f"Avoided allergens: {', '.join(allergies) if allergies else 'None'}",
            f"Budget target: ${budget}/day (Actual: ${total_weekly_cost/days:.2f}/day)"
        ]
    }

def main():
    """Main demo function"""
    print("🍽️  Welcome to the Personalized Nutrition Optimization Engine!")
    print("Let's create your personalized meal plan!\n")
    
    # Get user input
    print("📋 Basic Information:")
    name = input("Enter your name: ").strip()
    age = int(input("Enter your age: "))
    sex = input("Enter your sex (male/female): ").strip().lower()
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in cm: "))
    
    # Activity level
    print("\n🏃 Activity Level:")
    print("1. Sedentary")
    print("2. Lightly Active") 
    print("3. Moderately Active")
    print("4. Very Active")
    print("5. Extremely Active")
    
    activity_choice = int(input("Choose your activity level (1-5): "))
    activity_levels = ["sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"]
    activity_level = activity_levels[activity_choice - 1] if 1 <= activity_choice <= 5 else "moderately_active"
    
    # Budget
    budget = float(input("\n💰 Enter your daily food budget in USD: "))
    
    # Dietary preference
    print("\n🥗 Dietary Preference:")
    print("1. Vegan (no animal products)")
    print("2. Vegetarian (no meat/fish, dairy/eggs OK)")
    print("3. Non-Vegetarian (everything)")
    
    diet_choice = int(input("Choose your dietary preference (1-3): ") or "3")
    diet_map = {
        1: "vegan",
        2: "vegetarian", 
        3: "non_vegetarian"
    }
    dietary_preference = diet_map.get(diet_choice, "non_vegetarian")
    
    # Allergies
    allergies_input = input("\n🚫 Enter any allergies (comma-separated, or press Enter for none): ").strip()
    allergies = [a.strip().lower() for a in allergies_input.split(',') if a.strip()] if allergies_input else []
    
    # Meal preferences
    meal_count = int(input("\n🍽️ Number of meals per day (2-6): ") or "3")
    days = int(input("Number of days to plan (1-7): ") or "1")
    
    print(f"\n⏳ Generating your personalized meal plan for {days} day(s)...")
    
    # Generate meal plan
    result = generate_meal_plan(name, age, sex, weight, height, activity_level, budget, allergies, meal_count, days, dietary_preference)
    
    if not result.get('success'):
        print(f"\n❌ Error: {result.get('error')}")
        return
    
    # Display results
    print("\n" + "="*60)
    print("🎯 YOUR PERSONALIZED MEAL PLAN")
    print("="*60)
    
    # User info
    user_info = result['user_info']
    print(f"\n👤 Profile: {user_info['name']}")
    print(f"   BMR: {user_info['bmr']:.0f} calories/day")
    print(f"   TDEE: {user_info['tdee']:.0f} calories/day")
    print(f"   Target: {user_info['target_calories']:.0f} calories/day")
    
    # Meal plan
    meal_plan = result['meal_plan']
    for day_key, day_data in meal_plan.items():
        print(f"\n📅 {day_key.replace('_', ' ').title()}:")
        
        for meal_key, meal_data in day_data.items():
            if meal_key == 'daily_totals':
                # Show daily totals
                totals = meal_data
                print(f"\n  📈 Daily Totals:")
                print(f"     🔥 {totals['calories']:.0f} calories")
                print(f"     🥩 {totals['protein']:.1f}g protein ({totals['protein']*4/totals['calories']*100:.1f}%)")
                print(f"     🍞 {totals['carbs']:.1f}g carbs ({totals['carbs']*4/totals['calories']*100:.1f}%)")
                print(f"     🥑 {totals['fat']:.1f}g fat ({totals['fat']*9/totals['calories']*100:.1f}%)")
                print(f"     💰 ${totals['cost']:.2f}")
                continue
                
            # Show individual meals
            meal_name = meal_key.replace('_', ' ').title()
            print(f"\n  🍽️  {meal_name}:")
            
            # Show foods
            foods = meal_data['foods']
            food_names = [f['name'] for f in foods]
            print(f"     • {', '.join(food_names)}")
            
            # Show nutrition
            nutrition = meal_data['nutrition']
            print(f"     📊 {nutrition['calories']:.0f} cal | {nutrition['protein']:.1f}g protein | {nutrition['carbs']:.1f}g carbs | {nutrition['fat']:.1f}g fat")
    
    # Shopping list
    shopping_list = result['shopping_list']
    items = shopping_list['items']
    total_cost = shopping_list['total_estimated_cost']
    
    print(f"\n🛒 Shopping List ({len(items)} items):")
    for item in items:
        print(f"   • {item['food']}: {item['quantity']:.0f}{item['unit']} (${item['estimated_cost']:.2f})")
    
    print(f"\n💰 Total Estimated Cost: ${total_cost:.2f}")
    
    # Budget check
    daily_cost = total_cost / days
    if daily_cost <= budget:
        print(f"✅ Within your ${budget:.2f}/day budget! (${budget - daily_cost:.2f} remaining per day)")
    else:
        print(f"⚠️  Exceeds budget by ${daily_cost - budget:.2f} per day")
    
    # Optimization notes
    optimization = result['optimization_notes']
    if optimization:
        print(f"\n🎯 Optimization Notes:")
        for note in optimization:
            print(f"   • {note}")
    
    print("\n✅ Complete meal plan generated successfully!")
    print("💡 You can run this demo again to try different preferences!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()