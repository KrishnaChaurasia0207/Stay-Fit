"""
User profile and dietary preference models
Handles user data, preferences, and historical information
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from datetime import datetime, date
from enum import Enum
import json


class ActivityLevel(Enum):
    """Activity level enumeration for TDEE calculation"""
    SEDENTARY = 1.2  # Little to no exercise
    LIGHTLY_ACTIVE = 1.375  # Light exercise 1-3 days/week
    MODERATELY_ACTIVE = 1.55  # Moderate exercise 3-5 days/week
    VERY_ACTIVE = 1.725  # Hard exercise 6-7 days/week
    EXTREMELY_ACTIVE = 1.9  # Very hard exercise, physical job


class DietaryRestriction(Enum):
    """Dietary restriction types"""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"
    KETO = "keto"
    PALEO = "paleo"
    LOW_CARB = "low_carb"
    LOW_FAT = "low_fat"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"


@dataclass
class BiometricData:
    """Wearable/biometric data structure"""
    timestamp: datetime
    steps: Optional[int] = None
    heart_rate: Optional[int] = None  # Average heart rate
    sleep_hours: Optional[float] = None
    glucose_mg_dl: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'steps': self.steps,
            'heart_rate': self.heart_rate,
            'sleep_hours': self.sleep_hours,
            'glucose_mg_dl': self.glucose_mg_dl,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'weight_kg': self.weight_kg,
            'body_fat_percentage': self.body_fat_percentage
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BiometricData':
        """Create from dictionary"""
        data_copy = data.copy()
        if 'timestamp' in data_copy:
            data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
        return cls(**data_copy)


@dataclass
class MealHistory:
    """Historical meal data for personalization"""
    date: date
    meal_type: str  # breakfast, lunch, dinner, snack
    foods: List[str]  # List of food names
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    satisfaction_rating: Optional[int] = None  # 1-5 scale
    preparation_time: Optional[int] = None  # minutes
    cost: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            'date': self.date.isoformat(),
            'meal_type': self.meal_type,
            'foods': self.foods,
            'calories': self.calories,
            'protein_g': self.protein_g,
            'carbs_g': self.carbs_g,
            'fat_g': self.fat_g,
            'satisfaction_rating': self.satisfaction_rating,
            'preparation_time': self.preparation_time,
            'cost': self.cost
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MealHistory':
        """Create from dictionary"""
        data_copy = data.copy()
        if 'date' in data_copy:
            data_copy['date'] = date.fromisoformat(data_copy['date'])
        return cls(**data_copy)


@dataclass
class DietaryPreferences:
    """User dietary preferences and restrictions"""
    allergies: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    cuisine_preferences: List[str] = field(default_factory=list)
    dietary_restrictions: List[DietaryRestriction] = field(default_factory=list)
    preferred_meal_times: Dict[str, str] = field(default_factory=dict)  # meal_type: time
    max_preparation_time: Optional[int] = None  # minutes
    spice_tolerance: Optional[str] = "medium"  # low, medium, high
    texture_preferences: List[str] = field(default_factory=list)  # crunchy, smooth, etc.
    organic_preference: bool = False
    local_preference: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            'allergies': self.allergies,
            'dislikes': self.dislikes,
            'cuisine_preferences': self.cuisine_preferences,
            'dietary_restrictions': [dr.value for dr in self.dietary_restrictions],
            'preferred_meal_times': self.preferred_meal_times,
            'max_preparation_time': self.max_preparation_time,
            'spice_tolerance': self.spice_tolerance,
            'texture_preferences': self.texture_preferences,
            'organic_preference': self.organic_preference,
            'local_preference': self.local_preference
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DietaryPreferences':
        """Create from dictionary"""
        data_copy = data.copy()
        if 'dietary_restrictions' in data_copy:
            data_copy['dietary_restrictions'] = [
                DietaryRestriction(dr) for dr in data_copy['dietary_restrictions']
            ]
        return cls(**data_copy)


@dataclass
class UserProfile:
    """Complete user profile with all relevant information"""
    # Basic Information
    name: str
    age: int
    sex: str  # "male", "female", "other"
    weight_kg: float
    height_cm: float
    
    # Lifestyle
    activity_level: ActivityLevel = ActivityLevel.MODERATELY_ACTIVE
    daily_budget: Optional[float] = None  # USD
    timezone: str = "UTC"
    
    # Health Goals
    goal_weight_kg: Optional[float] = None
    target_calories: Optional[int] = None
    target_protein_g: Optional[int] = None
    target_carbs_g: Optional[int] = None
    target_fat_g: Optional[int] = None
    
    # Preferences
    dietary_preferences: DietaryPreferences = field(default_factory=DietaryPreferences)
    
    # Historical Data
    meal_history: List[MealHistory] = field(default_factory=list)
    biometric_data: List[BiometricData] = field(default_factory=list)
    
    # Personalization Data
    preferred_foods: List[str] = field(default_factory=list)
    avoided_foods: List[str] = field(default_factory=list)
    meal_satisfaction_trends: Dict[str, float] = field(default_factory=dict)
    
    def calculate_bmr(self) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        More accurate than Harris-Benedict for modern populations
        """
        if self.sex.lower() == "male":
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:  # female or other
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        
        return bmr
    
    def calculate_tdee(self) -> float:
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr()
        return bmr * self.activity_level.value
    
    def get_latest_biometrics(self) -> Optional[BiometricData]:
        """Get the most recent biometric data"""
        if not self.biometric_data:
            return None
        return max(self.biometric_data, key=lambda x: x.timestamp)
    
    def get_recent_meals(self, days: int = 7) -> List[MealHistory]:
        """Get meals from the last N days"""
        cutoff_date = date.today()
        from datetime import timedelta
        cutoff_date = cutoff_date - timedelta(days=days)
        
        return [meal for meal in self.meal_history if meal.date >= cutoff_date]
    
    def add_meal_history(self, meal: MealHistory):
        """Add a meal to history"""
        self.meal_history.append(meal)
        # Keep only last 90 days of history
        from datetime import timedelta
        cutoff_date = date.today() - timedelta(days=90)
        self.meal_history = [m for m in self.meal_history if m.date >= cutoff_date]
    
    def add_biometric_data(self, data: BiometricData):
        """Add biometric data"""
        self.biometric_data.append(data)
        # Keep only last 30 days of biometric data
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=30)
        self.biometric_data = [b for b in self.biometric_data if b.timestamp >= cutoff_date]
    
    def update_food_preferences(self, food_name: str, liked: bool, strength: float = 1.0):
        """Update food preferences based on user feedback"""
        if liked:
            if food_name not in self.preferred_foods:
                self.preferred_foods.append(food_name)
            if food_name in self.avoided_foods:
                self.avoided_foods.remove(food_name)
        else:
            if food_name not in self.avoided_foods:
                self.avoided_foods.append(food_name)
            if food_name in self.preferred_foods:
                self.preferred_foods.remove(food_name)
    
    def get_macro_targets(self) -> Dict[str, float]:
        """Get macro targets based on TDEE and preferences"""
        if self.target_calories:
            target_calories = self.target_calories
        else:
            target_calories = self.calculate_tdee()
        
        # Use custom targets if set, otherwise use default ratios
        from .config import Config
        ratios = Config.DEFAULT_MACRO_RATIOS
        
        protein_calories = target_calories * ratios['protein']
        carb_calories = target_calories * ratios['carbs']
        fat_calories = target_calories * ratios['fat']
        
        return {
            'calories': target_calories,
            'protein_g': self.target_protein_g or (protein_calories / 4),  # 4 cal/g
            'carbs_g': self.target_carbs_g or (carb_calories / 4),  # 4 cal/g
            'fat_g': self.target_fat_g or (fat_calories / 9)  # 9 cal/g
        }
    
    def is_food_allowed(self, food_data: Dict[str, Any]) -> bool:
        """Check if a food is allowed based on dietary restrictions"""
        food_name = food_data.get('name', '').lower()
        allergens = food_data.get('allergens', [])
        
        # Check allergies
        for allergy in self.dietary_preferences.allergies:
            if allergy.lower() in allergens or allergy.lower() in food_name:
                return False
        
        # Check dislikes
        for dislike in self.dietary_preferences.dislikes:
            if dislike.lower() in food_name:
                return False
        
        # Check dietary restrictions
        for restriction in self.dietary_preferences.dietary_restrictions:
            if not self._check_dietary_restriction(food_data, restriction):
                return False
        
        return True
    
    def _check_dietary_restriction(self, food_data: Dict[str, Any], restriction: DietaryRestriction) -> bool:
        """Check if food meets specific dietary restriction"""
        food_name = food_data.get('name', '').lower()
        category = food_data.get('category', '').lower()
        
        if restriction == DietaryRestriction.VEGETARIAN:
            meat_keywords = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 'meat']
            return not any(keyword in food_name for keyword in meat_keywords)
        
        elif restriction == DietaryRestriction.VEGAN:
            animal_keywords = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 
                             'meat', 'milk', 'cheese', 'yogurt', 'egg', 'butter', 'honey']
            return not any(keyword in food_name for keyword in animal_keywords)
        
        elif restriction == DietaryRestriction.GLUTEN_FREE:
            gluten_keywords = ['wheat', 'bread', 'pasta', 'oat', 'barley', 'rye']
            return not any(keyword in food_name for keyword in gluten_keywords)
        
        elif restriction == DietaryRestriction.DAIRY_FREE:
            dairy_keywords = ['milk', 'cheese', 'yogurt', 'butter', 'cream']
            return not any(keyword in food_name for keyword in dairy_keywords)
        
        elif restriction == DietaryRestriction.KETO:
            # High fat, very low carb
            carbs = food_data.get('carbs_g', 0)
            return carbs < 5  # Less than 5g carbs per 100g
        
        elif restriction == DietaryRestriction.LOW_CARB:
            carbs = food_data.get('carbs_g', 0)
            return carbs < 15  # Less than 15g carbs per 100g
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for serialization"""
        return {
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'weight_kg': self.weight_kg,
            'height_cm': self.height_cm,
            'activity_level': self.activity_level.value,
            'daily_budget': self.daily_budget,
            'timezone': self.timezone,
            'goal_weight_kg': self.goal_weight_kg,
            'target_calories': self.target_calories,
            'target_protein_g': self.target_protein_g,
            'target_carbs_g': self.target_carbs_g,
            'target_fat_g': self.target_fat_g,
            'dietary_preferences': self.dietary_preferences.to_dict(),
            'meal_history': [meal.to_dict() for meal in self.meal_history],
            'biometric_data': [data.to_dict() for data in self.biometric_data],
            'preferred_foods': self.preferred_foods,
            'avoided_foods': self.avoided_foods,
            'meal_satisfaction_trends': self.meal_satisfaction_trends
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create UserProfile from dictionary"""
        data_copy = data.copy()
        
        # Convert activity level
        if 'activity_level' in data_copy:
            activity_value = data_copy['activity_level']
            for level in ActivityLevel:
                if level.value == activity_value:
                    data_copy['activity_level'] = level
                    break
        
        # Convert dietary preferences
        if 'dietary_preferences' in data_copy:
            data_copy['dietary_preferences'] = DietaryPreferences.from_dict(
                data_copy['dietary_preferences']
            )
        
        # Convert meal history
        if 'meal_history' in data_copy:
            data_copy['meal_history'] = [
                MealHistory.from_dict(meal) for meal in data_copy['meal_history']
            ]
        
        # Convert biometric data
        if 'biometric_data' in data_copy:
            data_copy['biometric_data'] = [
                BiometricData.from_dict(bio) for bio in data_copy['biometric_data']
            ]
        
        return cls(**data_copy)
    
    def save_to_file(self, filepath: str):
        """Save profile to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'UserProfile':
        """Load profile from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)