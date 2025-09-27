<<<<<<< HEAD
# Personalized Nutrition Optimization Engine

A production-ready backend engine that generates personalized, adaptive meal plans using user profiles, dietary preferences, optional biometric data, nutrition APIs, and complex ML models.

## Features

- **Personalized Meal Planning**: Generate meal plans based on user profile, dietary preferences, and goals
- **Real-time Biometric Adaptation**: Adapt meal plans based on wearable data (glucose, activity, sleep, heart rate)
- **ML-Powered Optimization**: Use machine learning models for meal satisfaction prediction and optimization
- **Multi-source Nutrition Data**: Local database with API fallback (Spoonacular & USDA FoodData Central)
- **Intelligent Shopping Lists**: Generate optimized shopping lists with cost estimates and substitutions
- **Dietary Restrictions Support**: Full support for vegetarian, vegan, gluten-free, and other dietary needs
- **Budget Optimization**: Optimize meal plans within specified budget constraints
- **Production Ready**: Modular, scalable architecture suitable for integration into health applications

## Activity Levels

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys (optional):
```bash
export SPOONACULAR_API_KEY="your_spoonacular_key"
export USDA_API_KEY="your_usda_key"
```

## Quick Start

```python
from nutrition_engine.engine import PersonalizedNutritionEngine

# Initialize the engine
engine = PersonalizedNutritionEngine()

# Define user profile
user_data = {
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
        "cuisine_preferences": ["mediterranean", "american"]
    }
}

# Optional biometric data
biometric_data = [
    {
        "timestamp": "2024-01-15T10:00:00",
        "steps": 8500,
        "heart_rate": 72,
        "sleep_hours": 7.5,
        "glucose_mg_dl": 95
    }
]

# Generate meal plan
result = engine.generate_meal_plan(
    user_data=user_data,
    biometric_data=biometric_data,
    meal_count=3
)

# Print results
if result['success']:
    print(f"Generated {len(result['meals'])} meals with {result['total_calories']:.0f} calories")
    for meal in result['meals']:
        print(f"{meal['meal_type']}: {', '.join(meal['items'])} ({meal['calories']:.0f} cal)")
else:
    print(f"Error: {result['error']}")
```

## API Reference

### PersonalizedNutritionEngine

The main engine class that orchestrates all nutrition optimization components.

#### Methods

##### `generate_meal_plan(user_data, preferences=None, biometric_data=None, meal_count=3, days=1)`

Generate a complete personalized meal plan.

**Parameters:**
- `user_data` (dict): User profile information
  - `name` (str): User's name
  - `age` (int): Age in years
  - `sex` (str): "male", "female", or "other"
  - `weight_kg` (float): Weight in kilograms
  - `height_cm` (float): Height in centimeters
  - `activity_level` (str): Activity level ("sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active")
  - `daily_budget` (float, optional): Daily food budget in USD
  - `dietary_preferences` (dict, optional): Dietary preferences and restrictions

- `preferences` (dict, optional): Additional meal planning preferences
- `biometric_data` (list, optional): Recent biometric data for adaptations
- `meal_count` (int): Number of meals per day (default: 3)
- `days` (int): Number of days to plan for (default: 1)

**Returns:**
```json
{
  "success": true,
  "meals": [
    {
      "meal_type": "breakfast",
      "items": ["Oatmeal", "Milk", "Banana"],
      "calories": 350,
      "protein": 15,
      "carbs": 55,
      "fat": 8
    }
  ],
  "total_calories": 1500,
  "total_macros": {
    "protein": 100,
    "carbs": 170,
    "fat": 46
  },
  "shopping_list": [
    {
      "item": "Oatmeal",
      "quantity": 100,
      "unit": "g"
    }
  ],
  "total_cost": 18.50,
  "adaptations": "Reduced carbohydrates due to high glucose reading",
  "personalization_notes": "Optimized for moderate activity level and budget constraints"
}
```

##### `get_nutrition_insights(user_data, biometric_data=None)`

Get detailed nutrition and metabolic insights for a user.

**Returns:**
```json
{
  "success": true,
  "user_profile": {
    "bmr": 1650,
    "tdee": 2285,
    "activity_level": "MODERATELY_ACTIVE",
    "bmi": 23.1
  },
  "calorie_requirements": {
    "maintenance": 2285,
    "weight_loss": 1785,
    "weight_gain": 2785
  },
  "macro_targets": {
    "calories": 2285,
    "protein_g": 143,
    "carbs_g": 257,
    "fat_g": 76
  },
  "metabolic_insights": {
    "metabolic_rate": "normal",
    "recommendations": [
      "Maintain consistent daily activity",
      "Focus on high-quality protein sources"
    ]
  }
}
```

##### `simulate_biometric_changes(current_biometrics, scenario)`

Simulate biometric changes and show adaptation responses.

**Parameters:**
- `current_biometrics` (dict): Current biometric values
- `scenario` (str): Simulation scenario ("high_glucose", "low_activity", "poor_sleep", "high_stress")

## User Data Structure

### User Profile
```python
user_data = {
    # Required fields
    "name": "John Doe",
    "age": 32,
    "sex": "male",  # "male", "female", "other"
    "weight_kg": 75.0,
    "height_cm": 180.0,
    
    # Optional fields
    "activity_level": "moderately_active",  # See activity levels below
    "daily_budget": 25.0,  # USD
    "goal_weight_kg": 70.0,
    "target_calories": 2000,
    
    # Dietary preferences
    "dietary_preferences": {
        "allergies": ["nuts", "shellfish"],
        "dislikes": ["fish", "mushrooms"],
        "cuisine_preferences": ["mediterranean", "american", "asian"],
        "dietary_restrictions": ["vegetarian"],  # See restrictions below
        "max_preparation_time": 30  # minutes
    },
    
    # Historical meal data (optional)
    "meal_history": [
        {
            "date": "2024-01-14",
            "meal_type": "breakfast",
            "foods": ["Oatmeal", "Banana", "Milk"],
            "calories": 350,
            "protein_g": 15,
            "carbs_g": 55,
            "fat_g": 8,
            "satisfaction_rating": 4  # 1-5 scale
        }
    ]
}
```

### Activity Levels
- `sedentary`: Little to no exercise
- `lightly_active`: Light exercise 1-3 days/week
- `moderately_active`: Moderate exercise 3-5 days/week
- `very_active`: Hard exercise 6-7 days/week
- `extremely_active`: Very hard exercise, physical job

### Dietary Restrictions
- `vegetarian`: No meat
- `vegan`: No animal products
- `pescatarian`: Fish but no other meat
- `keto`: Very low carb, high fat
- `paleo`: Paleolithic diet
- `low_carb`: Reduced carbohydrates
- `low_fat`: Reduced fat intake
- `gluten_free`: No gluten
- `dairy_free`: No dairy products

### Biometric Data
```python
biometric_data = [
    {
        "timestamp": "2024-01-15T10:00:00",
        "steps": 8500,
        "heart_rate": 72,  # Average resting heart rate
        "sleep_hours": 7.5,
        "glucose_mg_dl": 95,  # Blood glucose level
        "weight_kg": 75.0,
        "body_fat_percentage": 15.0,
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80
    }
]
```

## Adaptation System

The engine automatically adapts meal plans based on biometric data:

### High Glucose (>140 mg/dL)
- Reduces carbohydrate portions by 20-30%
- Increases protein slightly
- Focuses on low-glycemic foods

### Low Activity (<5000 steps)
- Reduces overall portion sizes by 15%
- Adjusts calorie targets downward

### Poor Sleep (<6 hours)
- Increases protein by 15% for recovery
- Reduces refined carbohydrates
- Focuses on sleep-supporting nutrients

### High Stress (elevated heart rate)
- Adjusts meal composition for stress management
- Reduces stimulating foods
- Emphasizes calming nutrients

## Configuration

### Environment Variables
```bash
SPOONACULAR_API_KEY=your_key_here
USDA_API_KEY=your_key_here
```

### Custom Configuration
```python
config_overrides = {
    'CACHE_ENABLED': True,
    'CACHE_EXPIRY_HOURS': 48,
    'DEFAULT_DAILY_BUDGET': 20.0,
    'HIGH_GLUCOSE_THRESHOLD': 150
}

engine = PersonalizedNutritionEngine(config_overrides)
```

## Testing

Run the comprehensive test suite:

```bash
python test_engine.py
```

The test suite includes:
- Basic meal plan generation
- Biometric adaptation testing
- Dietary restriction handling
- Nutrition insights
- Error handling
- Performance testing

## Architecture

### Core Components

1. **Engine (`engine.py`)**: Main orchestrator and API interface
2. **Models (`models.py`)**: Data models for users, meals, and biometrics
3. **Meal Planner (`meal_planner.py`)**: Core meal plan generation logic
4. **ML Models (`ml_models.py`)**: Machine learning for optimization
5. **Adaptation (`adaptation.py`)**: Real-time biometric adaptation
6. **Shopping (`shopping.py`)**: Shopping list generation
7. **Metabolism (`metabolism.py`)**: BMR/TDEE calculation
8. **API Client (`api_client.py`)**: External nutrition data integration
9. **Config (`config.py`)**: Configuration management

### Data Flow

1. User data and preferences are processed
2. Biometric data is analyzed for adaptation triggers
3. Available foods are filtered based on restrictions
4. ML models optimize meal selection
5. Real-time adaptations are applied
6. Shopping lists are generated
7. Complete meal plan is returned

## Production Deployment

### Integration Points

The engine is designed for easy integration into existing health applications:

```python
# Health app integration example
class HealthAppNutritionService:
    def __init__(self):
        self.engine = PersonalizedNutritionEngine()
    
    def generate_user_meal_plan(self, user_id: str):
        # Fetch user data from your database
        user_data = self.get_user_profile(user_id)
        biometric_data = self.get_recent_biometrics(user_id)
        
        # Generate meal plan
        meal_plan = self.engine.generate_meal_plan(
            user_data=user_data,
            biometric_data=biometric_data
        )
        
        # Store results in your database
        self.save_meal_plan(user_id, meal_plan)
        
        return meal_plan
```

### Scaling Considerations

- **Caching**: API responses are cached to reduce external API calls
- **Async Processing**: Meal plan generation can be run asynchronously
- **Database Integration**: User profiles and meal history can be stored in your database
- **API Rate Limits**: Built-in rate limiting for external nutrition APIs
- **Model Training**: ML models can be retrained with aggregated user data

### Security

- API keys are loaded from environment variables
- No user data is sent to external APIs without explicit consent
- All user data processing happens locally
- Biometric data is handled with appropriate privacy considerations

## Limitations

- Local nutrition database contains 25 food items (expandable)
- ML models improve with more user feedback data
- External API availability affects food search capabilities
- Real-time adaptation requires recent biometric data

## Support

For issues, feature requests, or integration support, please refer to the documentation or contact the development team.

## License

=======
# Personalized Nutrition Optimization Engine

A production-ready backend engine that generates personalized, adaptive meal plans using user profiles, dietary preferences, optional biometric data, nutrition APIs, and complex ML models.

## Features

- **Personalized Meal Planning**: Generate meal plans based on user profile, dietary preferences, and goals
- **Real-time Biometric Adaptation**: Adapt meal plans based on wearable data (glucose, activity, sleep, heart rate)
- **ML-Powered Optimization**: Use machine learning models for meal satisfaction prediction and optimization
- **Multi-source Nutrition Data**: Local database with API fallback (Spoonacular & USDA FoodData Central)
- **Intelligent Shopping Lists**: Generate optimized shopping lists with cost estimates and substitutions
- **Dietary Restrictions Support**: Full support for vegetarian, vegan, gluten-free, and other dietary needs
- **Budget Optimization**: Optimize meal plans within specified budget constraints
- **Production Ready**: Modular, scalable architecture suitable for integration into health applications

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys (optional):
```bash
export SPOONACULAR_API_KEY="your_spoonacular_key"
export USDA_API_KEY="your_usda_key"
```

## Quick Start

```python
from nutrition_engine.engine import PersonalizedNutritionEngine

# Initialize the engine
engine = PersonalizedNutritionEngine()

# Define user profile
user_data = {
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
        "cuisine_preferences": ["mediterranean", "american"]
    }
}

# Optional biometric data
biometric_data = [
    {
        "timestamp": "2024-01-15T10:00:00",
        "steps": 8500,
        "heart_rate": 72,
        "sleep_hours": 7.5,
        "glucose_mg_dl": 95
    }
]

# Generate meal plan
result = engine.generate_meal_plan(
    user_data=user_data,
    biometric_data=biometric_data,
    meal_count=3
)

# Print results
if result['success']:
    print(f"Generated {len(result['meals'])} meals with {result['total_calories']:.0f} calories")
    for meal in result['meals']:
        print(f"{meal['meal_type']}: {', '.join(meal['items'])} ({meal['calories']:.0f} cal)")
else:
    print(f"Error: {result['error']}")
```

## API Reference

### PersonalizedNutritionEngine

The main engine class that orchestrates all nutrition optimization components.

#### Methods

##### `generate_meal_plan(user_data, preferences=None, biometric_data=None, meal_count=3, days=1)`

Generate a complete personalized meal plan.

**Parameters:**
- `user_data` (dict): User profile information
  - `name` (str): User's name
  - `age` (int): Age in years
  - `sex` (str): "male", "female", or "other"
  - `weight_kg` (float): Weight in kilograms
  - `height_cm` (float): Height in centimeters
  - `activity_level` (str): Activity level ("sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active")
  - `daily_budget` (float, optional): Daily food budget in USD
  - `dietary_preferences` (dict, optional): Dietary preferences and restrictions

- `preferences` (dict, optional): Additional meal planning preferences
- `biometric_data` (list, optional): Recent biometric data for adaptations
- `meal_count` (int): Number of meals per day (default: 3)
- `days` (int): Number of days to plan for (default: 1)

**Returns:**
```json
{
  "success": true,
  "meals": [
    {
      "meal_type": "breakfast",
      "items": ["Oatmeal", "Milk", "Banana"],
      "calories": 350,
      "protein": 15,
      "carbs": 55,
      "fat": 8
    }
  ],
  "total_calories": 1500,
  "total_macros": {
    "protein": 100,
    "carbs": 170,
    "fat": 46
  },
  "shopping_list": [
    {
      "item": "Oatmeal",
      "quantity": 100,
      "unit": "g"
    }
  ],
  "total_cost": 18.50,
  "adaptations": "Reduced carbohydrates due to high glucose reading",
  "personalization_notes": "Optimized for moderate activity level and budget constraints"
}
```

##### `get_nutrition_insights(user_data, biometric_data=None)`

Get detailed nutrition and metabolic insights for a user.

**Returns:**
```json
{
  "success": true,
  "user_profile": {
    "bmr": 1650,
    "tdee": 2285,
    "activity_level": "MODERATELY_ACTIVE",
    "bmi": 23.1
  },
  "calorie_requirements": {
    "maintenance": 2285,
    "weight_loss": 1785,
    "weight_gain": 2785
  },
  "macro_targets": {
    "calories": 2285,
    "protein_g": 143,
    "carbs_g": 257,
    "fat_g": 76
  },
  "metabolic_insights": {
    "metabolic_rate": "normal",
    "recommendations": [
      "Maintain consistent daily activity",
      "Focus on high-quality protein sources"
    ]
  }
}
```

##### `simulate_biometric_changes(current_biometrics, scenario)`

Simulate biometric changes and show adaptation responses.

**Parameters:**
- `current_biometrics` (dict): Current biometric values
- `scenario` (str): Simulation scenario ("high_glucose", "low_activity", "poor_sleep", "high_stress")

## User Data Structure

### User Profile
```python
user_data = {
    # Required fields
    "name": "John Doe",
    "age": 32,
    "sex": "male",  # "male", "female", "other"
    "weight_kg": 75.0,
    "height_cm": 180.0,
    
    # Optional fields
    "activity_level": "moderately_active",  # See activity levels below
    "daily_budget": 25.0,  # USD
    "goal_weight_kg": 70.0,
    "target_calories": 2000,
    
    # Dietary preferences
    "dietary_preferences": {
        "allergies": ["nuts", "shellfish"],
        "dislikes": ["fish", "mushrooms"],
        "cuisine_preferences": ["mediterranean", "american", "asian"],
        "dietary_restrictions": ["vegetarian"],  # See restrictions below
        "max_preparation_time": 30  # minutes
    },
    
    # Historical meal data (optional)
    "meal_history": [
        {
            "date": "2024-01-14",
            "meal_type": "breakfast",
            "foods": ["Oatmeal", "Banana", "Milk"],
            "calories": 350,
            "protein_g": 15,
            "carbs_g": 55,
            "fat_g": 8,
            "satisfaction_rating": 4  # 1-5 scale
        }
    ]
}
```

### Activity Levels
- `sedentary`: Little to no exercise
- `lightly_active`: Light exercise 1-3 days/week
- `moderately_active`: Moderate exercise 3-5 days/week
- `very_active`: Hard exercise 6-7 days/week
- `extremely_active`: Very hard exercise, physical job

### Dietary Restrictions
- `vegetarian`: No meat
- `vegan`: No animal products
- `pescatarian`: Fish but no other meat
- `keto`: Very low carb, high fat
- `paleo`: Paleolithic diet
- `low_carb`: Reduced carbohydrates
- `low_fat`: Reduced fat intake
- `gluten_free`: No gluten
- `dairy_free`: No dairy products

### Biometric Data
```python
biometric_data = [
    {
        "timestamp": "2024-01-15T10:00:00",
        "steps": 8500,
        "heart_rate": 72,  # Average resting heart rate
        "sleep_hours": 7.5,
        "glucose_mg_dl": 95,  # Blood glucose level
        "weight_kg": 75.0,
        "body_fat_percentage": 15.0,
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80
    }
]
```

## Adaptation System

The engine automatically adapts meal plans based on biometric data:

### High Glucose (>140 mg/dL)
- Reduces carbohydrate portions by 20-30%
- Increases protein slightly
- Focuses on low-glycemic foods

### Low Activity (<5000 steps)
- Reduces overall portion sizes by 15%
- Adjusts calorie targets downward

### Poor Sleep (<6 hours)
- Increases protein by 15% for recovery
- Reduces refined carbohydrates
- Focuses on sleep-supporting nutrients

### High Stress (elevated heart rate)
- Adjusts meal composition for stress management
- Reduces stimulating foods
- Emphasizes calming nutrients

## Configuration

### Environment Variables
```bash
SPOONACULAR_API_KEY=your_key_here
USDA_API_KEY=your_key_here
```

### Custom Configuration
```python
config_overrides = {
    'CACHE_ENABLED': True,
    'CACHE_EXPIRY_HOURS': 48,
    'DEFAULT_DAILY_BUDGET': 20.0,
    'HIGH_GLUCOSE_THRESHOLD': 150
}

engine = PersonalizedNutritionEngine(config_overrides)
```

## Testing

Run the comprehensive test suite:

```bash
python test_engine.py
```

The test suite includes:
- Basic meal plan generation
- Biometric adaptation testing
- Dietary restriction handling
- Nutrition insights
- Error handling
- Performance testing

## Architecture

### Core Components

1. **Engine (`engine.py`)**: Main orchestrator and API interface
2. **Models (`models.py`)**: Data models for users, meals, and biometrics
3. **Meal Planner (`meal_planner.py`)**: Core meal plan generation logic
4. **ML Models (`ml_models.py`)**: Machine learning for optimization
5. **Adaptation (`adaptation.py`)**: Real-time biometric adaptation
6. **Shopping (`shopping.py`)**: Shopping list generation
7. **Metabolism (`metabolism.py`)**: BMR/TDEE calculation
8. **API Client (`api_client.py`)**: External nutrition data integration
9. **Config (`config.py`)**: Configuration management

### Data Flow

1. User data and preferences are processed
2. Biometric data is analyzed for adaptation triggers
3. Available foods are filtered based on restrictions
4. ML models optimize meal selection
5. Real-time adaptations are applied
6. Shopping lists are generated
7. Complete meal plan is returned

## Production Deployment

### Integration Points

The engine is designed for easy integration into existing health applications:

```python
# Health app integration example
class HealthAppNutritionService:
    def __init__(self):
        self.engine = PersonalizedNutritionEngine()
    
    def generate_user_meal_plan(self, user_id: str):
        # Fetch user data from your database
        user_data = self.get_user_profile(user_id)
        biometric_data = self.get_recent_biometrics(user_id)
        
        # Generate meal plan
        meal_plan = self.engine.generate_meal_plan(
            user_data=user_data,
            biometric_data=biometric_data
        )
        
        # Store results in your database
        self.save_meal_plan(user_id, meal_plan)
        
        return meal_plan
```

### Scaling Considerations

- **Caching**: API responses are cached to reduce external API calls
- **Async Processing**: Meal plan generation can be run asynchronously
- **Database Integration**: User profiles and meal history can be stored in your database
- **API Rate Limits**: Built-in rate limiting for external nutrition APIs
- **Model Training**: ML models can be retrained with aggregated user data

### Security

- API keys are loaded from environment variables
- No user data is sent to external APIs without explicit consent
- All user data processing happens locally
- Biometric data is handled with appropriate privacy considerations

## Limitations

- Local nutrition database contains 25 food items (expandable)
- ML models improve with more user feedback data
- External API availability affects food search capabilities
- Real-time adaptation requires recent biometric data

## Support

For issues, feature requests, or integration support, please refer to the documentation or contact the development team.

## License

>>>>>>> bc2e5f79847cba85284b54c4c7ecf4b55b7b6c4b
This project is proprietary software designed for integration into commercial health and nutrition applications.