"""
Metabolism calculation engine for BMR, TDEE, and adaptive calorie requirements
Includes multiple formulas and biometric-based adjustments
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import numpy as np
from enum import Enum

from models import UserProfile, BiometricData, ActivityLevel


class BMRFormula(Enum):
    """Available BMR calculation formulas"""
    MIFFLIN_ST_JEOR = "mifflin_st_jeor"  # Most accurate for modern populations
    HARRIS_BENEDICT = "harris_benedict"  # Traditional formula
    KATCH_MCARDLE = "katch_mcardle"  # Uses body fat percentage
    CUNNINGHAM = "cunningham"  # For athletes with low body fat


class MetabolismCalculator:
    """Advanced metabolism calculation with biometric adaptations"""
    
    def __init__(self):
        self.adaptive_factors = {
            'sleep_quality': 1.0,
            'stress_level': 1.0,
            'glucose_regulation': 1.0,
            'activity_consistency': 1.0,
            'recovery_status': 1.0
        }
    
    def calculate_bmr(self, profile: UserProfile, formula: BMRFormula = BMRFormula.MIFFLIN_ST_JEOR, 
                     body_fat_percentage: Optional[float] = None) -> float:
        """
        Calculate Basal Metabolic Rate using specified formula
        
        Args:
            profile: User profile with basic metrics
            formula: BMR calculation formula to use
            body_fat_percentage: Required for Katch-McArdle and Cunningham formulas
            
        Returns:
            BMR in calories per day
        """
        if formula == BMRFormula.MIFFLIN_ST_JEOR:
            return self._mifflin_st_jeor(profile)
        elif formula == BMRFormula.HARRIS_BENEDICT:
            return self._harris_benedict(profile)
        elif formula == BMRFormula.KATCH_MCARDLE:
            if body_fat_percentage is None:
                # Fall back to Mifflin-St Jeor if no body fat data
                return self._mifflin_st_jeor(profile)
            return self._katch_mcardle(profile, body_fat_percentage)
        elif formula == BMRFormula.CUNNINGHAM:
            if body_fat_percentage is None:
                return self._mifflin_st_jeor(profile)
            return self._cunningham(profile, body_fat_percentage)
        else:
            return self._mifflin_st_jeor(profile)
    
    def calculate_tdee(self, profile: UserProfile, recent_biometrics: List[BiometricData] = None,
                      adaptive: bool = True) -> Dict[str, float]:
        """
        Calculate Total Daily Energy Expenditure with adaptive adjustments
        
        Args:
            profile: User profile
            recent_biometrics: Recent biometric data for adaptations
            adaptive: Whether to apply biometric-based adaptations
            
        Returns:
            Dictionary with TDEE breakdown and adaptive factors
        """
        # Get optimal body fat percentage for calculations
        body_fat = self._estimate_body_fat_percentage(profile, recent_biometrics)
        
        # Calculate base BMR
        bmr = self.calculate_bmr(profile, BMRFormula.MIFFLIN_ST_JEOR, body_fat)
        
        # Base TDEE from activity level
        base_tdee = bmr * profile.activity_level.value
        
        if not adaptive or not recent_biometrics:
            return {
                'bmr': bmr,
                'base_tdee': base_tdee,
                'adaptive_tdee': base_tdee,
                'adaptive_factors': self.adaptive_factors.copy()
            }
        
        # Apply adaptive adjustments
        adaptive_factors = self._calculate_adaptive_factors(profile, recent_biometrics)
        adaptive_multiplier = np.prod(list(adaptive_factors.values()))
        adaptive_tdee = base_tdee * adaptive_multiplier
        
        return {
            'bmr': bmr,
            'base_tdee': base_tdee,
            'adaptive_tdee': adaptive_tdee,
            'adaptive_factors': adaptive_factors,
            'adaptive_multiplier': adaptive_multiplier
        }
    
    def calculate_calorie_needs_by_goal(self, profile: UserProfile, 
                                      goal: str = "maintain",
                                      rate_kg_per_week: float = 0.5) -> Dict[str, float]:
        """
        Calculate calorie needs based on user goals
        
        Args:
            profile: User profile
            goal: "lose", "gain", or "maintain"
            rate_kg_per_week: Rate of weight change (kg per week)
            
        Returns:
            Calorie targets for different goals
        """
        tdee_data = self.calculate_tdee(profile)
        base_calories = tdee_data['adaptive_tdee']
        
        # 1 kg fat = ~7700 calories (3500 calories per pound * 2.2)
        calories_per_kg = 7700
        daily_calorie_adjustment = (rate_kg_per_week * calories_per_kg) / 7
        
        goals = {
            'maintain': base_calories,
            'lose': base_calories - abs(daily_calorie_adjustment),
            'gain': base_calories + abs(daily_calorie_adjustment)
        }
        
        # Safety bounds
        min_calories = max(profile.calculate_bmr() * 1.1, 1200)  # Never below 1200 or 110% BMR
        max_calories = base_calories * 1.5  # Never above 150% of TDEE
        
        for goal_type in goals:
            goals[goal_type] = max(min_calories, min(goals[goal_type], max_calories))
        
        return {
            'maintenance': goals['maintain'],
            'weight_loss': goals['lose'],
            'weight_gain': goals['gain'],
            'min_safe_calories': min_calories,
            'max_safe_calories': max_calories,
            'tdee_breakdown': tdee_data
        }
    
    def _mifflin_st_jeor(self, profile: UserProfile) -> float:
        """Mifflin-St Jeor formula (most accurate for general population)"""
        if profile.sex.lower() == "male":
            return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
        else:
            return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161
    
    def _harris_benedict(self, profile: UserProfile) -> float:
        """Harris-Benedict formula (traditional, less accurate)"""
        if profile.sex.lower() == "male":
            return 88.362 + (13.397 * profile.weight_kg) + (4.799 * profile.height_cm) - (5.677 * profile.age)
        else:
            return 447.593 + (9.247 * profile.weight_kg) + (3.098 * profile.height_cm) - (4.330 * profile.age)
    
    def _katch_mcardle(self, profile: UserProfile, body_fat_percentage: float) -> float:
        """Katch-McArdle formula (uses lean body mass)"""
        lean_mass_kg = profile.weight_kg * (1 - body_fat_percentage / 100)
        return 370 + (21.6 * lean_mass_kg)
    
    def _cunningham(self, profile: UserProfile, body_fat_percentage: float) -> float:
        """Cunningham formula (for athletes with low body fat)"""
        lean_mass_kg = profile.weight_kg * (1 - body_fat_percentage / 100)
        return 500 + (22 * lean_mass_kg)
    
    def _estimate_body_fat_percentage(self, profile: UserProfile, 
                                    recent_biometrics: List[BiometricData] = None) -> Optional[float]:
        """Estimate body fat percentage using available data"""
        # Check if we have recent body fat measurements
        if recent_biometrics:
            for bio in sorted(recent_biometrics, key=lambda x: x.timestamp, reverse=True):
                if bio.body_fat_percentage is not None:
                    return bio.body_fat_percentage
        
        # Estimate using BMI and demographics (rough approximation)
        bmi = profile.weight_kg / ((profile.height_cm / 100) ** 2)
        
        if profile.sex.lower() == "male":
            # Deurenberg formula for men
            body_fat = (1.20 * bmi) + (0.23 * profile.age) - 16.2
        else:
            # Deurenberg formula for women
            body_fat = (1.20 * bmi) + (0.23 * profile.age) - 5.4
        
        # Clamp to reasonable ranges
        return max(5, min(body_fat, 50))
    
    def _calculate_adaptive_factors(self, profile: UserProfile, 
                                  recent_biometrics: List[BiometricData]) -> Dict[str, float]:
        """Calculate adaptive factors based on biometric trends"""
        factors = self.adaptive_factors.copy()
        
        if not recent_biometrics:
            return factors
        
        # Sort by timestamp (most recent first)
        sorted_biometrics = sorted(recent_biometrics, key=lambda x: x.timestamp, reverse=True)
        
        # Sleep quality factor
        sleep_factor = self._calculate_sleep_factor(sorted_biometrics)
        factors['sleep_quality'] = sleep_factor
        
        # Glucose regulation factor
        glucose_factor = self._calculate_glucose_factor(sorted_biometrics)
        factors['glucose_regulation'] = glucose_factor
        
        # Activity consistency factor
        activity_factor = self._calculate_activity_factor(sorted_biometrics)
        factors['activity_consistency'] = activity_factor
        
        # Heart rate variability (stress indicator)
        stress_factor = self._calculate_stress_factor(sorted_biometrics)
        factors['stress_level'] = stress_factor
        
        # Recovery status based on multiple factors
        recovery_factor = self._calculate_recovery_factor(sorted_biometrics)
        factors['recovery_status'] = recovery_factor
        
        return factors
    
    def _calculate_sleep_factor(self, biometrics: List[BiometricData]) -> float:
        """Calculate sleep quality impact on metabolism"""
        sleep_hours = [b.sleep_hours for b in biometrics[-7:] if b.sleep_hours is not None]
        
        if not sleep_hours:
            return 1.0
        
        avg_sleep = np.mean(sleep_hours)
        
        # Optimal sleep is 7-9 hours
        if 7 <= avg_sleep <= 9:
            return 1.0
        elif avg_sleep < 6:
            # Poor sleep reduces metabolism
            return 0.95 - (6 - avg_sleep) * 0.02
        elif avg_sleep > 10:
            # Excessive sleep may indicate recovery needs
            return 0.98
        else:
            return 1.0
    
    def _calculate_glucose_factor(self, biometrics: List[BiometricData]) -> float:
        """Calculate glucose regulation impact"""
        glucose_readings = [b.glucose_mg_dl for b in biometrics[-5:] if b.glucose_mg_dl is not None]
        
        if not glucose_readings:
            return 1.0
        
        avg_glucose = np.mean(glucose_readings)
        
        # Normal fasting glucose: 70-100 mg/dL
        # Post-meal glucose: <140 mg/dL
        if avg_glucose > 140:
            # High glucose suggests insulin resistance
            return 0.92
        elif avg_glucose > 120:
            return 0.96
        elif 70 <= avg_glucose <= 100:
            return 1.02  # Good glucose control slightly boosts metabolism
        else:
            return 1.0
    
    def _calculate_activity_factor(self, biometrics: List[BiometricData]) -> float:
        """Calculate activity consistency impact"""
        steps = [b.steps for b in biometrics[-7:] if b.steps is not None]
        
        if len(steps) < 3:
            return 1.0
        
        avg_steps = np.mean(steps)
        step_variability = np.std(steps) / avg_steps if avg_steps > 0 else 0
        
        # Consistent high activity boosts metabolism
        if avg_steps > 10000 and step_variability < 0.3:
            return 1.05
        elif avg_steps > 8000 and step_variability < 0.4:
            return 1.02
        elif avg_steps < 3000:
            return 0.95
        else:
            return 1.0
    
    def _calculate_stress_factor(self, biometrics: List[BiometricData]) -> float:
        """Calculate stress impact based on heart rate patterns"""
        hr_readings = [b.heart_rate for b in biometrics[-5:] if b.heart_rate is not None]
        
        if len(hr_readings) < 3:
            return 1.0
        
        avg_hr = np.mean(hr_readings)
        hr_variability = np.std(hr_readings)
        
        # High resting HR or high variability suggests stress
        if avg_hr > 80 or hr_variability > 15:
            return 0.96  # Stress can reduce metabolic efficiency
        elif 60 <= avg_hr <= 70 and hr_variability < 10:
            return 1.02  # Good cardiovascular health
        else:
            return 1.0
    
    def _calculate_recovery_factor(self, biometrics: List[BiometricData]) -> float:
        """Calculate overall recovery status"""
        recent = biometrics[:3] if len(biometrics) >= 3 else biometrics
        
        recovery_indicators = []
        
        for bio in recent:
            score = 0
            indicators = 0
            
            # Sleep contribution
            if bio.sleep_hours is not None:
                if 7 <= bio.sleep_hours <= 9:
                    score += 1
                indicators += 1
            
            # Heart rate contribution
            if bio.heart_rate is not None:
                if 60 <= bio.heart_rate <= 75:
                    score += 1
                indicators += 1
            
            # Activity contribution
            if bio.steps is not None:
                if bio.steps >= 5000:
                    score += 1
                indicators += 1
            
            if indicators > 0:
                recovery_indicators.append(score / indicators)
        
        if not recovery_indicators:
            return 1.0
        
        avg_recovery = np.mean(recovery_indicators)
        
        # Good recovery slightly boosts metabolism
        if avg_recovery > 0.8:
            return 1.03
        elif avg_recovery > 0.6:
            return 1.01
        elif avg_recovery < 0.3:
            return 0.94
        else:
            return 1.0
    
    def get_metabolic_insights(self, profile: UserProfile, 
                             recent_biometrics: List[BiometricData] = None) -> Dict[str, Any]:
        """Generate insights about user's metabolic status"""
        tdee_data = self.calculate_tdee(profile, recent_biometrics, adaptive=True)
        calorie_needs = self.calculate_calorie_needs_by_goal(profile)
        
        insights = {
            'metabolic_rate': 'normal',
            'recommendations': [],
            'adaptations_active': [],
            'health_indicators': {}
        }
        
        # Analyze adaptive factors
        factors = tdee_data['adaptive_factors']
        
        if factors['sleep_quality'] < 0.95:
            insights['recommendations'].append("Improve sleep quality and duration")
            insights['adaptations_active'].append("Sleep-adjusted metabolism")
        
        if factors['glucose_regulation'] < 0.95:
            insights['recommendations'].append("Focus on blood sugar stability")
            insights['adaptations_active'].append("Glucose-regulated adjustments")
        
        if factors['activity_consistency'] < 0.98:
            insights['recommendations'].append("Maintain consistent daily activity")
            insights['adaptations_active'].append("Activity-based adjustments")
        
        if factors['stress_level'] < 0.98:
            insights['recommendations'].append("Implement stress management techniques")
            insights['adaptations_active'].append("Stress-response adjustments")
        
        # Overall metabolic rate assessment
        multiplier = tdee_data['adaptive_multiplier']
        if multiplier > 1.05:
            insights['metabolic_rate'] = 'high'
        elif multiplier < 0.95:
            insights['metabolic_rate'] = 'low'
        
        insights['health_indicators'] = {
            'metabolic_flexibility': multiplier,
            'sleep_efficiency': factors['sleep_quality'],
            'glucose_stability': factors['glucose_regulation'],
            'activity_consistency': factors['activity_consistency'],
            'stress_resilience': factors['stress_level'],
            'recovery_capacity': factors['recovery_status']
        }
        
        return insights