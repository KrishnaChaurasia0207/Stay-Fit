"""
Usage examples for the Personalized Nutrition Optimization Engine
Demonstrates various features and use cases
"""

from datetime import datetime, date, timedelta
import json
from engine import PersonalizedNutritionEngine


def example_basic_meal_plan():
    """Example 1: Basic meal plan generation"""
    print("🥗 Example 1: Basic Meal Plan Generation")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    user_data = {
        "name": "Alice Johnson",
        "age": 29,
        "sex": "female",
        "weight_kg": 65.0,
        "height_cm": 168.0,
        "activity_level": "moderately_active",
        "daily_budget": 30.0
    }
    
    result = engine.generate_meal_plan(user_data=user_data, meal_count=3)
    
    if result['success']:
        print(f"✅ Generated meal plan for {user_data['name']}")
        print(f"Total calories: {result['total_calories']:.0f}")
        print(f"Macros - Protein: {result['total_macros']['protein']:.1f}g, "
              f"Carbs: {result['total_macros']['carbs']:.1f}g, "
              f"Fat: {result['total_macros']['fat']:.1f}g")
        
        print("\nMeals:")
        for meal in result['meals']:
            items_str = ", ".join(meal['items'])
            print(f"  {meal['meal_type'].title()}: {items_str} ({meal['calories']:.0f} cal)")
        
        print(f"\nShopping list: {len(result['shopping_list'])} items")
        print(f"Estimated cost: ${result.get('total_cost', 0):.2f}")
    else:
        print(f"❌ Error: {result['error']}")
    
    return result


def example_vegetarian_with_allergies():
    """Example 2: Vegetarian user with allergies"""
    print("\n🌱 Example 2: Vegetarian with Allergies")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    user_data = {
        "name": "David Chen",
        "age": 34,
        "sex": "male",
        "weight_kg": 72.0,
        "height_cm": 175.0,
        "activity_level": "very_active",
        "daily_budget": 25.0,
        "dietary_preferences": {
            "allergies": ["nuts", "dairy"],
            "dislikes": ["mushrooms", "eggplant"],
            "cuisine_preferences": ["asian", "mediterranean"],
            "max_preparation_time": 25
        }
    }
    
    result = engine.generate_meal_plan(user_data=user_data, meal_count=3)
    
    if result['success']:
        print(f"✅ Generated vegetarian meal plan for {user_data['name']}")
        print(f"Personalization: {result['personalization_notes']}")
        
        print("\nMeals:")
        all_items = []
        for meal in result['meals']:
            items_str = ", ".join(meal['items'])
            all_items.extend(meal['items'])
            print(f"  {meal['meal_type'].title()}: {items_str}")
        
        # Check for restricted items
        restricted_found = []
        for item in all_items:
            item_lower = item.lower()
            if any(allergen.lower() in item_lower for allergen in user_data['dietary_preferences']['allergies']):
                restricted_found.append(item)
        
        if not restricted_found:
            print("✅ No allergens detected in meal plan")
        else:
            print(f"⚠️  Potential allergens found: {restricted_found}")
    else:
        print(f"❌ Error: {result['error']}")


def example_high_glucose_adaptation():
    """Example 3: Real-time adaptation for high glucose"""
    print("\n📊 Example 3: High Glucose Adaptation")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    user_data = {
        "name": "Maria Rodriguez",
        "age": 45,
        "sex": "female",
        "weight_kg": 68.0,
        "height_cm": 162.0,
        "activity_level": "lightly_active"
    }
    
    # Normal biometric data
    normal_biometrics = [
        {
            "timestamp": datetime.now().isoformat(),
            "steps": 7500,
            "heart_rate": 72,
            "sleep_hours": 7.5,
            "glucose_mg_dl": 92
        }
    ]
    
    # High glucose biometric data
    high_glucose_biometrics = [
        {
            "timestamp": datetime.now().isoformat(),
            "steps": 6000,
            "heart_rate": 78,
            "sleep_hours": 6.0,
            "glucose_mg_dl": 165  # High glucose
        }
    ]
    
    # Generate both meal plans
    normal_plan = engine.generate_meal_plan(
        user_data=user_data,
        biometric_data=normal_biometrics
    )
    
    adapted_plan = engine.generate_meal_plan(
        user_data=user_data,
        biometric_data=high_glucose_biometrics
    )
    
    print("Normal conditions:")
    print(f"  Total carbs: {normal_plan['total_macros']['carbs']:.1f}g")
    
    print("High glucose adaptation:")
    print(f"  Total carbs: {adapted_plan['total_macros']['carbs']:.1f}g")
    print(f"  Adaptations: {adapted_plan['adaptations']}")
    
    carb_reduction = normal_plan['total_macros']['carbs'] - adapted_plan['total_macros']['carbs']
    print(f"  Carb reduction: {carb_reduction:.1f}g ({carb_reduction/normal_plan['total_macros']['carbs']*100:.1f}%)")


def example_nutrition_insights():
    """Example 4: Detailed nutrition insights"""
    print("\n🔍 Example 4: Nutrition Insights")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    user_data = {
        "name": "Mike Thompson",
        "age": 38,
        "sex": "male",
        "weight_kg": 85.0,
        "height_cm": 185.0,
        "activity_level": "very_active"
    }
    
    biometric_data = [
        {
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "steps": 12500,
            "heart_rate": 65,
            "sleep_hours": 8.0,
            "glucose_mg_dl": 88,
            "weight_kg": 85.0,
            "body_fat_percentage": 12.0
        }
    ]
    
    insights = engine.get_nutrition_insights(
        user_data=user_data,
        biometric_data=biometric_data
    )
    
    if insights['success']:
        profile = insights['user_profile']
        requirements = insights['calorie_requirements']
        
        print(f"User: {user_data['name']} ({user_data['age']} years old)")
        print(f"BMI: {profile['bmi']:.1f}")
        print(f"BMR: {profile['bmr']:.0f} calories/day")
        print(f"TDEE: {profile['tdee']:.0f} calories/day")
        
        print(f"\nCalorie Requirements:")
        print(f"  Maintenance: {requirements['maintenance']:.0f} cal/day")
        print(f"  Weight loss: {requirements['weight_loss']:.0f} cal/day")
        print(f"  Weight gain: {requirements['weight_gain']:.0f} cal/day")
        
        print(f"\nRecommendations:")
        for rec in insights['recommendations']:
            print(f"  • {rec}")
    else:
        print(f"❌ Error: {insights['error']}")


def example_meal_history_learning():
    """Example 5: Learning from meal history"""
    print("\n📚 Example 5: Learning from Meal History")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    # User with meal history
    user_data = {
        "name": "Sarah Kim",
        "age": 31,
        "sex": "female",
        "weight_kg": 58.0,
        "height_cm": 160.0,
        "activity_level": "moderately_active",
        "meal_history": [
            {
                "date": (date.today() - timedelta(days=1)).isoformat(),
                "meal_type": "breakfast",
                "foods": ["Greek Yogurt", "Blueberries", "Almonds"],
                "calories": 280,
                "protein_g": 18,
                "carbs_g": 22,
                "fat_g": 12,
                "satisfaction_rating": 5
            },
            {
                "date": (date.today() - timedelta(days=1)).isoformat(),
                "meal_type": "lunch",
                "foods": ["Quinoa", "Chicken Breast", "Spinach"],
                "calories": 420,
                "protein_g": 35,
                "carbs_g": 38,
                "fat_g": 8,
                "satisfaction_rating": 4
            },
            {
                "date": (date.today() - timedelta(days=2)).isoformat(),
                "meal_type": "dinner",
                "foods": ["Salmon", "Sweet Potato", "Broccoli"],
                "calories": 480,
                "protein_g": 32,
                "carbs_g": 42,
                "fat_g": 18,
                "satisfaction_rating": 5
            }
        ]
    }
    
    result = engine.generate_meal_plan(user_data=user_data, meal_count=3)
    
    if result['success']:
        print(f"✅ Generated personalized meal plan for {user_data['name']}")
        print(f"Personalization notes: {result['personalization_notes']}")
        
        # Analyze patterns from history
        history = user_data['meal_history']
        avg_satisfaction = sum(m['satisfaction_rating'] for m in history) / len(history)
        avg_protein = sum(m['protein_g'] for m in history) / len(history)
        
        print(f"\nLearning from history:")
        print(f"  Average satisfaction: {avg_satisfaction:.1f}/5")
        print(f"  Average protein: {avg_protein:.1f}g per meal")
        
        print(f"\nNew meal plan protein average: {sum(m['protein'] for m in result['meals'])/len(result['meals']):.1f}g per meal")
    else:
        print(f"❌ Error: {result['error']}")


def example_biometric_simulation():
    """Example 6: Biometric change simulation"""
    print("\n🔬 Example 6: Biometric Simulation")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    current_biometrics = {
        "steps": 8000,
        "heart_rate": 70,
        "sleep_hours": 7.5,
        "glucose_mg_dl": 90
    }
    
    scenarios = ["high_glucose", "low_activity", "poor_sleep", "high_stress"]
    
    for scenario in scenarios:
        simulation = engine.simulate_biometric_changes(current_biometrics, scenario)
        
        print(f"{scenario.replace('_', ' ').title()}:")
        print(f"  Simulated values: {simulation['simulated_biometrics']}")
        print(f"  Expected adaptations:")
        for adaptation in simulation['expected_adaptations']:
            print(f"    • {adaptation}")
        print()


def save_example_outputs():
    """Save example outputs to files"""
    print("💾 Saving Example Outputs")
    print("-" * 50)
    
    engine = PersonalizedNutritionEngine()
    
    # Generate various examples
    examples = {
        "basic_meal_plan": example_basic_meal_plan(),
        "nutrition_insights": engine.get_nutrition_insights({
            "name": "Example User",
            "age": 30,
            "sex": "other",
            "weight_kg": 70,
            "height_cm": 170
        })
    }
    
    # Save to JSON file
    with open('example_outputs.json', 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    
    print("✅ Example outputs saved to 'example_outputs.json'")


def main():
    """Run all examples"""
    print("🚀 Personalized Nutrition Engine - Usage Examples")
    print("=" * 60)
    
    try:
        example_basic_meal_plan()
        example_vegetarian_with_allergies()
        example_high_glucose_adaptation()
        example_nutrition_insights()
        example_meal_history_learning()
        example_biometric_simulation()
        save_example_outputs()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()