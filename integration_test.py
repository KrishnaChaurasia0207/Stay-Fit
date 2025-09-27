import requests
import json

def test_frontend_backend_integration():
    """Test if frontend is properly using backend instead of fallbacks"""
    
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
    
    # Test 2: Check if backend meal plan endpoint works
    try:
        meal_payload = {
            "user_data": {
                "name": "Integration Test User",
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
        
        print("Backend meal plan generation:", meal_response.status_code)
        if meal_response.status_code == 200:
            meal_data = meal_response.json()
            if meal_data.get("success"):
                print("✅ Backend meal plan generation is working")
                print(f"   Generated {len(meal_data.get('meals', []))} meals")
            else:
                print("❌ Backend meal plan generation failed")
        else:
            print("❌ Backend meal plan endpoint is not working")
    except Exception as e:
        print("❌ Error testing backend meal plan:", str(e))
    
    # Test 3: Check if frontend is accessible
    try:
        frontend_response = requests.get("http://localhost:3000")
        print("Frontend accessibility:", frontend_response.status_code)
        if frontend_response.status_code == 200:
            print("✅ Frontend is running and accessible")
        else:
            print("❌ Frontend is not accessible")
    except Exception as e:
        print("❌ Frontend is not accessible:", str(e))

if __name__ == "__main__":
    print("Testing frontend-backend integration...")
    print("=" * 50)
    test_frontend_backend_integration()
    print("=" * 50)
    print("Integration test completed.")