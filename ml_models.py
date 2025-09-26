"""
Machine Learning models for meal recommendation and optimization
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from scipy.optimize import minimize
import joblib

from models import UserProfile, MealHistory
from config import Config


class NutritionFeatureExtractor:
    """Extract features for ML models"""
    
    def __init__(self):
        self.scalers = {}
        self.fitted = False
    
    def extract_user_features(self, profile: UserProfile) -> Dict[str, float]:
        """Extract features from user profile"""
        features = {
            'age': profile.age,
            'sex_male': 1.0 if profile.sex.lower() == 'male' else 0.0,
            'weight_kg': profile.weight_kg,
            'height_cm': profile.height_cm,
            'bmi': profile.weight_kg / ((profile.height_cm / 100) ** 2),
            'activity_level': profile.activity_level.value,
            'bmr': profile.calculate_bmr(),
            'tdee': profile.calculate_tdee(),
            'daily_budget': profile.daily_budget or Config.DEFAULT_DAILY_BUDGET,
            'vegetarian': 1.0 if any('vegetarian' in str(dr).lower() for dr in profile.dietary_preferences.dietary_restrictions) else 0.0,
            'vegan': 1.0 if any('vegan' in str(dr).lower() for dr in profile.dietary_preferences.dietary_restrictions) else 0.0,
            'num_allergies': len(profile.dietary_preferences.allergies),
            'num_preferred_foods': len(profile.preferred_foods),
        }
        
        # Recent biometric features
        latest_bio = profile.get_latest_biometrics()
        if latest_bio:
            features.update({
                'recent_steps': latest_bio.steps or 5000,
                'recent_heart_rate': latest_bio.heart_rate or 70,
                'recent_sleep_hours': latest_bio.sleep_hours or 7.5,
                'recent_glucose': latest_bio.glucose_mg_dl or 90,
            })
        else:
            features.update({
                'recent_steps': 5000,
                'recent_heart_rate': 70,
                'recent_sleep_hours': 7.5,
                'recent_glucose': 90,
            })
        
        return features
    
    def extract_food_features(self, food_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from food item"""
        features = {
            'calories_per_100g': food_data.get('calories_per_100g', 0),
            'protein_g': food_data.get('protein_g', 0),
            'carbs_g': food_data.get('carbs_g', 0),
            'fat_g': food_data.get('fat_g', 0),
            'cost_per_100g': food_data.get('cost_per_100g', 1.0),
            'preparation_time': food_data.get('preparation_time', 10),
            'has_dairy': 1.0 if 'dairy' in food_data.get('allergens', []) else 0.0,
            'has_gluten': 1.0 if 'gluten' in food_data.get('allergens', []) else 0.0,
            'category_protein': 1.0 if food_data.get('category') == 'protein' else 0.0,
            'category_carbohydrate': 1.0 if food_data.get('category') == 'carbohydrate' else 0.0,
            'category_vegetable': 1.0 if food_data.get('category') == 'vegetable' else 0.0,
        }
        return features


class MealSatisfactionPredictor:
    """Predict meal satisfaction using user history"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42)
        self.feature_extractor = NutritionFeatureExtractor()
        self.trained = False
    
    def train(self, profiles: List[UserProfile], meal_histories: List[List[MealHistory]]):
        """Train the satisfaction prediction model"""
        features = []
        targets = []
        
        for profile, meals in zip(profiles, meal_histories):
            user_features = self.feature_extractor.extract_user_features(profile)
            
            for meal in meals:
                if meal.satisfaction_rating is not None:
                    # Create synthetic food features from meal data
                    food_features = {
                        'calories_per_100g': meal.calories,
                        'protein_g': meal.protein_g,
                        'carbs_g': meal.carbs_g,
                        'fat_g': meal.fat_g,
                        'cost_per_100g': meal.cost or 2.0,
                        'preparation_time': meal.preparation_time or 15,
                        'has_dairy': 0.0, 'has_gluten': 0.0,
                        'category_protein': 0.5, 'category_carbohydrate': 0.3,
                        'category_vegetable': 0.2,
                    }
                    
                    combined_features = {**user_features, **food_features}
                    features.append(combined_features)
                    targets.append(meal.satisfaction_rating)
        
        if not features:
            return
        
        # Convert to arrays
        feature_names = list(features[0].keys())
        X = np.array([[f[name] for name in feature_names] for f in features])
        y = np.array(targets)
        
        self.model.fit(X, y)
        self.feature_names = feature_names
        self.trained = True
    
    def predict_satisfaction(self, profile: UserProfile, food_data: Dict[str, Any]) -> float:
        """Predict satisfaction score for a food item"""
        if not self.trained:
            return 3.0
        
        user_features = self.feature_extractor.extract_user_features(profile)
        food_features = self.feature_extractor.extract_food_features(food_data)
        combined_features = {**user_features, **food_features}
        
        X = np.array([[combined_features.get(name, 0) for name in self.feature_names]])
        prediction = self.model.predict(X)[0]
        return max(1.0, min(5.0, prediction))


class MealOptimizer:
    """Multi-objective optimization for meal planning"""
    
    def __init__(self):
        self.satisfaction_predictor = MealSatisfactionPredictor()
    
    def optimize_meal_plan(self, profile: UserProfile, available_foods: List[Dict[str, Any]],
                          target_calories: Dict[str, float], 
                          meal_types: List[str] = None) -> Dict[str, Any]:
        """Optimize meal plan using multi-objective optimization"""
        if meal_types is None:
            meal_types = ['breakfast', 'lunch', 'dinner']
        
        # Filter allowed foods
        allowed_foods = [food for food in available_foods if profile.is_food_allowed(food)]
        
        if not allowed_foods:
            return {'success': False, 'error': 'No allowed foods available'}
        
        # Calorie distribution
        calorie_distribution = Config.MEAL_CALORIE_DISTRIBUTION
        total_target_calories = target_calories.get('calories', profile.calculate_tdee())
        
        optimized_meals = []
        total_cost = 0
        total_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        for meal_type in meal_types:
            meal_target_calories = total_target_calories * calorie_distribution.get(meal_type, 0.33)
            
            # Score each food for this meal
            food_scores = []
            for food in allowed_foods:
                satisfaction_score = self.satisfaction_predictor.predict_satisfaction(profile, food)
                nutrition_density = self._calculate_nutrition_density(food)
                cost_efficiency = 1.0 / max(food.get('cost_per_100g', 1), 0.1)
                meal_fit = self._calculate_meal_type_fit(food, meal_type)
                
                combined_score = (satisfaction_score * 0.4 + nutrition_density * 0.3 + 
                                cost_efficiency * 0.2 + meal_fit * 0.1)
                
                food_scores.append({'food': food, 'score': combined_score})
            
            # Select best food for this meal
            food_scores.sort(key=lambda x: x['score'], reverse=True)
            selected_food = food_scores[0]['food']
            
            # Calculate portion size
            portion_size = meal_target_calories / max(selected_food.get('calories_per_100g', 100), 1) * 100
            portion_size = min(portion_size, 400)  # Cap at 400g
            
            actual_calories = selected_food.get('calories_per_100g', 0) * portion_size / 100
            
            meal = {
                'meal_type': meal_type,
                'items': [selected_food['name']],
                'calories': actual_calories,
                'protein': selected_food.get('protein_g', 0) * portion_size / 100,
                'carbs': selected_food.get('carbs_g', 0) * portion_size / 100,
                'fat': selected_food.get('fat_g', 0) * portion_size / 100
            }
            
            optimized_meals.append(meal)
            total_cost += selected_food.get('cost_per_100g', 1) * portion_size / 100
            
            # Aggregate nutrition
            total_nutrition['calories'] += meal['calories']
            total_nutrition['protein'] += meal['protein']
            total_nutrition['carbs'] += meal['carbs']
            total_nutrition['fat'] += meal['fat']
        
        return {
            'success': True,
            'meals': optimized_meals,
            'total_nutrition': total_nutrition,
            'total_cost': total_cost
        }
    
    def _calculate_nutrition_density(self, food: Dict[str, Any]) -> float:
        """Calculate nutrition density score"""
        calories = max(food.get('calories_per_100g', 1), 1)
        protein = food.get('protein_g', 0)
        fiber = food.get('fiber_g', 0)
        
        # Higher protein and fiber = better nutrition density
        density_score = (protein * 4 + fiber * 2) / calories
        return min(density_score, 2.0)  # Cap at 2.0
    
    def _calculate_meal_type_fit(self, food: Dict[str, Any], meal_type: str) -> float:
        """Calculate how well food fits meal type"""
        category = food.get('category', '').lower()
        name = food.get('name', '').lower()
        
        if meal_type == 'breakfast':
            if any(word in name for word in ['oat', 'egg', 'yogurt', 'milk']):
                return 1.0
            elif category in ['dairy', 'fruit']:
                return 0.8
            else:
                return 0.5
        
        elif meal_type == 'lunch':
            if category in ['protein', 'carbohydrate', 'vegetable']:
                return 1.0
            else:
                return 0.7
        
        elif meal_type == 'dinner':
            if category in ['protein', 'vegetable']:
                return 1.0
            elif category == 'carbohydrate':
                return 0.8
            else:
                return 0.6
        
        return 0.5