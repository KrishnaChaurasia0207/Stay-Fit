# Multi-Agent Nutrition Engine - Backend API

This directory contains the FastAPI backend for the Multi-Agent Nutrition Engine, providing a production-ready REST API for external integration.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

This will install all required packages including FastAPI and Uvicorn.

### Starting the Server
To start the backend server, run:
```bash
python start_backend.py
```

The server will start on `http://localhost:8000` with auto-reload enabled.

## 📚 API Documentation

Once the server is running, you can access:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health-check
- **API Root**: http://localhost:8000/

## 🛠️ API Endpoints

### GET `/`
Health check endpoint that returns basic information about the API.

### GET `/health-check`
Comprehensive health check that verifies:
- Database connectivity
- API functionality
- System status

### GET `/foods`
Returns all foods available in the nutrition database.

### POST `/meal-plan`
Generates a personalized meal plan based on user data and biometric information.

**Request Body:**
```json
{
  "user_data": {
    "name": "string",
    "age": "integer",
    "sex": "string",
    "weight_kg": "number",
    "height_cm": "number",
    "activity_level": "string (optional)",
    "daily_budget": "number (optional)",
    "dietary_preferences": "object (optional)"
  },
  "biometric_data": [
    {
      "timestamp": "string (optional)",
      "glucose_mg_dl": "number (optional)",
      "sleep_hours": "number (optional)",
      "steps": "integer (optional)"
    }
  ],
  "options": "object (optional)"
}
```

**Response:**
```json
{
  "success": "boolean",
  "meals": "array",
  "total_calories": "number",
  "total_macros": {
    "protein": "number",
    "carbs": "number",
    "fat": "number"
  },
  "shopping_list": "array",
  "total_cost": "number",
  "adaptations": "string",
  "personalization_notes": "string",
  "metabolic_profile": {
    "bmr": "number",
    "tdee": "number",
    "bmi": "number"
  },
  "generated_at": "string",
  "api_version": "string"
}
```

## 🧪 End-to-End Scenarios

To run the end-to-end meal planning scenarios:
```bash
python end_to_end_scenarios.py
```

This demonstrates various use cases:
1. Basic meal planning for a healthy adult
2. Meal planning for a diabetic patient with glucose monitoring
3. High-protein meal planning for an athlete
4. Budget-conscious meal planning for a student

## 🏗️ Architecture

The backend is built with:
- **FastAPI**: High-performance web framework
- **Uvicorn**: ASGI server for async support
- **Pydantic**: Data validation and serialization

## 📖 Usage Examples

### Python Client Example
```python
import requests

# Generate a meal plan
user_data = {
    "name": "John Doe",
    "age": 30,
    "sex": "male",
    "weight_kg": 75,
    "height_cm": 180
}

response = requests.post(
    "http://localhost:8000/meal-plan",
    json={"user_data": user_data}
)

if response.status_code == 200:
    meal_plan = response.json()
    print(f"Generated {len(meal_plan['meals'])} meals")
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/meal-plan" \
     -H "Content-Type: application/json" \
     -d '{
           "user_data": {
             "name": "John Doe",
             "age": 30,
             "sex": "male",
             "weight_kg": 75,
             "height_cm": 180
           }
         }'
```

## 🧪 Testing

Run the end-to-end scenarios to test the API:
```bash
python end_to_end_scenarios.py
```

Make sure the backend server is running before executing the scenarios.

## 📈 Features

- **Real-time Health Adaptation**: Adjusts meal plans based on biometric data
- **Budget Optimization**: Creates cost-effective meal plans within user budgets
- **Allergy Awareness**: Filters foods based on user allergies
- **Personalized Nutrition**: Tailors plans to individual metabolic profiles
- **Shopping List Generation**: Automatically creates shopping lists from meal plans
- **API Documentation**: Auto-generated interactive API documentation

## 🛡️ Error Handling

The API provides comprehensive error handling:
- Input validation with detailed error messages
- Internal server error handling
- HTTP status codes for different error types

## 🚀 Deployment

For production deployment, consider using:
- **Gunicorn** or **Uvicorn** with multiple workers
- **Docker** for containerization
- **Nginx** as a reverse proxy
- **Cloud platforms** like AWS, GCP, or Azure

Example production command:
```bash
uvicorn start_backend:app --host 0.0.0.0 --port 8000 --workers 4
```