import requests
import json

def test_health_check():
    try:
        response = requests.get('http://localhost:8000/health-check')
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_ml_endpoints():
    # Test data
    test_user = {
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
    }

    test_food = {
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

    test_foods = [
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
    ]

    try:
        # Test satisfaction prediction
        print("\nTesting ML Satisfaction Prediction...")
        satisfaction_payload = {
            "user_data": test_user,
            "food_data": test_food
        }
        response = requests.post('http://localhost:8000/ml/predict-satisfaction', json=satisfaction_payload)
        print("Satisfaction Prediction Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error testing satisfaction prediction: {e}")

    try:
        # Test meal optimization
        print("\nTesting ML Meal Optimization...")
        optimization_payload = {
            "user_data": test_user,
            "available_foods": test_foods,
            "target_calories": {"calories": 2000},
            "meal_types": ["breakfast", "lunch", "dinner"]
        }
        response = requests.post('http://localhost:8000/ml/optimize-meals', json=optimization_payload)
        print("Meal Optimization Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error testing meal optimization: {e}")

if __name__ == "__main__":
    print("Testing Nutrition Engine API...")
    print("=" * 40)
    
    if test_health_check():
        test_ml_endpoints()
    else:
        print("Failed to connect to the API server")