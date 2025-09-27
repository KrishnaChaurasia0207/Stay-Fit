import requests
import json

def test_image_integration():
    """Test the image integration between frontend and backend"""
    
    # Test 1: Check if backend is accessible
    try:
        backend_health = requests.get("http://localhost:8000/health-check")
        print("Backend health check:", backend_health.status_code)
        if backend_health.status_code == 200:
            print("✅ Backend is running and accessible")
        else:
            print("❌ Backend is not accessible")
            return
    except Exception as e:
        print("❌ Backend is not accessible:", str(e))
        return
    
    # Test 2: Check if image serving endpoint works
    try:
        image_response = requests.get("http://localhost:8000/images/chicken_breast.jpg")
        print("Image serving endpoint:", image_response.status_code)
        if image_response.status_code == 200:
            print("✅ Image serving endpoint is working")
        else:
            print("❌ Image serving endpoint is not working")
    except Exception as e:
        print("❌ Error testing image serving endpoint:", str(e))
    
    # Test 3: Check if meal plan generation includes image URLs
    try:
        meal_payload = {
            "user_data": {
                "name": "Image Test User",
                "age": 25,
                "sex": "male",
                "weight_kg": 70,
                "height_cm": 175
            }
        }
        
        meal_response = requests.post(
            "http://localhost:8000/meal-plan",
            headers={"Content-Type": "application/json"},
            json=meal_payload
        )
        
        print("Meal plan generation:", meal_response.status_code)
        if meal_response.status_code == 200:
            meal_data = meal_response.json()
            if meal_data.get("success"):
                print("✅ Meal plan generation is working")
                # Check if meals include image URLs
                meals = meal_data.get("meals", [])
                if meals and len(meals) > 0:
                    first_meal = meals[0]
                    if "image_urls" in first_meal:
                        print("✅ Meal plan includes image URLs")
                        print(f"   First meal has {len(first_meal['image_urls'])} image URLs")
                        if len(first_meal['image_urls']) > 0:
                            print(f"   First image URL: {first_meal['image_urls'][0]}")
                    else:
                        print("❌ Meal plan does not include image URLs")
                else:
                    print("❌ No meals in response")
            else:
                print("❌ Meal plan generation failed")
        else:
            print("❌ Meal plan endpoint is not working")
    except Exception as e:
        print("❌ Error testing meal plan generation:", str(e))

if __name__ == "__main__":
    print("Testing image integration between frontend and backend...")
    print("=" * 60)
    test_image_integration()
    print("=" * 60)
    print("Image integration test completed.")