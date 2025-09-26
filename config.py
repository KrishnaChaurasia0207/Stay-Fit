"""
Configuration settings for the Personalized Nutrition Optimization Engine
"""

import os
from typing import Dict, Any

class Config:
    """Main configuration class for the nutrition engine"""
    
    # API Configuration
    SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY', 'b5243cc8fe664369af9d849488fc9c82')
    USDA_API_KEY = os.getenv('USDA_API_KEY', 'BGOU8660WZCtxcdfx72HwI8ZtjI2PVhyhKc43yD8')
    
    # API Endpoints
    SPOONACULAR_BASE_URL = "https://api.spoonacular.com"
    USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    
    # Cache Configuration
    CACHE_ENABLED = True
    CACHE_EXPIRY_HOURS = 24
    CACHE_MAX_SIZE = 1000
    
    # Local Database
    LOCAL_DB_PATH = "data/nutrition_db.json"
    CACHE_DB_PATH = "data/api_cache.json"
    
    # ML Model Configuration
    MODEL_UPDATE_THRESHOLD = 10  # Number of interactions before model update
    LEARNING_RATE = 0.01
    
    # Nutrition Targets (per 100g)
    DEFAULT_MACRO_RATIOS = {
        "protein": 0.25,  # 25% of calories from protein
        "carbs": 0.45,    # 45% of calories from carbs
        "fat": 0.30       # 30% of calories from fat
    }
    
    # Meal Distribution
    MEAL_CALORIE_DISTRIBUTION = {
        "breakfast": 0.25,
        "lunch": 0.40,
        "dinner": 0.35
    }
    
    # Budget and Cost Settings
    DEFAULT_DAILY_BUDGET = 15.0  # USD
    COST_WEIGHT_FACTOR = 0.2     # How much to weight cost in optimization
    
    # Biometric Thresholds for Adaptations
    HIGH_GLUCOSE_THRESHOLD = 140  # mg/dl
    LOW_ACTIVITY_THRESHOLD = 5000  # steps
    POOR_SLEEP_THRESHOLD = 6      # hours
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API configuration dictionary"""
        return {
            'spoonacular': {
                'key': cls.SPOONACULAR_API_KEY,
                'base_url': cls.SPOONACULAR_BASE_URL
            },
            'usda': {
                'key': cls.USDA_API_KEY,
                'base_url': cls.USDA_BASE_URL
            }
        }