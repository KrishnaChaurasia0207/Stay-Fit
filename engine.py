"""
Main Personalized Nutrition Optimization Engine
Orchestrates all components and provides the main API
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date
import json
from pathlib import Path

from models import UserProfile, BiometricData, MealHistory, DietaryPreferences, ActivityLevel
from meal_planner import MealPlanGenerator
from adaptation import MealAdaptationEngine
from shopping import ShoppingListGenerator
from metabolism import MetabolismCalculator
from config import Config


class PersonalizedNutritionEngine:
    """
    Main engine class that orchestrates all nutrition optimization components
    
    This is the primary interface for generating personalized meal plans
    with ML-based optimization and real-time biometric adaptations.
    """
    
    def __init__(self, config_overrides: Dict[str, Any] = None):
        """
        Initialize the nutrition engine
        
        Args:
            config_overrides: Optional configuration overrides
        """
        self.config = Config()
        if config_overrides:
            for key, value in config_overrides.items():
                setattr(self.config, key, value)
        
        # Initialize core components
        self.meal_planner = MealPlanGenerator()
        self.adaptation_engine = MealAdaptationEngine()
        self.shopping_generator = ShoppingListGenerator()
        self.metabolism_calc = MetabolismCalculator()
        
        # Engine metadata
        self.version = "1.0.0"
        self.last_optimization = None
    
    def generate_meal_plan(self, 
                          user_data: Dict[str, Any],
                          preferences: Dict[str, Any] = None,
                          biometric_data: List[Dict[str, Any]] = None,
                          meal_count: int = 3,
                          days: int = 1) -> Dict[str, Any]:
        """
        Generate a complete personalized meal plan
        
        Args:
            user_data: User profile information (name, age, sex, weight_kg, height_cm, etc.)
            preferences: Additional preferences and constraints
            biometric_data: Recent biometric data for adaptations
            meal_count: Number of meals per day (default: 3)
            days: Number of days to plan for (default: 1)
            
        Returns:
            Complete meal plan with nutrition, shopping list, and adaptations
        """
        try:
            # Create user profile from input data
            profile = self._create_user_profile(user_data)
            
            # Process biometric data
            biometrics = self._process_biometric_data(biometric_data or [])
            
            # Set meal preferences
            meal_preferences = preferences or {}
            meal_types = self._determine_meal_types(meal_count)
            meal_preferences['meal_types'] = meal_types
            
            # Generate base meal plan
            meal_plan_result = self.meal_planner.generate_meal_plan(
                profile, meal_preferences, biometrics
            )
            
            if not meal_plan_result.get('success'):
                return self._format_error_response(meal_plan_result.get('error', 'Unknown error'))
            
            # Apply biometric adaptations
            adapted_meals, adaptation_notes = self.adaptation_engine.adapt_meal_plan(
                meal_plan_result['meals'], profile, biometrics
            )
            
            # Generate shopping list
            shopping_result = self.shopping_generator.generate_shopping_list(
                adapted_meals, profile, days
            )
            
            # Format final response
            response = self._format_success_response(
                adapted_meals,
                meal_plan_result,
                shopping_result,
                adaptation_notes,
                profile,
                biometrics
            )
            
            # Store optimization timestamp
            self.last_optimization = datetime.now()
            
            return response
            
        except Exception as e:
            return self._format_error_response(f"Engine error: {str(e)}")
    
    def update_user_feedback(self, 
                           user_id: str,
                           meal_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user preferences based on meal feedback
        
        Args:
            user_id: User identifier
            meal_feedback: Feedback on meals (satisfaction ratings, preferences)
            
        Returns:
            Updated user profile information
        """
        # This would integrate with a user database in production
        # For now, return a simple acknowledgment
        return {
            'success': True,
            'message': 'Feedback recorded for future meal plan improvements',
            'user_id': user_id,
            'feedback_processed': meal_feedback,
            'timestamp': datetime.now().isoformat()
        }
    
    def simulate_biometric_changes(self, 
                                 current_biometrics: Dict[str, Any],
                                 scenario: str = "high_glucose") -> Dict[str, Any]:
        """
        Simulate biometric changes and show adaptation responses
        
        Args:
            current_biometrics: Current biometric values
            scenario: Simulation scenario ('high_glucose', 'low_activity', 'poor_sleep')
            
        Returns:
            Simulated biometric data and expected adaptations
        """
        simulated_bio = current_biometrics.copy()
        adaptations = []
        
        if scenario == "high_glucose":
            simulated_bio['glucose_mg_dl'] = 155
            adaptations.append("Carbohydrate reduction recommended")
            adaptations.append("Increase protein portions")
            
        elif scenario == "low_activity":
            simulated_bio['steps'] = 3000
            adaptations.append("Reduce overall portion sizes")
            adaptations.append("Focus on lighter meals")
            
        elif scenario == "poor_sleep":
            simulated_bio['sleep_hours'] = 4.5
            adaptations.append("Increase protein for recovery")
            adaptations.append("Reduce refined carbohydrates")
            
        elif scenario == "high_stress":
            simulated_bio['heart_rate'] = 95
            adaptations.append("Stress-reducing meal composition")
            adaptations.append("Reduced caffeine recommendations")
        
        return {
            'scenario': scenario,
            'simulated_biometrics': simulated_bio,
            'expected_adaptations': adaptations,
            'adaptation_strength': 'moderate',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_nutrition_insights(self, 
                             user_data: Dict[str, Any],
                             biometric_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get detailed nutrition and metabolic insights for a user
        
        Args:
            user_data: User profile information
            biometric_data: Recent biometric data
            
        Returns:
            Detailed nutrition and metabolic analysis
        """
        try:
            profile = self._create_user_profile(user_data)
            biometrics = self._process_biometric_data(biometric_data or [])
            
            # Get metabolic insights
            metabolic_insights = self.metabolism_calc.get_metabolic_insights(profile, biometrics)
            
            # Calculate calorie needs
            calorie_needs = self.metabolism_calc.calculate_calorie_needs_by_goal(profile)
            
            # Get macro targets
            macro_targets = profile.get_macro_targets()
            
            # Analyze biometric trends if available
            biometric_analysis = {}
            if biometrics:
                biometric_analysis = self.adaptation_engine.analyzer.analyze_biometric_trends(biometrics)
            
            return {
                'success': True,
                'user_profile': {
                    'bmr': profile.calculate_bmr(),
                    'tdee': profile.calculate_tdee(),
                    'activity_level': profile.activity_level.name,
                    'bmi': profile.weight_kg / ((profile.height_cm / 100) ** 2)
                },
                'calorie_requirements': calorie_needs,
                'macro_targets': macro_targets,
                'metabolic_insights': metabolic_insights,
                'biometric_analysis': biometric_analysis,
                'recommendations': self._generate_nutrition_recommendations(profile, biometrics),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'error': f"Analysis error: {str(e)}"}
    
    def _create_user_profile(self, user_data: Dict[str, Any]) -> UserProfile:
        """Create UserProfile from input data"""
        # Extract basic information
        basic_info = {
            'name': user_data.get('name', 'User'),
            'age': user_data.get('age', 30),
            'sex': user_data.get('sex', 'other'),
            'weight_kg': user_data.get('weight_kg', 70),
            'height_cm': user_data.get('height_cm', 170)
        }
        
        # Activity level
        activity_level_str = user_data.get('activity_level', 'moderately_active')
        activity_level = ActivityLevel.MODERATELY_ACTIVE
        try:
            activity_level = ActivityLevel[activity_level_str.upper()]
        except (KeyError, AttributeError):
            pass
        
        # Dietary preferences
        prefs_data = user_data.get('dietary_preferences', {})
        dietary_prefs = DietaryPreferences(
            allergies=prefs_data.get('allergies', []),
            dislikes=prefs_data.get('dislikes', []),
            cuisine_preferences=prefs_data.get('cuisine_preferences', []),
            dietary_restrictions=[],  # Would parse from string/enum
            max_preparation_time=prefs_data.get('max_preparation_time')
        )
        
        # Create profile
        profile = UserProfile(
            activity_level=activity_level,
            daily_budget=user_data.get('daily_budget'),
            dietary_preferences=dietary_prefs,
            **basic_info
        )
        
        # Add historical data if provided
        meal_history = user_data.get('meal_history', [])
        for meal_data in meal_history:
            meal = MealHistory(
                date=date.fromisoformat(meal_data['date']),
                meal_type=meal_data['meal_type'],
                foods=meal_data['foods'],
                calories=meal_data['calories'],
                protein_g=meal_data['protein_g'],
                carbs_g=meal_data['carbs_g'],
                fat_g=meal_data['fat_g'],
                satisfaction_rating=meal_data.get('satisfaction_rating')
            )
            profile.add_meal_history(meal)
        
        return profile
    
    def _process_biometric_data(self, biometric_data: List[Dict[str, Any]]) -> List[BiometricData]:
        """Process biometric data from input format"""
        biometrics = []
        
        for bio_data in biometric_data:
            timestamp_str = bio_data.get('timestamp')
            if timestamp_str:
                timestamp = datetime.fromisoformat(timestamp_str)
            else:
                timestamp = datetime.now()
            
            bio = BiometricData(
                timestamp=timestamp,
                steps=bio_data.get('steps'),
                heart_rate=bio_data.get('heart_rate'),
                sleep_hours=bio_data.get('sleep_hours'),
                glucose_mg_dl=bio_data.get('glucose_mg_dl'),
                weight_kg=bio_data.get('weight_kg'),
                body_fat_percentage=bio_data.get('body_fat_percentage')
            )
            biometrics.append(bio)
        
        return biometrics
    
    def _determine_meal_types(self, meal_count: int) -> List[str]:
        """Determine meal types based on count"""
        if meal_count == 1:
            return ['lunch']
        elif meal_count == 2:
            return ['breakfast', 'dinner']
        elif meal_count == 3:
            return ['breakfast', 'lunch', 'dinner']
        elif meal_count == 4:
            return ['breakfast', 'morning_snack', 'lunch', 'dinner']
        elif meal_count == 5:
            return ['breakfast', 'morning_snack', 'lunch', 'afternoon_snack', 'dinner']
        else:
            return ['breakfast', 'lunch', 'dinner']
    
    def _format_success_response(self, 
                                meals: List[Dict[str, Any]],
                                meal_plan_result: Dict[str, Any],
                                shopping_result: Dict[str, Any],
                                adaptation_notes: List[str],
                                profile: UserProfile,
                                biometrics: List[BiometricData]) -> Dict[str, Any]:
        """Format successful response in required JSON structure"""
        
        # Calculate totals
        total_calories = sum(meal.get('calories', 0) for meal in meals)
        total_protein = sum(meal.get('protein', 0) for meal in meals)
        total_carbs = sum(meal.get('carbs', 0) for meal in meals)
        total_fat = sum(meal.get('fat', 0) for meal in meals)
        
        # Format meals for output
        formatted_meals = []
        for meal in meals:
            formatted_meals.append({
                'meal_type': meal.get('meal_type', 'meal'),
                'items': meal.get('items', []),
                'calories': round(meal.get('calories', 0), 1),
                'protein': round(meal.get('protein', 0), 1),
                'carbs': round(meal.get('carbs', 0), 1),
                'fat': round(meal.get('fat', 0), 1)
            })
        
        # Format shopping list
        shopping_list = []
        for category, items in shopping_result.get('shopping_list', {}).items():
            for item in items:
                shopping_list.append({
                    'item': item['item'],
                    'quantity': item['quantity'],
                    'unit': item['unit']
                })
        
        # Combine adaptation information
        adaptations_text = "; ".join(adaptation_notes) if adaptation_notes else ""
        if meal_plan_result.get('adaptations'):
            if adaptations_text:
                adaptations_text += "; " + meal_plan_result['adaptations']
            else:
                adaptations_text = meal_plan_result['adaptations']
        
        return {
            'success': True,
            'meals': formatted_meals,
            'total_calories': round(total_calories, 1),
            'total_macros': {
                'protein': round(total_protein, 1),
                'carbs': round(total_carbs, 1),
                'fat': round(total_fat, 1)
            },
            'shopping_list': shopping_list,
            'total_cost': shopping_result.get('estimated_cost', 0),
            'adaptations': adaptations_text,
            'personalization_notes': meal_plan_result.get('personalization_notes', ''),
            'metabolic_insights': meal_plan_result.get('metabolic_insights', {}),
            'engine_version': self.version,
            'generated_at': datetime.now().isoformat()
        }
    
    def _format_error_response(self, error_message: str) -> Dict[str, Any]:
        """Format error response"""
        return {
            'success': False,
            'error': error_message,
            'meals': [],
            'total_calories': 0,
            'total_macros': {'protein': 0, 'carbs': 0, 'fat': 0},
            'shopping_list': [],
            'adaptations': '',
            'personalization_notes': '',
            'engine_version': self.version,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_nutrition_recommendations(self, 
                                          profile: UserProfile,
                                          biometrics: List[BiometricData]) -> List[str]:
        """Generate personalized nutrition recommendations"""
        recommendations = []
        
        # BMI-based recommendations
        bmi = profile.weight_kg / ((profile.height_cm / 100) ** 2)
        if bmi < 18.5:
            recommendations.append("Consider increasing caloric intake for healthy weight gain")
        elif bmi > 25:
            recommendations.append("Focus on nutrient-dense, lower-calorie foods for weight management")
        
        # Activity-based recommendations
        if profile.activity_level.value > 1.6:
            recommendations.append("Increase protein intake to support high activity levels")
            recommendations.append("Ensure adequate carbohydrate intake for energy")
        
        # Age-based recommendations
        if profile.age > 50:
            recommendations.append("Prioritize calcium and vitamin D rich foods")
            recommendations.append("Focus on high-quality protein sources")
        
        # Biometric-based recommendations
        if biometrics:
            latest_bio = max(biometrics, key=lambda x: x.timestamp)
            
            if latest_bio.glucose_mg_dl and latest_bio.glucose_mg_dl > 100:
                recommendations.append("Monitor carbohydrate intake and timing")
            
            if latest_bio.steps and latest_bio.steps < 5000:
                recommendations.append("Consider smaller, more frequent meals")
            
            if latest_bio.sleep_hours and latest_bio.sleep_hours < 7:
                recommendations.append("Focus on foods that support sleep quality")
        
        return recommendations