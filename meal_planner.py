"""
Main meal plan generation engine with constraint handling
Orchestrates optimization, nutrition database, and user preferences
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date, timedelta

from models import UserProfile, BiometricData, MealHistory
from api_client import NutritionAPIClient
from metabolism import MetabolismCalculator
from ml_models import MealOptimizer, MealSatisfactionPredictor
from config import Config


class NutritionDatabase:
    """Local nutrition database with API fallback"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.LOCAL_DB_PATH
        self.api_client = NutritionAPIClient()
        self.local_foods = self._load_local_database()
    
    def _load_local_database(self) -> List[Dict[str, Any]]:
        """Load local nutrition database"""
        try:
            db_path = Path(self.db_path)
            if db_path.exists():
                with open(db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('foods', [])
        except Exception as e:
            print(f"Error loading local database: {e}")
        return []
    
    def search_foods(self, query: str = "", category: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """Search for foods in local database first, then APIs if needed"""
        results = []
        
        # Search local database
        for food in self.local_foods:
            if self._matches_criteria(food, query, category):
                results.append(food)
        
        # If we have enough results, return them
        if len(results) >= limit or not query:
            return results[:limit]
        
        # Otherwise, search APIs for additional results
        try:
            api_results = self.api_client.search_food(query, limit - len(results))
            results.extend(api_results)
        except Exception as e:
            print(f"API search failed: {e}")
        
        return results[:limit]
    
    def get_food_by_id(self, food_id: str) -> Optional[Dict[str, Any]]:
        """Get specific food by ID"""
        # Check local database first
        for food in self.local_foods:
            if str(food.get('id')) == str(food_id):
                return food
        
        # Try API
        try:
            return self.api_client.get_food_nutrition(food_id)
        except Exception as e:
            print(f"Error getting food {food_id}: {e}")
            return None
    
    def _matches_criteria(self, food: Dict[str, Any], query: str, category: str) -> bool:
        """Check if food matches search criteria"""
        if category and food.get('category', '').lower() != category.lower():
            return False
        
        if query:
            query_lower = query.lower()
            name_match = query_lower in food.get('name', '').lower()
            category_match = query_lower in food.get('category', '').lower()
            if not (name_match or category_match):
                return False
        
        return True


class MealPlanGenerator:
    """Main meal plan generation engine"""
    
    def __init__(self):
        self.nutrition_db = NutritionDatabase()
        self.metabolism_calc = MetabolismCalculator()
        self.meal_optimizer = MealOptimizer()
        self.satisfaction_predictor = MealSatisfactionPredictor()
    
    def generate_meal_plan(self, profile: UserProfile, 
                          preferences: Dict[str, Any] = None,
                          biometric_data: List[BiometricData] = None) -> Dict[str, Any]:
        """
        Generate personalized meal plan
        
        Args:
            profile: User profile with preferences and history
            preferences: Additional preferences (meal count, specific goals)
            biometric_data: Recent biometric data for adaptations
            
        Returns:
            Complete meal plan with nutrition, cost, and adaptation info
        """
        preferences = preferences or {}
        biometric_data = biometric_data or []
        
        try:
            # Calculate nutritional requirements
            calorie_needs = self._calculate_calorie_requirements(profile, biometric_data)
            
            # Get available foods
            available_foods = self._get_available_foods(profile, preferences)
            
            if not available_foods:
                return {
                    'success': False,
                    'error': 'No suitable foods found for user preferences',
                    'meals': [],
                    'total_calories': 0,
                    'total_macros': {'protein': 0, 'carbs': 0, 'fat': 0},
                    'shopping_list': [],
                    'adaptations': '',
                    'personalization_notes': ''
                }
            
            # Train satisfaction predictor if we have historical data
            if profile.meal_history:
                self._train_satisfaction_predictor(profile)
            
            # Generate optimized meal plan
            meal_plan = self.meal_optimizer.optimize_meal_plan(
                profile, available_foods, calorie_needs,
                preferences.get('meal_types', ['breakfast', 'lunch', 'dinner'])
            )
            
            if not meal_plan.get('success'):
                return {
                    'success': False,
                    'error': meal_plan.get('error', 'Meal optimization failed'),
                    'meals': [],
                    'total_calories': 0,
                    'total_macros': {'protein': 0, 'carbs': 0, 'fat': 0},
                    'shopping_list': [],
                    'adaptations': '',
                    'personalization_notes': ''
                }
            
            # Apply biometric adaptations
            adapted_meals, adaptations = self._apply_biometric_adaptations(
                meal_plan['meals'], profile, biometric_data
            )
            
            # Generate shopping list
            shopping_list = self._generate_shopping_list(adapted_meals)
            
            # Calculate final nutrition totals
            total_nutrition = self._calculate_total_nutrition(adapted_meals)
            
            # Generate personalization notes
            personalization_notes = self._generate_personalization_notes(profile, adapted_meals)
            
            return {
                'success': True,
                'meals': adapted_meals,
                'total_calories': total_nutrition['calories'],
                'total_macros': {
                    'protein': total_nutrition['protein'],
                    'carbs': total_nutrition['carbs'],
                    'fat': total_nutrition['fat']
                },
                'shopping_list': shopping_list,
                'total_cost': meal_plan.get('total_cost', 0),
                'adaptations': adaptations,
                'personalization_notes': personalization_notes,
                'metabolic_insights': self.metabolism_calc.get_metabolic_insights(profile, biometric_data)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Meal plan generation failed: {str(e)}',
                'meals': [],
                'total_calories': 0,
                'total_macros': {'protein': 0, 'carbs': 0, 'fat': 0},
                'shopping_list': [],
                'adaptations': '',
                'personalization_notes': ''
            }
    
    def _calculate_calorie_requirements(self, profile: UserProfile, 
                                      biometric_data: List[BiometricData]) -> Dict[str, float]:
        """Calculate calorie and macro requirements"""
        # Get adaptive TDEE
        tdee_data = self.metabolism_calc.calculate_tdee(profile, biometric_data, adaptive=True)
        
        # Get macro targets
        macro_targets = profile.get_macro_targets()
        
        # Apply any goal-based adjustments
        calorie_needs = self.metabolism_calc.calculate_calorie_needs_by_goal(profile, "maintain")
        
        return {
            'calories': calorie_needs['maintenance'],
            'protein': macro_targets['protein_g'],
            'carbs': macro_targets['carbs_g'],
            'fat': macro_targets['fat_g'],
            'tdee_data': tdee_data
        }
    
    def _get_available_foods(self, profile: UserProfile, 
                           preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get foods that match user preferences and constraints"""
        # Start with all local foods
        all_foods = self.nutrition_db.local_foods.copy()
        
        # Add any specific food searches from preferences
        search_terms = preferences.get('food_searches', [])
        for term in search_terms:
            additional_foods = self.nutrition_db.search_foods(term, limit=10)
            all_foods.extend(additional_foods)
        
        # Filter based on user constraints
        allowed_foods = []
        for food in all_foods:
            if profile.is_food_allowed(food):
                # Add preference scoring
                food_copy = food.copy()
                food_copy['preference_score'] = self._calculate_preference_score(food, profile)
                allowed_foods.append(food_copy)
        
        # Sort by preference score
        allowed_foods.sort(key=lambda x: x.get('preference_score', 0), reverse=True)
        
        return allowed_foods
    
    def _calculate_preference_score(self, food: Dict[str, Any], profile: UserProfile) -> float:
        """Calculate preference score for a food item"""
        score = 1.0
        food_name = food.get('name', '').lower()
        
        # Preferred foods bonus
        for preferred in profile.preferred_foods:
            if preferred.lower() in food_name:
                score += 0.5
        
        # Avoided foods penalty
        for avoided in profile.avoided_foods:
            if avoided.lower() in food_name:
                score -= 0.3
        
        # Cuisine preference bonus
        cuisine_type = food.get('cuisine_type', '')
        if cuisine_type in profile.dietary_preferences.cuisine_preferences:
            score += 0.2
        
        # Budget consideration
        cost = food.get('cost_per_100g', 1.0)
        daily_budget = profile.daily_budget or Config.DEFAULT_DAILY_BUDGET
        if cost <= daily_budget / 10:  # Reasonable cost per 100g
            score += 0.1
        
        return max(0, score)
    
    def _train_satisfaction_predictor(self, profile: UserProfile):
        """Train satisfaction predictor with user's meal history"""
        # For now, train on single user's data
        # In production, would use aggregated anonymous data
        profiles = [profile]
        meal_histories = [profile.meal_history]
        
        self.satisfaction_predictor.train(profiles, meal_histories)
        self.meal_optimizer.satisfaction_predictor = self.satisfaction_predictor
    
    def _apply_biometric_adaptations(self, meals: List[Dict[str, Any]], 
                                   profile: UserProfile, 
                                   biometric_data: List[BiometricData]) -> Tuple[List[Dict[str, Any]], str]:
        """Apply real-time adaptations based on biometric data"""
        if not biometric_data:
            return meals, ""
        
        adapted_meals = meals.copy()
        adaptations = []
        
        # Get latest biometric data
        latest_bio = max(biometric_data, key=lambda x: x.timestamp)
        
        # High glucose adaptation
        if latest_bio.glucose_mg_dl and latest_bio.glucose_mg_dl > Config.HIGH_GLUCOSE_THRESHOLD:
            adaptations.append("Reduced carbohydrate portions due to elevated glucose")
            # Reduce carbs in each meal by 20%
            for meal in adapted_meals:
                if 'carbs' in meal:
                    meal['carbs'] *= 0.8
                    meal['calories'] = meal.get('protein', 0) * 4 + meal['carbs'] * 4 + meal.get('fat', 0) * 9
        
        # Low activity adaptation
        if latest_bio.steps and latest_bio.steps < Config.LOW_ACTIVITY_THRESHOLD:
            adaptations.append("Reduced portion sizes due to low activity level")
            # Reduce all portions by 15%
            for meal in adapted_meals:
                for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                    if nutrient in meal:
                        meal[nutrient] *= 0.85
        
        # Poor sleep adaptation
        if latest_bio.sleep_hours and latest_bio.sleep_hours < Config.POOR_SLEEP_THRESHOLD:
            adaptations.append("Increased protein portions to support recovery from poor sleep")
            # Increase protein by 10%
            for meal in adapted_meals:
                if 'protein' in meal:
                    meal['protein'] *= 1.1
                    meal['calories'] = meal.get('protein', 0) * 4 + meal.get('carbs', 0) * 4 + meal.get('fat', 0) * 9
        
        adaptation_text = "; ".join(adaptations) if adaptations else ""
        return adapted_meals, adaptation_text
    
    def _generate_shopping_list(self, meals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate shopping list from meal plan"""
        ingredient_totals = {}
        
        for meal in meals:
            items = meal.get('items', [])
            portions = meal.get('portions', [100] * len(items))  # Default 100g portions
            
            for i, item in enumerate(items):
                portion = portions[i] if i < len(portions) else 100
                
                if item in ingredient_totals:
                    ingredient_totals[item] += portion
                else:
                    ingredient_totals[item] = portion
        
        shopping_list = []
        for item, quantity in ingredient_totals.items():
            shopping_list.append({
                'item': item,
                'quantity': round(quantity, 1),
                'unit': 'g'
            })
        
        return shopping_list
    
    def _calculate_total_nutrition(self, meals: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate total nutrition from all meals"""
        totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        for meal in meals:
            for nutrient in totals:
                totals[nutrient] += meal.get(nutrient, 0)
        
        return totals
    
    def _generate_personalization_notes(self, profile: UserProfile, 
                                      meals: List[Dict[str, Any]]) -> str:
        """Generate personalization notes based on user history and preferences"""
        notes = []
        
        # Check meal history trends
        recent_meals = profile.get_recent_meals(14)
        if recent_meals:
            avg_protein = sum(m.protein_g for m in recent_meals) / len(recent_meals)
            current_protein = sum(m.get('protein', 0) for m in meals)
            
            if current_protein > avg_protein * 1.2:
                notes.append("Increased protein based on recent low intake pattern")
            elif current_protein < avg_protein * 0.8:
                notes.append("Reduced protein to match recent preference trends")
        
        # Budget considerations
        if profile.daily_budget:
            notes.append(f"Meal plan optimized for daily budget of ${profile.daily_budget:.2f}")
        
        # Dietary restrictions
        if profile.dietary_preferences.dietary_restrictions:
            restriction_names = [dr.value for dr in profile.dietary_preferences.dietary_restrictions]
            notes.append(f"Customized for {', '.join(restriction_names)} dietary requirements")
        
        # Activity level adjustments
        if profile.activity_level.value > 1.6:
            notes.append("Higher calorie and protein targets for active lifestyle")
        
        return "; ".join(notes) if notes else "Standard personalized meal plan"