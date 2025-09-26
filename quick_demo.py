#!/usr/bin/env python3
"""
Simple Interactive Demo for Personalized Nutrition Optimization Engine
Allows user to input their data and see personalized meal plans generated.
"""

import json
import sys
import os
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our engine components
from engine import PersonalizedNutritionEngine

def main():
    """Main interactive demo function"""
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
    
    activity_map = {
        1: "sedentary",
        2: "lightly_active", 
        3: "moderately_active",
        4: "very_active",
        5: "extremely_active"
    }
    
    activity_choice = int(input("Choose your activity level (1-5): "))
    activity_level = activity_map.get(activity_choice, "moderately_active")
    
    # Budget
    budget = float(input("\n💰 Enter your daily food budget in USD: "))
    
    # Simple allergies
    allergies_input = input("\n🚫 Enter any allergies (comma-separated, or press Enter for none): ").strip()
    allergies = [a.strip().lower() for a in allergies_input.split(',') if a.strip()] if allergies_input else []
    
    # Meal preferences
    meal_count = int(input("\n🍽️ Number of meals per day (2-6): ") or "3")
    days = int(input("Number of days to plan (1-7): ") or "1")
    
    print("\n⏳ Generating your personalized meal plan...")
    
    # Create user data
    user_data = {
        'name': name,
        'age': age,
        'sex': sex,
        'weight_kg': weight,
        'height_cm': height,
        'activity_level': activity_level
    }
    
    preferences = {
        'allergies': allergies,
        'budget_per_day': budget
    }
    
    # Initialize engine and generate meal plan
    engine = PersonalizedNutritionEngine()
    result = engine.generate_meal_plan(
        user_data=user_data,
        preferences=preferences,
        meal_count=meal_count,
        days=days
    )
    
    # Display results
    print("\n" + "="*60)
    print("🎯 YOUR PERSONALIZED MEAL PLAN")
    print("="*60)
    
    # User info
    user_info = result.get('user_info', {})
    if user_info:
        print(f"\n👤 Profile: {user_info.get('name', 'N/A')}")
        print(f"   BMR: {user_info.get('bmr', 0):.0f} calories/day")
        print(f"   TDEE: {user_info.get('tdee', 0):.0f} calories/day")
    
    # Meal plan
    meal_plan = result.get('meal_plan', {})
    if meal_plan:
        for day_key, day_data in meal_plan.items():
            print(f"\n📅 {day_key.replace('_', ' ').title()}:")
            
            for meal_key, meal_data in day_data.items():
                if meal_key == 'daily_totals':
                    continue
                    
                meal_name = meal_key.replace('_', ' ').title()
                foods = meal_data.get('foods', [])
                nutrition = meal_data.get('nutrition', {})
                
                print(f"  🍽️  {meal_name}:")
                for food in foods:
                    print(f"     • {food}")
                
                calories = nutrition.get('calories', 0)
                protein = nutrition.get('protein', 0)
                carbs = nutrition.get('carbs', 0)
                fat = nutrition.get('fat', 0)
                print(f"     📊 {calories:.0f} cal | {protein:.1f}g protein | {carbs:.1f}g carbs | {fat:.1f}g fat")
            
            # Daily totals
            daily_totals = day_data.get('daily_totals', {})
            if daily_totals:
                print(f"\n  📈 Daily Totals:")
                calories = daily_totals.get('calories', 0)
                protein = daily_totals.get('protein', 0)
                carbs = daily_totals.get('carbs', 0)
                fat = daily_totals.get('fat', 0)
                print(f"     {calories:.0f} calories | {protein:.1f}g protein | {carbs:.1f}g carbs | {fat:.1f}g fat")
    
    # Shopping list
    shopping_list = result.get('shopping_list', {})
    if shopping_list:
        items = shopping_list.get('items', [])
        total_cost = shopping_list.get('total_estimated_cost', 0)
        
        print(f"\n🛒 Shopping List:")
        for item in items:
            name = item.get('food', 'N/A')
            quantity = item.get('quantity', 0)
            unit = item.get('unit', 'g')
            cost = item.get('estimated_cost', 0)
            print(f"   • {name}: {quantity:.0f}{unit} (${cost:.2f})")
        
        print(f"\n💰 Total Estimated Cost: ${total_cost:.2f}")
        
        # Budget check
        if total_cost <= budget:
            print(f"✅ Within your ${budget:.2f} budget!")
        else:
            print(f"⚠️  Exceeds budget by ${total_cost - budget:.2f}")
    
    print("\n✅ Meal plan generated successfully!")
    print("💡 You can run this demo again to try different preferences!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your input and try again.")