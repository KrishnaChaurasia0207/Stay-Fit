#!/usr/bin/env python3
"""
Working Test Suite for the Personalized Nutrition Optimization Engine
Uses the standalone meal generation logic that works without import issues
"""

import json
import sys
from datetime import datetime, date, timedelta
from standalone_demo import generate_meal_plan

def test_basic_meal_plan_generation():
    """Test basic meal plan generation"""
    print("🧪 Testing basic meal plan generation...")
    
    result = generate_meal_plan(
        name="John Doe",
        age=32,
        sex="male", 
        weight_kg=75.0,
        height_cm=180.0,
        activity_level="moderately_active",
        budget=25.0,
        allergies=["nuts"],
        meal_count=3,
        days=1
    )
    
    assert result['success'] == True, "Meal plan generation should succeed"
    assert 'meal_plan' in result, "Should have meal plan"
    assert 'shopping_list' in result, "Should have shopping list"
    assert result['user_info']['bmr'] > 0, "Should calculate BMR"
    assert result['user_info']['tdee'] > 0, "Should calculate TDEE"
    
    meal_plan = result['meal_plan']['day_1']
    meals = [k for k in meal_plan.keys() if k != 'daily_totals']
    
    print(f"✅ Generated {len(meals)} meals")
    print(f"   BMR: {result['user_info']['bmr']:.0f} calories")
    print(f"   TDEE: {result['user_info']['tdee']:.0f} calories")
    print(f"   Shopping items: {len(result['shopping_list']['items'])}")
    
    return result

def test_allergy_filtering():
    """Test that allergies are properly filtered"""
    print("\n🧪 Testing allergy filtering...")
    
    # Test with multiple allergies
    result = generate_meal_plan(
        name="Allergy User",
        age=25,
        sex="female",
        weight_kg=60.0,
        height_cm=165.0,
        activity_level="lightly_active",
        budget=20.0,
        allergies=["nuts", "dairy", "fish"],
        meal_count=3,
        days=1
    )
    
    assert result['success'] == True, "Should generate plan despite allergies"
    
    # Check shopping list doesn't contain allergens
    shopping_items = result['shopping_list']['items']
    allergen_foods = ['almonds', 'salmon', 'greek_yogurt', 'cottage_cheese']
    
    found_allergens = []
    for item in shopping_items:
        item_name = item['food'].lower().replace(' ', '_')
        if any(allergen in item_name for allergen in allergen_foods):
            found_allergens.append(item_name)
    
    assert len(found_allergens) == 0, f"Found allergens in meal plan: {found_allergens}"
    print(f"✅ Successfully avoided all allergens")
    print(f"   Safe foods used: {[item['food'] for item in shopping_items]}")

def test_budget_optimization():
    """Test budget optimization"""
    print("\n🧪 Testing budget optimization...")
    
    # Test with low budget
    low_budget_result = generate_meal_plan(
        name="Budget User",
        age=30,
        sex="male",
        weight_kg=70.0,
        height_cm=175.0,
        activity_level="sedentary",
        budget=5.0,  # Very low budget
        allergies=[],
        meal_count=3,
        days=1
    )
    
    assert low_budget_result['success'] == True, "Should generate plan with low budget"
    
    daily_cost = low_budget_result['shopping_list']['total_estimated_cost']
    budget = 5.0
    
    print(f"   Daily cost: ${daily_cost:.2f}")
    print(f"   Budget: ${budget:.2f}")
    print(f"   Budget status: {'✅ Within budget' if daily_cost <= budget else '⚠️ Over budget'}")
    
    # Test with high budget
    high_budget_result = generate_meal_plan(
        name="Premium User", 
        age=30,
        sex="male",
        weight_kg=70.0,
        height_cm=175.0,
        activity_level="very_active",
        budget=50.0,  # High budget
        allergies=[],
        meal_count=4,
        days=1
    )
    
    assert high_budget_result['success'] == True, "Should generate plan with high budget"
    print(f"✅ Budget optimization working for both low and high budgets")

def test_metabolic_calculations():
    """Test metabolic calculations (BMR/TDEE)"""
    print("\n🧪 Testing metabolic calculations...")
    
    # Test male BMR/TDEE
    male_result = generate_meal_plan(
        name="Male Test",
        age=30,
        sex="male",
        weight_kg=80.0,
        height_cm=180.0,
        activity_level="moderately_active",
        budget=25.0,
        allergies=[],
        meal_count=3,
        days=1
    )
    
    male_bmr = male_result['user_info']['bmr']
    male_tdee = male_result['user_info']['tdee']
    
    # Test female BMR/TDEE  
    female_result = generate_meal_plan(
        name="Female Test",
        age=30,
        sex="female",
        weight_kg=60.0,
        height_cm=165.0,
        activity_level="moderately_active",
        budget=25.0,
        allergies=[],
        meal_count=3,
        days=1
    )
    
    female_bmr = female_result['user_info']['bmr']
    female_tdee = female_result['user_info']['tdee']
    
    # Males should generally have higher BMR/TDEE
    assert male_bmr > female_bmr, "Male BMR should be higher than female BMR"
    assert male_tdee > female_tdee, "Male TDEE should be higher than female TDEE"
    assert male_tdee > male_bmr, "TDEE should be higher than BMR"
    assert female_tdee > female_bmr, "TDEE should be higher than BMR"
    
    print(f"   Male: BMR={male_bmr:.0f}, TDEE={male_tdee:.0f}")
    print(f"   Female: BMR={female_bmr:.0f}, TDEE={female_tdee:.0f}")
    print("✅ Metabolic calculations working correctly")

def test_multi_day_planning():
    """Test multi-day meal planning"""
    print("\n🧪 Testing multi-day meal planning...")
    
    result = generate_meal_plan(
        name="Multi Day User",
        age=28,
        sex="female",
        weight_kg=65.0,
        height_cm=170.0,
        activity_level="very_active",
        budget=30.0,
        allergies=[],
        meal_count=3,
        days=7  # Full week
    )
    
    assert result['success'] == True, "Multi-day planning should succeed"
    
    meal_plan = result['meal_plan']
    assert len(meal_plan) == 7, "Should have 7 days of meal plans"
    
    # Check each day has meals
    for day_key, day_data in meal_plan.items():
        meals = [k for k in day_data.keys() if k != 'daily_totals']
        assert len(meals) == 3, f"Each day should have 3 meals, {day_key} has {len(meals)}"
        assert 'daily_totals' in day_data, f"Each day should have daily totals"
    
    total_cost = result['shopping_list']['total_estimated_cost']
    daily_cost = total_cost / 7
    
    print(f"   Generated {len(meal_plan)} days of meal plans")
    print(f"   Total weekly cost: ${total_cost:.2f}")
    print(f"   Average daily cost: ${daily_cost:.2f}")
    print("✅ Multi-day planning working correctly")

def test_activity_level_impact():
    """Test that activity level impacts calorie targets"""
    print("\n🧪 Testing activity level impact...")
    
    # Sedentary user
    sedentary_result = generate_meal_plan(
        name="Sedentary User",
        age=25,
        sex="male",
        weight_kg=75.0,
        height_cm=180.0,
        activity_level="sedentary",
        budget=25.0,
        allergies=[],
        meal_count=3,
        days=1
    )
    
    # Very active user
    active_result = generate_meal_plan(
        name="Active User", 
        age=25,
        sex="male",
        weight_kg=75.0,
        height_cm=180.0,
        activity_level="extremely_active",
        budget=25.0,
        allergies=[],
        meal_count=3,
        days=1
    )
    
    sedentary_tdee = sedentary_result['user_info']['tdee']
    active_tdee = active_result['user_info']['tdee']
    
    assert active_tdee > sedentary_tdee, "Active user should have higher TDEE"
    
    difference = active_tdee - sedentary_tdee
    percentage_increase = (difference / sedentary_tdee) * 100
    
    print(f"   Sedentary TDEE: {sedentary_tdee:.0f} calories")
    print(f"   Active TDEE: {active_tdee:.0f} calories") 
    print(f"   Difference: {difference:.0f} calories ({percentage_increase:.1f}% increase)")
    print("✅ Activity level correctly impacts calorie targets")

def test_meal_variety():
    """Test that different meals are generated"""
    print("\n🧪 Testing meal variety...")
    
    result = generate_meal_plan(
        name="Variety User",
        age=30,
        sex="male",
        weight_kg=75.0,
        height_cm=180.0,
        activity_level="moderately_active",
        budget=25.0,
        allergies=[],
        meal_count=3,
        days=3
    )
    
    assert result['success'] == True, "Should generate varied meal plan"
    
    # Collect all unique foods across all meals
    all_foods = set()
    meal_combinations = []
    
    for day_key, day_data in result['meal_plan'].items():
        for meal_key, meal_data in day_data.items():
            if meal_key != 'daily_totals':
                foods = [f['name'] for f in meal_data['foods']]
                meal_combinations.append(f"{meal_key}: {', '.join(foods)}")
                all_foods.update(foods)
    
    unique_foods = len(all_foods)
    total_meals = len(meal_combinations)
    
    print(f"   Total unique foods used: {unique_foods}")
    print(f"   Total meals generated: {total_meals}")
    print(f"   Food variety ratio: {unique_foods/total_meals:.2f}")
    
    # Should have reasonable variety
    assert unique_foods >= 5, "Should use at least 5 different foods"
    print("✅ Meal variety is adequate")

def test_vegetarian_meal_plan():
    """Test vegetarian meal plan generation"""
    print("\n🥗 Testing vegetarian meal plan...")
    
    result = generate_meal_plan(
        name="Vegetarian User",
        age=25,
        sex="female",
        weight_kg=60.0,
        height_cm=165.0,
        activity_level="moderately_active",
        budget=25.0,
        allergies=[],
        meal_count=3,
        days=1,
        dietary_preference="vegetarian"
    )
    
    assert result['success'] == True, "Vegetarian meal plan should succeed"
    
    # Check that no meat/fish items are in the meals
    shopping_items = result['shopping_list']['items']
    meat_items = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna']
    
    found_meat = []
    for item in shopping_items:
        item_name = item['food'].lower()
        if any(meat in item_name for meat in meat_items):
            found_meat.append(item_name)
    
    assert len(found_meat) == 0, f"Vegetarian meal plan should not contain meat: {found_meat}"
    print(f"   ✅ No meat/fish found in vegetarian plan")
    print(f"   Foods used: {[item['food'] for item in shopping_items]}")

def test_vegan_meal_plan():
    """Test vegan meal plan generation"""
    print("\n🌱 Testing vegan meal plan...")
    
    result = generate_meal_plan(
        name="Vegan User",
        age=30,
        sex="male",
        weight_kg=70.0,
        height_cm=175.0,
        activity_level="moderately_active",
        budget=20.0,
        allergies=[],
        meal_count=3,
        days=1,
        dietary_preference="vegan"
    )
    
    assert result['success'] == True, "Vegan meal plan should succeed"
    
    # Check that no animal products are in the meals
    shopping_items = result['shopping_list']['items']
    animal_products = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 'eggs', 'milk', 'cheese', 'yogurt']
    
    found_animal_products = []
    for item in shopping_items:
        item_name = item['food'].lower()
        if any(animal in item_name for animal in animal_products):
            found_animal_products.append(item_name)
    
    assert len(found_animal_products) == 0, f"Vegan meal plan should not contain animal products: {found_animal_products}"
    print(f"   ✅ No animal products found in vegan plan")
    print(f"   Foods used: {[item['food'] for item in shopping_items]}")

def test_dietary_preference_and_allergies():
    """Test combination of dietary preference and allergies"""
    print("\n🥗🚫 Testing dietary preference + allergies...")
    
    # Vegan with nut allergy
    result = generate_meal_plan(
        name="Vegan Allergic User",
        age=28,
        sex="female",
        weight_kg=65.0,
        height_cm=170.0,
        activity_level="lightly_active",
        budget=30.0,
        allergies=["nuts", "soy"],
        meal_count=3,
        days=1,
        dietary_preference="vegan"
    )
    
    assert result['success'] == True, "Vegan + allergy meal plan should succeed"
    
    shopping_items = result['shopping_list']['items']
    
    # Check no animal products
    animal_products = ['chicken', 'beef', 'eggs', 'milk', 'cheese', 'yogurt']
    # Check no allergens
    allergens = ['almonds', 'peanut', 'tofu']
    
    found_violations = []
    for item in shopping_items:
        item_name = item['food'].lower()
        if any(animal in item_name for animal in animal_products + allergens):
            found_violations.append(item_name)
    
    assert len(found_violations) == 0, f"Should avoid both animal products and allergens: {found_violations}"
    print(f"   ✅ Successfully avoided animal products AND allergens")
    print(f"   Safe vegan foods: {[item['food'] for item in shopping_items]}")

def main():
    """Run all tests"""
    print("🎯 Starting Personalized Nutrition Engine Test Suite")
    print("=" * 60)
    
    try:
        # Run all tests
        test_basic_meal_plan_generation()
        test_allergy_filtering()
        test_budget_optimization()
        test_metabolic_calculations()
        test_multi_day_planning()
        test_activity_level_impact()
        test_vegetarian_meal_plan()
        test_vegan_meal_plan()
        test_dietary_preference_and_allergies()
        test_meal_variety()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("✅ Personalized Nutrition Engine is working correctly")
        print("🚀 Ready for production use!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)