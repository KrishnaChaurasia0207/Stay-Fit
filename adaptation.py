"""
Real-time adaptation system for biometric data
Monitors user biometrics and adapts meal plans dynamically
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import numpy as np

from models import UserProfile, BiometricData, MealHistory
from config import Config


class AdaptationReason(Enum):
    """Types of adaptation reasons"""
    HIGH_GLUCOSE = "high_glucose"
    LOW_ACTIVITY = "low_activity"
    POOR_SLEEP = "poor_sleep"
    HIGH_STRESS = "high_stress"
    WEIGHT_CHANGE = "weight_change"
    ILLNESS_RECOVERY = "illness_recovery"
    EXERCISE_SESSION = "exercise_session"
    MEAL_TIMING = "meal_timing"


class BiometricAnalyzer:
    """Analyzes biometric data for adaptation triggers"""
    
    def __init__(self):
        self.adaptation_thresholds = {
            'glucose_high': Config.HIGH_GLUCOSE_THRESHOLD,
            'glucose_low': 70,
            'steps_low': Config.LOW_ACTIVITY_THRESHOLD,
            'steps_high': 15000,
            'sleep_poor': Config.POOR_SLEEP_THRESHOLD,
            'sleep_excessive': 10,
            'heart_rate_high': 100,
            'heart_rate_low': 50,
            'weight_change_significant': 2.0  # kg change
        }
    
    def analyze_biometric_trends(self, biometric_data: List[BiometricData], 
                               days_back: int = 7) -> Dict[str, Any]:
        """Analyze biometric trends over specified period"""
        if not biometric_data:
            return {'trends': {}, 'alerts': [], 'adaptations_needed': []}
        
        # Sort by timestamp
        sorted_data = sorted(biometric_data, key=lambda x: x.timestamp)
        
        # Filter to last N days
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_data = [d for d in sorted_data if d.timestamp >= cutoff_date]
        
        if not recent_data:
            return {'trends': {}, 'alerts': [], 'adaptations_needed': []}
        
        trends = {}
        alerts = []
        adaptations_needed = []
        
        # Glucose analysis
        glucose_trends = self._analyze_glucose_trends(recent_data)
        trends['glucose'] = glucose_trends
        if glucose_trends['alerts']:
            alerts.extend(glucose_trends['alerts'])
            adaptations_needed.extend(glucose_trends['adaptations'])
        
        # Activity analysis
        activity_trends = self._analyze_activity_trends(recent_data)
        trends['activity'] = activity_trends
        if activity_trends['alerts']:
            alerts.extend(activity_trends['alerts'])
            adaptations_needed.extend(activity_trends['adaptations'])
        
        # Sleep analysis
        sleep_trends = self._analyze_sleep_trends(recent_data)
        trends['sleep'] = sleep_trends
        if sleep_trends['alerts']:
            alerts.extend(sleep_trends['alerts'])
            adaptations_needed.extend(sleep_trends['adaptations'])
        
        # Heart rate analysis
        hr_trends = self._analyze_heart_rate_trends(recent_data)
        trends['heart_rate'] = hr_trends
        if hr_trends['alerts']:
            alerts.extend(hr_trends['alerts'])
            adaptations_needed.extend(hr_trends['adaptations'])
        
        # Weight change analysis
        weight_trends = self._analyze_weight_trends(recent_data)
        trends['weight'] = weight_trends
        if weight_trends['alerts']:
            alerts.extend(weight_trends['alerts'])
            adaptations_needed.extend(weight_trends['adaptations'])
        
        return {
            'trends': trends,
            'alerts': alerts,
            'adaptations_needed': adaptations_needed,
            'analysis_period': f"{days_back} days",
            'data_points': len(recent_data)
        }
    
    def _analyze_glucose_trends(self, data: List[BiometricData]) -> Dict[str, Any]:
        """Analyze glucose level trends"""
        glucose_values = [d.glucose_mg_dl for d in data if d.glucose_mg_dl is not None]
        
        if not glucose_values:
            return {'status': 'no_data', 'alerts': [], 'adaptations': []}
        
        avg_glucose = np.mean(glucose_values)
        max_glucose = np.max(glucose_values)
        trend_direction = self._calculate_trend_direction(glucose_values)
        
        alerts = []
        adaptations = []
        
        if max_glucose > self.adaptation_thresholds['glucose_high']:
            alerts.append(f"High glucose reading detected: {max_glucose:.1f} mg/dL")
            adaptations.append(AdaptationReason.HIGH_GLUCOSE)
        
        if avg_glucose < self.adaptation_thresholds['glucose_low']:
            alerts.append(f"Low average glucose: {avg_glucose:.1f} mg/dL")
        
        return {
            'average': avg_glucose,
            'maximum': max_glucose,
            'trend': trend_direction,
            'status': self._glucose_status_classification(avg_glucose),
            'alerts': alerts,
            'adaptations': adaptations
        }
    
    def _analyze_activity_trends(self, data: List[BiometricData]) -> Dict[str, Any]:
        """Analyze activity level trends"""
        step_values = [d.steps for d in data if d.steps is not None]
        
        if not step_values:
            return {'status': 'no_data', 'alerts': [], 'adaptations': []}
        
        avg_steps = np.mean(step_values)
        min_steps = np.min(step_values)
        consistency = 1 - (np.std(step_values) / max(avg_steps, 1))
        
        alerts = []
        adaptations = []
        
        if avg_steps < self.adaptation_thresholds['steps_low']:
            alerts.append(f"Low activity detected: {avg_steps:.0f} avg steps/day")
            adaptations.append(AdaptationReason.LOW_ACTIVITY)
        
        if consistency < 0.5:
            alerts.append("Inconsistent activity patterns detected")
        
        return {
            'average_steps': avg_steps,
            'minimum_steps': min_steps,
            'consistency_score': consistency,
            'status': self._activity_status_classification(avg_steps),
            'alerts': alerts,
            'adaptations': adaptations
        }
    
    def _analyze_sleep_trends(self, data: List[BiometricData]) -> Dict[str, Any]:
        """Analyze sleep pattern trends"""
        sleep_values = [d.sleep_hours for d in data if d.sleep_hours is not None]
        
        if not sleep_values:
            return {'status': 'no_data', 'alerts': [], 'adaptations': []}
        
        avg_sleep = np.mean(sleep_values)
        min_sleep = np.min(sleep_values)
        sleep_debt = max(0, 7.5 - avg_sleep) * len(sleep_values)
        
        alerts = []
        adaptations = []
        
        if avg_sleep < self.adaptation_thresholds['sleep_poor']:
            alerts.append(f"Insufficient sleep: {avg_sleep:.1f} avg hours/night")
            adaptations.append(AdaptationReason.POOR_SLEEP)
        
        if sleep_debt > 5:  # More than 5 hours of cumulative sleep debt
            alerts.append(f"Significant sleep debt: {sleep_debt:.1f} hours")
        
        return {
            'average_hours': avg_sleep,
            'minimum_hours': min_sleep,
            'sleep_debt': sleep_debt,
            'status': self._sleep_status_classification(avg_sleep),
            'alerts': alerts,
            'adaptations': adaptations
        }
    
    def _analyze_heart_rate_trends(self, data: List[BiometricData]) -> Dict[str, Any]:
        """Analyze heart rate trends for stress indicators"""
        hr_values = [d.heart_rate for d in data if d.heart_rate is not None]
        
        if not hr_values:
            return {'status': 'no_data', 'alerts': [], 'adaptations': []}
        
        avg_hr = np.mean(hr_values)
        hr_variability = np.std(hr_values)
        trend = self._calculate_trend_direction(hr_values)
        
        alerts = []
        adaptations = []
        
        if avg_hr > self.adaptation_thresholds['heart_rate_high']:
            alerts.append(f"Elevated heart rate: {avg_hr:.1f} avg bpm")
            adaptations.append(AdaptationReason.HIGH_STRESS)
        
        if hr_variability > 20:
            alerts.append("High heart rate variability detected (possible stress)")
            adaptations.append(AdaptationReason.HIGH_STRESS)
        
        return {
            'average_bpm': avg_hr,
            'variability': hr_variability,
            'trend': trend,
            'status': self._heart_rate_status_classification(avg_hr),
            'alerts': alerts,
            'adaptations': adaptations
        }
    
    def _analyze_weight_trends(self, data: List[BiometricData]) -> Dict[str, Any]:
        """Analyze weight change trends"""
        weight_values = [d.weight_kg for d in data if d.weight_kg is not None]
        
        if len(weight_values) < 2:
            return {'status': 'insufficient_data', 'alerts': [], 'adaptations': []}
        
        weight_change = weight_values[-1] - weight_values[0]
        trend = self._calculate_trend_direction(weight_values)
        
        alerts = []
        adaptations = []
        
        if abs(weight_change) > self.adaptation_thresholds['weight_change_significant']:
            direction = "gained" if weight_change > 0 else "lost"
            alerts.append(f"Significant weight change: {direction} {abs(weight_change):.1f} kg")
            adaptations.append(AdaptationReason.WEIGHT_CHANGE)
        
        return {
            'total_change_kg': weight_change,
            'trend': trend,
            'rate_per_day': weight_change / max(len(weight_values), 1),
            'alerts': alerts,
            'adaptations': adaptations
        }
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction (increasing, decreasing, stable)"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _glucose_status_classification(self, avg_glucose: float) -> str:
        """Classify glucose status"""
        if avg_glucose < 70:
            return 'low'
        elif 70 <= avg_glucose <= 100:
            return 'normal'
        elif 100 < avg_glucose <= 125:
            return 'elevated'
        else:
            return 'high'
    
    def _activity_status_classification(self, avg_steps: float) -> str:
        """Classify activity status"""
        if avg_steps < 3000:
            return 'sedentary'
        elif 3000 <= avg_steps <= 7000:
            return 'low'
        elif 7000 < avg_steps <= 12000:
            return 'moderate'
        else:
            return 'high'
    
    def _sleep_status_classification(self, avg_sleep: float) -> str:
        """Classify sleep status"""
        if avg_sleep < 6:
            return 'insufficient'
        elif 6 <= avg_sleep <= 7:
            return 'borderline'
        elif 7 < avg_sleep <= 9:
            return 'adequate'
        else:
            return 'excessive'
    
    def _heart_rate_status_classification(self, avg_hr: float) -> str:
        """Classify heart rate status"""
        if avg_hr < 60:
            return 'low'
        elif 60 <= avg_hr <= 80:
            return 'normal'
        elif 80 < avg_hr <= 100:
            return 'elevated'
        else:
            return 'high'


class MealAdaptationEngine:
    """Adapts meal plans based on biometric analysis"""
    
    def __init__(self):
        self.analyzer = BiometricAnalyzer()
        self.adaptation_strategies = {
            AdaptationReason.HIGH_GLUCOSE: self._adapt_for_high_glucose,
            AdaptationReason.LOW_ACTIVITY: self._adapt_for_low_activity,
            AdaptationReason.POOR_SLEEP: self._adapt_for_poor_sleep,
            AdaptationReason.HIGH_STRESS: self._adapt_for_high_stress,
            AdaptationReason.WEIGHT_CHANGE: self._adapt_for_weight_change,
        }
    
    def adapt_meal_plan(self, meals: List[Dict[str, Any]], 
                       profile: UserProfile,
                       biometric_data: List[BiometricData]) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Adapt meal plan based on biometric analysis
        
        Returns:
            Tuple of (adapted_meals, adaptation_explanations)
        """
        # Analyze biometric data
        analysis = self.analyzer.analyze_biometric_trends(biometric_data)
        
        if not analysis['adaptations_needed']:
            return meals, []
        
        adapted_meals = [meal.copy() for meal in meals]
        adaptations_made = []
        
        # Apply adaptations in order of priority
        for adaptation_reason in analysis['adaptations_needed']:
            if adaptation_reason in self.adaptation_strategies:
                strategy = self.adaptation_strategies[adaptation_reason]
                adapted_meals, explanation = strategy(adapted_meals, analysis, profile)
                if explanation:
                    adaptations_made.append(explanation)
        
        return adapted_meals, adaptations_made
    
    def _adapt_for_high_glucose(self, meals: List[Dict[str, Any]], 
                              analysis: Dict[str, Any],
                              profile: UserProfile) -> Tuple[List[Dict[str, Any]], str]:
        """Adapt meals for high glucose levels"""
        glucose_info = analysis['trends']['glucose']
        reduction_factor = 0.7 if glucose_info['maximum'] > 160 else 0.8
        
        for meal in meals:
            if 'carbs' in meal:
                original_carbs = meal['carbs']
                meal['carbs'] *= reduction_factor
                # Compensate with slight protein increase
                if 'protein' in meal:
                    meal['protein'] *= 1.1
                # Recalculate calories
                meal['calories'] = (meal.get('protein', 0) * 4 + 
                                  meal['carbs'] * 4 + 
                                  meal.get('fat', 0) * 9)
        
        max_glucose = glucose_info['maximum']
        return meals, f"Reduced carbohydrate intake by {int((1-reduction_factor)*100)}% due to glucose reading of {max_glucose:.1f} mg/dL"
    
    def _adapt_for_low_activity(self, meals: List[Dict[str, Any]], 
                              analysis: Dict[str, Any],
                              profile: UserProfile) -> Tuple[List[Dict[str, Any]], str]:
        """Adapt meals for low activity levels"""
        activity_info = analysis['trends']['activity']
        reduction_factor = 0.85
        
        for meal in meals:
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                if nutrient in meal:
                    meal[nutrient] *= reduction_factor
        
        avg_steps = activity_info['average_steps']
        return meals, f"Reduced portion sizes by 15% due to low activity level ({avg_steps:.0f} avg steps/day)"
    
    def _adapt_for_poor_sleep(self, meals: List[Dict[str, Any]], 
                            analysis: Dict[str, Any],
                            profile: UserProfile) -> Tuple[List[Dict[str, Any]], str]:
        """Adapt meals for poor sleep recovery"""
        sleep_info = analysis['trends']['sleep']
        
        for meal in meals:
            if 'protein' in meal:
                meal['protein'] *= 1.15  # Increase protein for recovery
            # Slightly reduce refined carbs
            if 'carbs' in meal:
                meal['carbs'] *= 0.95
            # Recalculate calories
            meal['calories'] = (meal.get('protein', 0) * 4 + 
                              meal.get('carbs', 0) * 4 + 
                              meal.get('fat', 0) * 9)
        
        avg_sleep = sleep_info['average_hours']
        return meals, f"Increased protein by 15% to support recovery from insufficient sleep ({avg_sleep:.1f} avg hrs/night)"
    
    def _adapt_for_high_stress(self, meals: List[Dict[str, Any]], 
                             analysis: Dict[str, Any],
                             profile: UserProfile) -> Tuple[List[Dict[str, Any]], str]:
        """Adapt meals for high stress levels"""
        hr_info = analysis['trends']['heart_rate']
        
        # Increase magnesium-rich foods (represented by increasing vegetable portions)
        # Reduce caffeine-containing items (simplified approach)
        for meal in meals:
            # Slight reduction in overall calories to avoid stress eating
            for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                if nutrient in meal:
                    meal[nutrient] *= 0.95
        
        avg_hr = hr_info['average_bpm']
        return meals, f"Adjusted meal composition for stress management (elevated heart rate: {avg_hr:.1f} bpm)"
    
    def _adapt_for_weight_change(self, meals: List[Dict[str, Any]], 
                               analysis: Dict[str, Any],
                               profile: UserProfile) -> Tuple[List[Dict[str, Any]], str]:
        """Adapt meals for significant weight changes"""
        weight_info = analysis['trends']['weight']
        weight_change = weight_info['total_change_kg']
        
        if weight_change > 1:  # Weight gain
            # Slight calorie reduction
            reduction_factor = 0.9
            for meal in meals:
                for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                    if nutrient in meal:
                        meal[nutrient] *= reduction_factor
            
            return meals, f"Reduced portions by 10% due to weight gain of {weight_change:.1f} kg"
        
        elif weight_change < -1:  # Weight loss
            # Slight calorie increase, especially protein
            for meal in meals:
                meal['protein'] *= 1.1
                meal['calories'] *= 1.05
                # Recalculate other nutrients proportionally
                meal['carbs'] *= 1.02
                meal['fat'] *= 1.02
            
            return meals, f"Increased portions by 5% due to weight loss of {abs(weight_change):.1f} kg"
        
        return meals, ""