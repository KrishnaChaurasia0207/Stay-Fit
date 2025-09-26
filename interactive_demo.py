#!/usr/bin/env python3
"""
Interactive Demo for Personalized Nutrition Optimization Engine
Allows user to input their data and see personalized meal plans generated.
"""

import json
import sys
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from enum import Enum

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our engine components
from models import UserProfile, BiometricData, DietaryPreferences, ActivityLevel
from engine import PersonalizedNutritionEngine

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str = Colors.ENDC):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.ENDC}")

def get_user_input():
    """Collect user input for profile creation"""
    print_colored("\n🍽️  Welcome to the Personalized Nutrition Optimization Engine!", Colors.HEADER + Colors.BOLD)
    print_colored("Let's create your personalized meal plan!\n", Colors.CYAN)
    
    # Basic profile information
    print_colored("📋 Basic Information:", Colors.BLUE + Colors.BOLD)
    name = input("Enter your name: ").strip()
    
    while True:
        try:
            age = int(input("Enter your age: "))
            if 10 <= age <= 120:
                break
            else:
                print_colored("Please enter a valid age between 10 and 120.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number for age.", Colors.WARNING)
    
    while True:
        sex_input = input("Enter your sex (M/F): ").strip().upper()
        if sex_input in ['M', 'F']:
            sex = "male" if sex_input == 'M' else "female"
            break
        else:
            print_colored("Please enter 'M' for Male or 'F' for Female.", Colors.WARNING)
    
    while True:
        try:
            weight = float(input("Enter your weight in kg: "))
            if 30 <= weight <= 300:
                break
            else:
                print_colored("Please enter a valid weight between 30 and 300 kg.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number for weight.", Colors.WARNING)
    
    while True:
        try:
            height = float(input("Enter your height in cm: "))
            if 100 <= height <= 250:
                break
            else:
                print_colored("Please enter a valid height between 100 and 250 cm.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number for height.", Colors.WARNING)
    
    # Activity level
    print_colored("\n🏃 Activity Level:", Colors.BLUE + Colors.BOLD)
    print("1. Sedentary (little or no exercise)")
    print("2. Lightly Active (light exercise/sports 1-3 days/week)")
    print("3. Moderately Active (moderate exercise/sports 3-5 days/week)")
    print("4. Very Active (hard exercise/sports 6-7 days a week)")
    print("5. Extremely Active (very hard exercise, physical job)")
    
    while True:
        try:
            activity_choice = int(input("Choose your activity level (1-5): "))
            if 1 <= activity_choice <= 5:
                activity_levels = [
                    ActivityLevel.SEDENTARY,
                    ActivityLevel.LIGHTLY_ACTIVE,
                    ActivityLevel.MODERATELY_ACTIVE,
                    ActivityLevel.VERY_ACTIVE,
                    ActivityLevel.EXTREMELY_ACTIVE
                ]
                activity_level = activity_levels[activity_choice - 1]
                break
            else:
                print_colored("Please enter a number between 1 and 5.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number.", Colors.WARNING)
    
    # Dietary preferences
    print_colored("\n🥗 Dietary Preferences:", Colors.BLUE + Colors.BOLD)
    dietary_restrictions = []
    allergies = []
    
    restrictions_list = ["vegetarian", "vegan", "keto", "paleo", "mediterranean", "low_carb", "low_fat"]
    print("Select dietary restrictions (enter numbers separated by commas, or press Enter for none):")
    for i, restriction in enumerate(restrictions_list, 1):
        print(f"{i}. {restriction.replace('_', ' ').title()}")
    
    restrictions_input = input("Your choices: ").strip()
    if restrictions_input:
        try:
            choices = [int(x.strip()) for x in restrictions_input.split(',')]
            dietary_restrictions = [restrictions_list[i-1] for i in choices if 1 <= i <= len(restrictions_list)]
        except ValueError:
            print_colored("Invalid input, skipping dietary restrictions.", Colors.WARNING)
    
    allergies_list = ["dairy", "nuts", "gluten", "shellfish", "eggs", "soy"]
    print("\nSelect allergies (enter numbers separated by commas, or press Enter for none):")
    for i, allergy in enumerate(allergies_list, 1):
        print(f"{i}. {allergy.title()}")
    
    allergies_input = input("Your choices: ").strip()
    if allergies_input:
        try:
            choices = [int(x.strip()) for x in allergies_input.split(',')]
            allergies = [allergies_list[i-1] for i in choices if 1 <= i <= len(allergies_list)]
        except ValueError:
            print_colored("Invalid input, skipping allergies.", Colors.WARNING)
    
    # Budget
    print_colored("\n💰 Budget:", Colors.BLUE + Colors.BOLD)
    while True:
        try:
            budget = float(input("Enter your daily food budget in USD (or 0 for no limit): "))
            if budget >= 0:
                budget = budget if budget > 0 else None
                break
            else:
                print_colored("Please enter a positive number or 0.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number.", Colors.WARNING)
    
    # Biometric data (optional)
    print_colored("\n📊 Biometric Data (Optional):", Colors.BLUE + Colors.BOLD)
    print("Do you want to provide biometric data for more personalized recommendations?")
    use_biometrics = input("Enter 'y' for yes, or press Enter to skip: ").strip().lower() == 'y'
    
    biometric_data = None
    if use_biometrics:
        try:
            steps = int(input("Daily steps (or 0 to skip): ") or "0")
            heart_rate = int(input("Resting heart rate in bpm (or 0 to skip): ") or "0")
            sleep_hours = float(input("Hours of sleep last night (or 0 to skip): ") or "0")
            glucose_level = float(input("Blood glucose level in mg/dL (or 0 to skip): ") or "0")
            
            biometric_data = BiometricData(
                timestamp=datetime.now(),
                steps=steps if steps > 0 else None,
                heart_rate=heart_rate if heart_rate > 0 else None,
                sleep_hours=sleep_hours if sleep_hours > 0 else None,
                glucose_mg_dl=glucose_level if glucose_level > 0 else None
            )
        except ValueError:
            print_colored("Invalid biometric data, skipping.", Colors.WARNING)
            biometric_data = None
    
    # Meal preferences
    print_colored("\n🍽️ Meal Preferences:", Colors.BLUE + Colors.BOLD)
    while True:
        try:
            meal_count = int(input("Number of meals per day (2-6): ") or "3")
            if 2 <= meal_count <= 6:
                break
            else:
                print_colored("Please enter a number between 2 and 6.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number.", Colors.WARNING)
    
    while True:
        try:
            days = int(input("Number of days to plan (1-7): ") or "1")
            if 1 <= days <= 7:
                break
            else:
                print_colored("Please enter a number between 1 and 7.", Colors.WARNING)
        except ValueError:
            print_colored("Please enter a valid number.", Colors.WARNING)
    
    return {
        'user_data': {
            'name': name,
            'age': age,
            'sex': sex,
            'weight_kg': weight,
            'height_cm': height,
            'activity_level': activity_level.value
        },
        'preferences': {
            'dietary_restrictions': dietary_restrictions,
            'allergies': allergies,
            'budget_per_day': budget
        },
        'biometric_data': biometric_data,
        'meal_count': meal_count,
        'days': days
    }

def display_results(result: Dict[str, Any]):
    """Display the meal plan results in a formatted way"""
    print_colored("\n" + "="*60, Colors.HEADER)
    print_colored("🎯 YOUR PERSONALIZED MEAL PLAN", Colors.HEADER + Colors.BOLD)
    print_colored("="*60, Colors.HEADER)
    
    # User info
    user_info = result.get('user_info', {})
    if user_info:
        print_colored(f"\n👤 Profile: {user_info.get('name', 'N/A')}", Colors.CYAN + Colors.BOLD)
        print_colored(f"   BMR: {user_info.get('bmr', 0):.0f} calories/day", Colors.CYAN)
        print_colored(f"   TDEE: {user_info.get('tdee', 0):.0f} calories/day", Colors.CYAN)
    
    # Meal plan
    meal_plan = result.get('meal_plan', {})
    if meal_plan:
        for day_key, day_data in meal_plan.items():
            print_colored(f"\n📅 {day_key.replace('_', ' ').title()}:", Colors.GREEN + Colors.BOLD)
            
            for meal_key, meal_data in day_data.items():
                if meal_key == 'daily_totals':
                    continue
                    
                meal_name = meal_key.replace('_', ' ').title()
                foods = meal_data.get('foods', [])
                nutrition = meal_data.get('nutrition', {})
                
                print_colored(f"  🍽️  {meal_name}:", Colors.BLUE)
                for food in foods:
                    print(f"     • {food}")
                
                calories = nutrition.get('calories', 0)
                protein = nutrition.get('protein', 0)
                carbs = nutrition.get('carbs', 0)
                fat = nutrition.get('fat', 0)
                print_colored(f"     📊 {calories:.0f} cal | {protein:.1f}g protein | {carbs:.1f}g carbs | {fat:.1f}g fat", Colors.CYAN)
            
            # Daily totals
            daily_totals = day_data.get('daily_totals', {})
            if daily_totals:
                print_colored(f"\n  📈 Daily Totals:", Colors.GREEN)
                calories = daily_totals.get('calories', 0)
                protein = daily_totals.get('protein', 0)
                carbs = daily_totals.get('carbs', 0)
                fat = daily_totals.get('fat', 0)
                print_colored(f"     {calories:.0f} calories | {protein:.1f}g protein | {carbs:.1f}g carbs | {fat:.1f}g fat", Colors.GREEN)
    
    # Adaptations
    adaptations = result.get('adaptations', [])
    if adaptations:
        print_colored(f"\n🔧 Biometric Adaptations Applied:", Colors.WARNING + Colors.BOLD)
        for adaptation in adaptations:
            print_colored(f"   • {adaptation}", Colors.WARNING)
    
    # Shopping list
    shopping_list = result.get('shopping_list', {})
    if shopping_list:
        items = shopping_list.get('items', [])
        total_cost = shopping_list.get('total_estimated_cost', 0)
        
        print_colored(f"\n🛒 Shopping List:", Colors.BLUE + Colors.BOLD)
        for item in items:
            name = item.get('food', 'N/A')
            quantity = item.get('quantity', 0)
            unit = item.get('unit', 'g')
            cost = item.get('estimated_cost', 0)
            print(f"   • {name}: {quantity:.0f}{unit} (${cost:.2f})")
        
        print_colored(f"\n💰 Total Estimated Cost: ${total_cost:.2f}", Colors.GREEN + Colors.BOLD)
    
    # Optimization notes
    optimization = result.get('optimization_notes', [])
    if optimization:
        print_colored(f"\n🎯 Optimization Notes:", Colors.CYAN + Colors.BOLD)
        for note in optimization:
            print_colored(f"   • {note}", Colors.CYAN)

def main():
    """Main interactive demo function"""
    try:
        # Get user input
        user_input = get_user_input()
        
        print_colored("\n⏳ Generating your personalized meal plan...", Colors.CYAN + Colors.BOLD)
        
        # Initialize the engine
        engine = PersonalizedNutritionEngine()
        
        # Generate meal plan
        result = engine.generate_meal_plan(
            user_data=user_input['user_data'],
            preferences=user_input['preferences'],
            biometric_data=user_input['biometric_data'],
            meal_count=user_input['meal_count'],
            days=user_input['days']
        )
        
        # Display results
        display_results(result)
        
        print_colored("\n✅ Meal plan generated successfully!", Colors.GREEN + Colors.BOLD)
        print_colored("💡 Tip: You can run this demo again to try different preferences!", Colors.CYAN)
        
    except KeyboardInterrupt:
        print_colored("\n\n👋 Demo interrupted by user. Goodbye!", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ Error: {str(e)}", Colors.FAIL)
        print_colored("Please check your input and try again.", Colors.WARNING)

if __name__ == "__main__":
    main()