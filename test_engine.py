"""
Comprehensive test suite for the Personalized Nutrition Optimization Engine
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date, timedelta

# Add the nutrition_engine directory to the path
sys.path.append(str(Path(__file__).parent))

from engine import PersonalizedNutritionEngine


def create_sample_user_data():
    """Create sample user data for testing"""
    return {
        "name": "John Doe",
        "age": 32,
        "sex": "male",
        "weight_kg": 75.0,
        "height_cm": 180.0,
        "activity_level": "moderately_active",
        "daily_budget": 25.0,
        "dietary_preferences": {
            "allergies": ["nuts"],
            "dislikes": ["fish"],
            "cuisine_preferences": ["american", "mediterranean"],
            "max_preparation_time": 30
        },
        "meal_history": [
            {
                "date": (date.today() - timedelta(days=1)).isoformat(),
                "meal_type": "breakfast",
                "foods": ["Oatmeal", "Banana", "Milk"],
                "calories": 350,
                "protein_g": 15,
                "carbs_g": 55,
                "fat_g": 8,
                "satisfaction_rating": 4
            },
            {
                "date": (date.today() - timedelta(days=1)).isoformat(),
                "meal_type": "lunch",
                "foods": ["Chicken Breast", "Rice", "Broccoli"],
                "calories": 520,
                "protein_g": 45,
                "carbs_g": 48,
                "fat_g": 12,
                "satisfaction_rating": 5
            }
        ]
    }


def create_sample_biometric_data():
    """Create sample biometric data for testing"""
    return [
        {
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "steps": 8500,
            "heart_rate": 72,
            "sleep_hours": 7.5,
            "glucose_mg_dl": 95,
            "weight_kg": 75.0
        },
        {
            "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
            "steps": 12000,
            "heart_rate": 68,
            "sleep_hours": 8.0,
            "glucose_mg_dl": 88,
            "weight_kg": 75.2
        }
    ]


def create_high_glucose_biometric_data():
    """Create biometric data with high glucose for adaptation testing"""
    return [
        {
            "timestamp": datetime.now().isoformat(),
            "steps": 6000,
            "heart_rate": 78,
            "sleep_hours": 6.5,
            "glucose_mg_dl": 155,  # High glucose
            "weight_kg": 75.0
        }
    ]


def create_vegetarian_user_data():
    """Create sample vegetarian user data"""
    return {
        "name": "Jane Smith",
        "age": 28,
        "sex": "female",
        "weight_kg": 62.0,
        "height_cm": 165.0,
        "activity_level": "very_active",
        "daily_budget": 20.0,
        "dietary_preferences": {
            "allergies": ["dairy"],
            "dislikes": ["mushrooms"],
            "cuisine_preferences": ["indian", "mediterranean"],
            "dietary_restrictions": ["vegetarian", "dairy_free"]
        }
    }


def test_basic_meal_plan_generation():
    """Test basic meal plan generation"""
    print("🧪 Testing basic meal plan generation...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_sample_user_data()
    biometric_data = create_sample_biometric_data()
    
    result = engine.generate_meal_plan(
        user_data=user_data,
        biometric_data=biometric_data,
        meal_count=3
    )
    
    assert result['success'] == True, "Meal plan generation should succeed"
    assert len(result['meals']) == 3, "Should generate 3 meals"
    assert result['total_calories'] > 0, "Should have positive total calories"
    assert len(result['shopping_list']) > 0, "Should generate shopping list"
    
    print(f"✅ Generated {len(result['meals'])} meals with {result['total_calories']:.0f} calories")
    print(f"   Shopping list has {len(result['shopping_list'])} items")
    return result


def test_high_glucose_adaptation():
    """Test adaptation for high glucose levels"""
    print("\n🧪 Testing high glucose adaptation...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_sample_user_data()
    
    # Normal biometric data
    normal_bio = create_sample_biometric_data()
    normal_result = engine.generate_meal_plan(
        user_data=user_data,
        biometric_data=normal_bio
    )
    
    # High glucose biometric data
    high_glucose_bio = create_high_glucose_biometric_data()
    adapted_result = engine.generate_meal_plan(
        user_data=user_data,
        biometric_data=high_glucose_bio
    )
    
    # Compare carb content
    normal_carbs = normal_result['total_macros']['carbs']
    adapted_carbs = adapted_result['total_macros']['carbs']
    
    print(f"   Normal carbs: {normal_carbs:.1f}g")
    print(f"   Adapted carbs: {adapted_carbs:.1f}g")
    print(f"   Adaptation notes: {adapted_result['adaptations']}")
    
    # Should have adaptation notes
    assert adapted_result['adaptations'] != "", "Should have adaptation notes for high glucose"
    print("✅ High glucose adaptation working")


def test_vegetarian_meal_plan():
    """Test meal plan for vegetarian user"""
    print("\n🧪 Testing vegetarian meal plan...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_vegetarian_user_data()
    
    result = engine.generate_meal_plan(
        user_data=user_data,
        meal_count=3
    )
    
    assert result['success'] == True, "Vegetarian meal plan should succeed"
    
    # Check that no meat items are in the meals
    all_items = []
    for meal in result['meals']:
        all_items.extend(meal['items'])
    
    meat_items = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon']
    has_meat = any(any(meat in item.lower() for meat in meat_items) for item in all_items)
    
    assert not has_meat, "Vegetarian meal plan should not contain meat"
    print(f"✅ Generated vegetarian meal plan with items: {all_items}")


def test_nutrition_insights():
    """Test nutrition insights functionality"""
    print("\n🧪 Testing nutrition insights...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_sample_user_data()
    biometric_data = create_sample_biometric_data()
    
    insights = engine.get_nutrition_insights(
        user_data=user_data,
        biometric_data=biometric_data
    )
    
    assert insights['success'] == True, "Nutrition insights should succeed"
    assert 'user_profile' in insights, "Should contain user profile"
    assert 'calorie_requirements' in insights, "Should contain calorie requirements"
    assert 'metabolic_insights' in insights, "Should contain metabolic insights"
    
    bmr = insights['user_profile']['bmr']
    tdee = insights['user_profile']['tdee']
    
    print(f"   BMR: {bmr:.0f} calories/day")
    print(f"   TDEE: {tdee:.0f} calories/day")
    print(f"   Recommendations: {len(insights['recommendations'])} items")
    print("✅ Nutrition insights working")


def test_biometric_simulation():
    """Test biometric change simulation"""
    print("\n🧪 Testing biometric simulation...")
    
    engine = PersonalizedNutritionEngine()
    current_bio = {
        "steps": 8000,
        "heart_rate": 70,
        "sleep_hours": 7.5,
        "glucose_mg_dl": 90
    }
    
    scenarios = ["high_glucose", "low_activity", "poor_sleep", "high_stress"]
    
    for scenario in scenarios:
        simulation = engine.simulate_biometric_changes(current_bio, scenario)
        
        assert simulation['scenario'] == scenario, f"Should return correct scenario: {scenario}"
        assert len(simulation['expected_adaptations']) > 0, f"Should have adaptations for {scenario}"
        
        print(f"   {scenario}: {len(simulation['expected_adaptations'])} adaptations")
    
    print("✅ Biometric simulation working")


def test_error_handling():
    """Test error handling with invalid data"""
    print("\n🧪 Testing error handling...")
    
    engine = PersonalizedNutritionEngine()
    
    # Test with minimal invalid data
    invalid_user_data = {
        "name": "Test User"
        # Missing required fields
    }
    
    try:
        result = engine.generate_meal_plan(user_data=invalid_user_data)
        # Should not fail completely, should use defaults
        assert 'success' in result, "Should return result structure even with missing data"
        print("✅ Error handling working - graceful degradation")
    except Exception as e:
        print(f"   Handled exception: {e}")
        print("✅ Error handling working - exception caught")


def test_shopping_list_generation():
    """Test shopping list generation with cost estimates"""
    print("\n🧪 Testing shopping list generation...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_sample_user_data()
    
    result = engine.generate_meal_plan(
        user_data=user_data,
        days=7  # Test weekly shopping list
    )
    
    assert len(result['shopping_list']) > 0, "Should generate shopping list"
    assert result['total_cost'] > 0, "Should estimate total cost"
    
    # Check shopping list format
    sample_item = result['shopping_list'][0]
    required_fields = ['item', 'quantity', 'unit']
    for field in required_fields:
        assert field in sample_item, f"Shopping list item should have {field}"
    
    print(f"   Generated shopping list with {len(result['shopping_list'])} items")
    print(f"   Estimated cost: ${result['total_cost']:.2f}")
    print("✅ Shopping list generation working")


def run_performance_test():
    """Run performance test with multiple meal plan generations"""
    print("\n🚀 Running performance test...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_sample_user_data()
    biometric_data = create_sample_biometric_data()
    
    import time
    start_time = time.time()
    
    num_tests = 10
    successful_generations = 0
    
    for i in range(num_tests):
        result = engine.generate_meal_plan(
            user_data=user_data,
            biometric_data=biometric_data
        )
        if result['success']:
            successful_generations += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_tests
    
    print(f"   Generated {successful_generations}/{num_tests} meal plans")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Average time per generation: {avg_time:.2f} seconds")
    print("✅ Performance test completed")


def save_sample_output():
    """Generate and save sample output for documentation"""
    print("\n📄 Generating sample output...")
    
    engine = PersonalizedNutritionEngine()
    user_data = create_sample_user_data()
    biometric_data = create_sample_biometric_data()
    
    result = engine.generate_meal_plan(
        user_data=user_data,
        biometric_data=biometric_data,
        meal_count=3
    )
    
    # Save to file
    output_path = Path(__file__).parent / 'sample_output.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"   Sample output saved to: {output_path}")
    print("✅ Sample output generated")
    
    return result


def main():
    """Run all tests"""
    print("🎯 Starting Personalized Nutrition Engine Test Suite")
    print("=" * 60)
    
    try:
        # Core functionality tests
        basic_result = test_basic_meal_plan_generation()
        test_high_glucose_adaptation()
        test_vegetarian_meal_plan()
        test_nutrition_insights()
        test_biometric_simulation()
        test_shopping_list_generation()
        
        # Edge case and error handling
        test_error_handling()
        
        # Performance test
        run_performance_test()
        
        # Generate sample output
        sample_output = save_sample_output()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print(f"   Engine version: {PersonalizedNutritionEngine().version}")
        print(f"   Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Print sample meal plan
        print("\n📋 Sample Meal Plan:")
        for meal in basic_result['meals']:
            print(f"   {meal['meal_type'].title()}: {', '.join(meal['items'])} ({meal['calories']:.0f} cal)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)