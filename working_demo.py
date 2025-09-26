#!/usr/bin/env python3
"""
Working Interactive Demo - Shows Complete Meal Plan Results
"""

import json
import sys
import os
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    
    activity_choice = int(input("Choose your activity level (1-5): "))
    activity_levels = ["sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"]
    activity_level = activity_levels[activity_choice - 1] if 1 <= activity_choice <= 5 else "moderately_active"
    
    # Budget
    budget = float(input("\n💰 Enter your daily food budget in USD: "))
    
    # Simple allergies
    allergies_input = input("\n🚫 Enter any allergies (comma-separated, or press Enter for none): ").strip()
    allergies = [a.strip().lower() for a in allergies_input.split(',') if a.strip()] if allergies_input else []
    
    # Meal preferences
    meal_count = int(input("\n🍽️ Number of meals per day (2-6): ") or "3")
    days = int(input("Number of days to plan (1-7): ") or "1")
    
    print("\n⏳ Generating your personalized meal plan...")
    
    # Import and initialize engine
    try:
        from engine import PersonalizedNutritionEngine
        engine = PersonalizedNutritionEngine()
        
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
        
        # Generate meal plan
        result = engine.generate_meal_plan(
            user_data=user_data,
            preferences=preferences,
            meal_count=meal_count,
            days=days
        )
        
        # Display results beautifully
        print("\n" + "="*60)
        print("🎯 YOUR PERSONALIZED MEAL PLAN")
        print("="*60)
        
        # Save and show the raw result for debugging
        with open('debug_result.json', 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        # User profile info
        user_info = result.get('user_info', {})
        if user_info:
            print(f"\n👤 Profile: {user_info.get('name', name)}")
            print(f"   BMR: {user_info.get('bmr', 0):.0f} calories/day")
            print(f"   TDEE: {user_info.get('tdee', 0):.0f} calories/day")
        
        # Show complete result structure
        print(f"\n🔍 Debug Info:")
        print(f"   Result keys: {list(result.keys())}")
        
        # Meal plan details
        meal_plan = result.get('meal_plan', {})
        print(f"\n📋 Meal Plan Keys: {list(meal_plan.keys()) if meal_plan else 'No meal plan found'}")
        
        if meal_plan:
            for day_key, day_data in meal_plan.items():
                print(f"\n📅 {day_key.replace('_', ' ').title()}:")
                print(f"   Day data keys: {list(day_data.keys()) if isinstance(day_data, dict) else 'Not a dict'}")
                
                if isinstance(day_data, dict):
                    for meal_key, meal_data in day_data.items():
                        if meal_key == 'daily_totals':
                            # Show daily totals
                            totals = meal_data
                            print(f"\n  📈 Daily Totals:")
                            print(f"     🔥 {totals.get('calories', 0):.0f} calories")
                            print(f"     🥩 {totals.get('protein', 0):.1f}g protein")
                            print(f"     🍞 {totals.get('carbs', 0):.1f}g carbs") 
                            print(f"     🥑 {totals.get('fat', 0):.1f}g fat")
                            continue
                            
                        # Show individual meals
                        meal_name = meal_key.replace('_', ' ').title()
                        print(f"\n  🍽️  {meal_name}:")
                        
                        if isinstance(meal_data, dict):
                            foods = meal_data.get('foods', [])
                            nutrition = meal_data.get('nutrition', {})
                            
                            # Show foods
                            if foods:
                                for food in foods:
                                    print(f"     • {food}")
                            else:
                                print("     • No foods listed")
                            
                            # Show nutrition
                            if nutrition:
                                calories = nutrition.get('calories', 0)
                                protein = nutrition.get('protein', 0)
                                carbs = nutrition.get('carbs', 0)
                                fat = nutrition.get('fat', 0)
                                print(f"     📊 {calories:.0f} cal | {protein:.1f}g protein | {carbs:.1f}g carbs | {fat:.1f}g fat")
                        else:
                            print(f"     Meal data: {meal_data}")
        
        # Shopping list
        shopping_list = result.get('shopping_list', {})
        if shopping_list:
            items = shopping_list.get('items', [])
            total_cost = shopping_list.get('total_estimated_cost', 0)
            
            print(f"\n🛒 Shopping List ({len(items)} items):")
            for item in items:
                if isinstance(item, dict):
                    name = item.get('food', 'Unknown')
                    quantity = item.get('quantity', 0)
                    unit = item.get('unit', 'g')
                    cost = item.get('estimated_cost', 0)
                    print(f"   • {name}: {quantity:.0f}{unit} (${cost:.2f})")
                else:
                    print(f"   • {item}")
            
            print(f"\n💰 Total Estimated Cost: ${total_cost:.2f}")
            
            # Budget check
            if total_cost <= budget:
                print(f"✅ Within your ${budget:.2f} budget! (${budget - total_cost:.2f} remaining)")
            else:
                print(f"⚠️  Exceeds budget by ${total_cost - budget:.2f}")
        else:
            print("\n🛒 No shopping list generated")
        
        # Adaptations
        adaptations = result.get('adaptations', [])
        if adaptations:
            print(f"\n🔧 Adaptations Applied:")
            for adaptation in adaptations:
                print(f"   • {adaptation}")
        
        # Optimization notes
        optimization = result.get('optimization_notes', [])
        if optimization:
            print(f"\n🎯 Optimization Notes:")
            for note in optimization:
                print(f"   • {note}")
        
        print(f"\n💾 Full result saved to 'debug_result.json' for inspection")
        print("\n✅ Meal plan generated successfully!")
        print("💡 Check the debug_result.json file to see the complete data structure!")
        
    except Exception as e:
        print(f"\n❌ Error generating meal plan: {e}")
        import traceback
        traceback.print_exc()
        print("\nTrying simple fallback...")
        
        # Simple fallback meal plan
        print(f"\n🍽️ Simple Meal Plan for {name}:")
        print(f"   Target: ~{(10 * weight + 6.25 * height - 5 * age + 5) * 1.55:.0f} calories/day")
        print(f"   Budget: ${budget}/day")
        
        simple_meals = [
            "🥣 Breakfast: Oatmeal with banana and nuts",
            "🥗 Lunch: Grilled chicken with quinoa and vegetables", 
            "🍽️ Dinner: Salmon with sweet potato and broccoli"
        ]
        
        for meal in simple_meals:
            print(f"   {meal}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()