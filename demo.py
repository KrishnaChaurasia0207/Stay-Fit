"""
Demo script for the Personalized Nutrition Optimization Engine
Run this to see the engine in action with sample data
"""

import sys
import json
from datetime import datetime, date, timedelta

# Fix imports for standalone execution
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import main engine
from engine import PersonalizedNutritionEngine


def main():
    """Demonstrate the Personalized Nutrition Engine"""
    
    print("🥗 Personalized Nutrition Optimization Engine Demo")
    print("=" * 60)
    
    try:
        # Initialize the engine
        engine = PersonalizedNutritionEngine()
        print("✅ Engine initialized successfully")
        
        # Sample user data
        user_data = {
            "name": "Demo User",
            "age": 30,
            "sex": "male",
            "weight_kg": 75.0,
            "height_cm": 180.0,
            "activity_level": "moderately_active",
            "daily_budget": 25.0,
            "dietary_preferences": {
                "allergies": ["nuts"],
                "dislikes": ["fish"],
                "cuisine_preferences": ["mediterranean"]
            }
        }
        
        # Sample biometric data
        biometric_data = [
            {
                "timestamp": datetime.now().isoformat(),
                "steps": 8500,
                "heart_rate": 72,
                "sleep_hours": 7.5,
                "glucose_mg_dl": 95
            }
        ]
        
        print(f"\n👤 User Profile: {user_data['name']}")
        print(f"   Age: {user_data['age']}, Weight: {user_data['weight_kg']}kg, Height: {user_data['height_cm']}cm")
        print(f"   Activity Level: {user_data['activity_level']}")
        print(f"   Budget: ${user_data['daily_budget']}/day")
        print(f"   Recent Biometrics: {biometric_data[0]['steps']} steps, {biometric_data[0]['glucose_mg_dl']} mg/dL glucose")
        
        # Generate meal plan
        print("\n🔄 Generating personalized meal plan...")
        result = engine.generate_meal_plan(
            user_data=user_data,
            biometric_data=biometric_data,
            meal_count=3
        )
        
        if result['success']:
            print("✅ Meal plan generated successfully!")
            
            # Display results
            print(f"\n📊 Nutrition Summary:")
            print(f"   Total Calories: {result['total_calories']:.0f}")
            print(f"   Protein: {result['total_macros']['protein']:.1f}g")
            print(f"   Carbs: {result['total_macros']['carbs']:.1f}g")
            print(f"   Fat: {result['total_macros']['fat']:.1f}g")
            
            print(f"\n🍽️ Meal Plan:")
            for i, meal in enumerate(result['meals'], 1):
                items_str = ", ".join(meal['items'])
                print(f"   {i}. {meal['meal_type'].title()}: {items_str}")
                print(f"      Calories: {meal['calories']:.0f}, Protein: {meal['protein']:.1f}g")
            
            print(f"\n🛒 Shopping List ({len(result['shopping_list'])} items):")
            for item in result['shopping_list'][:5]:  # Show first 5 items
                print(f"   • {item['item']}: {item['quantity']} {item['unit']}")
            if len(result['shopping_list']) > 5:
                print(f"   ... and {len(result['shopping_list']) - 5} more items")
            
            if result['adaptations']:
                print(f"\n🔧 Adaptations Applied:")
                print(f"   {result['adaptations']}")
            
            if result['personalization_notes']:
                print(f"\n📝 Personalization Notes:")
                print(f"   {result['personalization_notes']}")
            
            print(f"\n💰 Estimated Cost: ${result.get('total_cost', 0):.2f}")
            
            # Save sample output
            with open('demo_output.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full output saved to 'demo_output.json'")
            
        else:
            print(f"❌ Error generating meal plan: {result['error']}")
            return False
        
        # Test high glucose adaptation
        print(f"\n🧪 Testing High Glucose Adaptation...")
        high_glucose_bio = [
            {
                "timestamp": datetime.now().isoformat(),
                "steps": 6000,
                "heart_rate": 78,
                "sleep_hours": 6.0,
                "glucose_mg_dl": 160  # High glucose
            }
        ]
        
        adapted_result = engine.generate_meal_plan(
            user_data=user_data,
            biometric_data=high_glucose_bio,
            meal_count=3
        )
        
        if adapted_result['success']:
            carb_reduction = result['total_macros']['carbs'] - adapted_result['total_macros']['carbs']
            print(f"   Normal carbs: {result['total_macros']['carbs']:.1f}g")
            print(f"   Adapted carbs: {adapted_result['total_macros']['carbs']:.1f}g")
            print(f"   Reduction: {carb_reduction:.1f}g ({carb_reduction/result['total_macros']['carbs']*100:.1f}%)")
            print(f"   Adaptation: {adapted_result['adaptations']}")
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"   Engine Version: {engine.version}")
        print(f"   Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all required dependencies are installed: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n✨ The Personalized Nutrition Optimization Engine is ready for integration!")
        print(f"   • Check README.md for detailed documentation")
        print(f"   • Run test_engine.py for comprehensive testing")
        print(f"   • Use examples.py for more usage examples")
    
    sys.exit(0 if success else 1)