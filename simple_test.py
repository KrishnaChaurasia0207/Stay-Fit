import requests
import json
import time

def test_api_endpoints():
    # Wait a moment for the server to fully start
    time.sleep(2)
    
    print("Testing Nutrition Engine API Endpoints...")
    print("=" * 50)
    
    try:
        # Test health check
        print("1. Testing Health Check Endpoint...")
        response = requests.get('http://localhost:8000/health-check', timeout=5)
        if response.status_code == 200:
            print("   ✓ Health check successful")
            print(f"   Status: {response.json().get('status')}")
        else:
            print(f"   ✗ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
    
    try:
        # Test ML satisfaction prediction
        print("\n2. Testing ML Satisfaction Prediction...")
        satisfaction_payload = {
            "user_data": {
                "name": "John Doe",
                "age": 30,
                "sex": "male",
                "weight_kg": 75,
                "height_cm": 180,
                "activity_level": "moderately_active",
                "daily_budget": 20.0,
                "dietary_preferences": {
                    "allergies": ["gluten"],
                    "dislikes": ["broccoli"],
                    "cuisine_preferences": ["italian", "mexican"]
                }
            },
            "food_data": {
                "name": "Grilled Chicken Breast",
                "calories_per_100g": 165,
                "protein_g": 31,
                "carbs_g": 0,
                "fat_g": 3.6,
                "cost_per_100g": 2.5,
                "preparation_time": 15,
                "allergens": [],
                "category": "protein"
            }
        }
        
        response = requests.post(
            'http://localhost:8000/ml/predict-satisfaction',
            json=satisfaction_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✓ Satisfaction prediction successful")
            if result.get('success'):
                score = result.get('satisfaction_score')
                print(f"   Predicted satisfaction score: {score:.2f}/5.0")
            else:
                print(f"   Error: {result.get('error')}")
        else:
            print(f"   ✗ Satisfaction prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Satisfaction prediction error: {e}")
    
    try:
        # Test ML meal optimization
        print("\n3. Testing ML Meal Optimization...")
        optimization_payload = {
            "user_data": {
                "name": "John Doe",
                "age": 30,
                "sex": "male",
                "weight_kg": 75,
                "height_cm": 180,
                "activity_level": "moderately_active",
                "daily_budget": 20.0,
                "dietary_preferences": {
                    "allergies": ["gluten"],
                    "dislikes": ["broccoli"],
                    "cuisine_preferences": ["italian", "mexican"]
                }
            },
            "available_foods": [
                {
                    "name": "Grilled Chicken Breast",
                    "calories_per_100g": 165,
                    "protein_g": 31,
                    "carbs_g": 0,
                    "fat_g": 3.6,
                    "cost_per_100g": 2.5,
                    "preparation_time": 15,
                    "allergens": [],
                    "category": "protein"
                },
                {
                    "name": "Brown Rice",
                    "calories_per_100g": 111,
                    "protein_g": 2.6,
                    "carbs_g": 23,
                    "fat_g": 0.9,
                    "cost_per_100g": 0.8,
                    "preparation_time": 25,
                    "allergens": [],
                    "category": "carbohydrate"
                },
                {
                    "name": "Broccoli",
                    "calories_per_100g": 34,
                    "protein_g": 2.8,
                    "carbs_g": 7,
                    "fat_g": 0.4,
                    "cost_per_100g": 1.2,
                    "preparation_time": 10,
                    "allergens": [],
                    "category": "vegetable"
                }
            ],
            "target_calories": {"calories": 2000},
            "meal_types": ["breakfast", "lunch", "dinner"]
        }
        
        response = requests.post(
            'http://localhost:8000/ml/optimize-meals',
            json=optimization_payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✓ Meal optimization successful")
            if result.get('success'):
                meals = result.get('meals', [])
                print(f"   Generated {len(meals)} optimized meals")
                for meal in meals:
                    print(f"     - {meal.get('meal_type', 'N/A').title()}: {', '.join(meal.get('items', []))}")
            else:
                print(f"   Error: {result.get('error')}")
        else:
            print(f"   ✗ Meal optimization failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Meal optimization error: {e}")
    
    print("\n" + "=" * 50)
    print("API Testing Complete!")

if __name__ == "__main__":
    test_api_endpoints()