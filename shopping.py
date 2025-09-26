"""
Shopping list generation module
Creates optimized shopping lists with cost estimates and nutritional grouping
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import json

from models import UserProfile
from config import Config


class ShoppingListGenerator:
    """Generate optimized shopping lists from meal plans"""
    
    def __init__(self):
        self.standard_portions = {
            # Standard package sizes for common items
            'milk': 1000,  # 1L
            'eggs': 12,    # dozen
            'bread': 1,    # loaf
            'rice': 1000,  # 1kg bag
            'pasta': 500,  # 500g box
            'oats': 500,   # 500g container
        }
        
        self.conversion_factors = {
            # Conversion from 100g to typical units
            'milk': {'unit': 'ml', 'factor': 100},
            'yogurt': {'unit': 'ml', 'factor': 100},
            'rice': {'unit': 'g', 'factor': 100},
            'pasta': {'unit': 'g', 'factor': 100},
            'oats': {'unit': 'g', 'factor': 100},
            'chicken': {'unit': 'g', 'factor': 100},
            'salmon': {'unit': 'g', 'factor': 100},
            'eggs': {'unit': 'pieces', 'factor': 2},  # ~50g per egg
            'bread': {'unit': 'slices', 'factor': 3.3},  # ~30g per slice
        }
    
    def generate_shopping_list(self, meals: List[Dict[str, Any]], 
                             profile: UserProfile,
                             days: int = 7,
                             include_cost_estimates: bool = True) -> Dict[str, Any]:
        """
        Generate comprehensive shopping list from meal plans
        
        Args:
            meals: List of meal dictionaries
            profile: User profile for preferences
            days: Number of days the shopping list should cover
            include_cost_estimates: Whether to include cost estimates
            
        Returns:
            Dictionary with categorized shopping list and totals
        """
        # Aggregate ingredients from all meals
        ingredient_totals = self._aggregate_ingredients(meals, days)
        
        # Convert to shopping units
        shopping_items = self._convert_to_shopping_units(ingredient_totals)
        
        # Categorize items
        categorized_items = self._categorize_items(shopping_items)
        
        # Calculate costs if requested
        total_cost = 0
        if include_cost_estimates:
            total_cost = self._calculate_total_cost(shopping_items)
        
        # Add suggested substitutions
        substitutions = self._suggest_substitutions(shopping_items, profile)
        
        # Generate shopping tips
        shopping_tips = self._generate_shopping_tips(categorized_items, profile)
        
        return {
            'shopping_list': categorized_items,
            'total_items': len(shopping_items),
            'estimated_cost': total_cost,
            'currency': 'USD',
            'days_covered': days,
            'substitutions': substitutions,
            'shopping_tips': shopping_tips,
            'preparation_notes': self._generate_preparation_notes(shopping_items)
        }
    
    def _aggregate_ingredients(self, meals: List[Dict[str, Any]], days: int) -> Dict[str, float]:
        """Aggregate ingredient quantities across all meals"""
        ingredient_totals = defaultdict(float)
        
        for meal in meals:
            items = meal.get('items', [])
            portions = meal.get('portions', [])
            
            # If no portions specified, estimate from calories
            if not portions and 'calories' in meal and items:
                estimated_portion = meal['calories'] / len(items) / 2  # Rough estimate
                portions = [estimated_portion] * len(items)
            
            for i, item in enumerate(items):
                if i < len(portions):
                    quantity = portions[i]
                else:
                    quantity = 100  # Default 100g
                
                # Multiply by days to get total quantity needed
                ingredient_totals[item] += quantity * days
        
        return dict(ingredient_totals)
    
    def _convert_to_shopping_units(self, ingredient_totals: Dict[str, float]) -> List[Dict[str, Any]]:
        """Convert ingredient quantities to practical shopping units"""
        shopping_items = []
        
        for ingredient, total_grams in ingredient_totals.items():
            item_key = self._find_conversion_key(ingredient)
            
            if item_key in self.conversion_factors:
                conversion = self.conversion_factors[item_key]
                converted_quantity = total_grams / conversion['factor']
                unit = conversion['unit']
            else:
                # Default to grams
                converted_quantity = total_grams
                unit = 'g'
            
            # Round to practical quantities
            practical_quantity = self._round_to_practical_quantity(converted_quantity, unit)
            
            shopping_items.append({
                'item': ingredient,
                'quantity': practical_quantity,
                'unit': unit,
                'original_grams': total_grams,
                'category': self._categorize_single_item(ingredient)
            })
        
        return shopping_items
    
    def _find_conversion_key(self, ingredient: str) -> str:
        """Find the best conversion key for an ingredient"""
        ingredient_lower = ingredient.lower()
        
        for key in self.conversion_factors.keys():
            if key in ingredient_lower:
                return key
        
        return ingredient_lower
    
    def _round_to_practical_quantity(self, quantity: float, unit: str) -> float:
        """Round quantities to practical shopping amounts"""
        if unit == 'g':
            if quantity < 50:
                return 50
            elif quantity < 250:
                return round(quantity / 50) * 50
            elif quantity < 1000:
                return round(quantity / 100) * 100
            else:
                return round(quantity / 250) * 250
        
        elif unit == 'ml':
            if quantity < 250:
                return 250
            elif quantity < 1000:
                return round(quantity / 250) * 250
            else:
                return round(quantity / 500) * 500
        
        elif unit == 'pieces':
            return max(1, round(quantity))
        
        elif unit == 'slices':
            return max(1, round(quantity))
        
        else:
            return round(quantity, 1)
    
    def _categorize_items(self, shopping_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize shopping items by food category"""
        categories = {
            'Proteins': [],
            'Dairy & Eggs': [],
            'Grains & Carbs': [],
            'Fruits': [],
            'Vegetables': [],
            'Fats & Oils': [],
            'Pantry & Others': []
        }
        
        category_mapping = {
            'protein': 'Proteins',
            'dairy': 'Dairy & Eggs',
            'carbohydrate': 'Grains & Carbs',
            'fruit': 'Fruits',
            'vegetable': 'Vegetables',
            'fat': 'Fats & Oils'
        }
        
        for item in shopping_items:
            category = item.get('category', 'other')
            target_category = category_mapping.get(category, 'Pantry & Others')
            categories[target_category].append(item)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def _categorize_single_item(self, ingredient: str) -> str:
        """Categorize a single ingredient"""
        ingredient_lower = ingredient.lower()
        
        # Protein sources
        if any(word in ingredient_lower for word in ['chicken', 'beef', 'pork', 'turkey', 'fish', 
                                                    'salmon', 'tuna', 'tofu', 'lentils', 'beans']):
            return 'protein'
        
        # Dairy and eggs
        if any(word in ingredient_lower for word in ['milk', 'cheese', 'yogurt', 'butter', 'eggs']):
            return 'dairy'
        
        # Grains and carbs
        if any(word in ingredient_lower for word in ['rice', 'bread', 'pasta', 'oats', 'quinoa', 
                                                    'potato', 'sweet potato']):
            return 'carbohydrate'
        
        # Fruits
        if any(word in ingredient_lower for word in ['apple', 'banana', 'berry', 'orange', 
                                                    'grape', 'mango', 'pear']):
            return 'fruit'
        
        # Vegetables
        if any(word in ingredient_lower for word in ['broccoli', 'spinach', 'carrot', 'pepper', 
                                                    'onion', 'garlic', 'tomato', 'lettuce']):
            return 'vegetable'
        
        # Fats and oils
        if any(word in ingredient_lower for word in ['oil', 'avocado', 'nuts', 'almond', 'olive']):
            return 'fat'
        
        return 'other'
    
    def _calculate_total_cost(self, shopping_items: List[Dict[str, Any]]) -> float:
        """Calculate estimated total cost of shopping list"""
        total_cost = 0
        
        # Cost estimates per 100g (simplified)
        cost_estimates = {
            'chicken': 2.50,
            'salmon': 4.20,
            'turkey': 3.20,
            'beef': 5.00,
            'eggs': 1.20,
            'milk': 0.60,
            'yogurt': 1.50,
            'cheese': 3.00,
            'rice': 0.45,
            'bread': 1.20,
            'pasta': 0.80,
            'oats': 0.35,
            'quinoa': 1.20,
            'potato': 0.30,
            'sweet potato': 0.65,
            'broccoli': 0.80,
            'spinach': 1.10,
            'carrot': 0.50,
            'apple': 0.80,
            'banana': 0.40,
            'avocado': 2.80,
            'almonds': 3.50,
            'olive oil': 4.50
        }
        
        for item in shopping_items:
            item_name = item['item'].lower()
            original_grams = item['original_grams']
            
            # Find best cost estimate
            cost_per_100g = 1.50  # Default cost
            for key, cost in cost_estimates.items():
                if key in item_name:
                    cost_per_100g = cost
                    break
            
            item_cost = (original_grams / 100) * cost_per_100g
            total_cost += item_cost
            
            # Add cost to item
            item['estimated_cost'] = round(item_cost, 2)
        
        return round(total_cost, 2)
    
    def _suggest_substitutions(self, shopping_items: List[Dict[str, Any]], 
                             profile: UserProfile) -> List[Dict[str, Any]]:
        """Suggest ingredient substitutions based on user preferences and budget"""
        substitutions = []
        
        budget_threshold = (profile.daily_budget or Config.DEFAULT_DAILY_BUDGET) * 7 * 0.8
        
        for item in shopping_items:
            item_cost = item.get('estimated_cost', 0)
            
            # Suggest cheaper alternatives for expensive items
            if item_cost > budget_threshold * 0.1:  # If item is >10% of weekly budget
                alternatives = self._get_cheaper_alternatives(item['item'])
                if alternatives:
                    substitutions.append({
                        'original': item['item'],
                        'alternatives': alternatives,
                        'reason': 'Budget-friendly option',
                        'potential_savings': round(item_cost * 0.3, 2)
                    })
            
            # Suggest alternatives for dietary restrictions
            dietary_alternatives = self._get_dietary_alternatives(item['item'], profile)
            if dietary_alternatives:
                substitutions.extend(dietary_alternatives)
        
        return substitutions
    
    def _get_cheaper_alternatives(self, ingredient: str) -> List[str]:
        """Get cheaper alternatives for expensive ingredients"""
        alternatives_map = {
            'salmon': ['tuna', 'chicken breast', 'eggs'],
            'beef': ['ground turkey', 'chicken thighs', 'lentils'],
            'almonds': ['peanuts', 'sunflower seeds'],
            'quinoa': ['brown rice', 'oats'],
            'avocado': ['olive oil', 'nuts'],
            'organic': ['conventional equivalent']
        }
        
        ingredient_lower = ingredient.lower()
        for key, alternatives in alternatives_map.items():
            if key in ingredient_lower:
                return alternatives
        
        return []
    
    def _get_dietary_alternatives(self, ingredient: str, profile: UserProfile) -> List[Dict[str, Any]]:
        """Get dietary restriction alternatives"""
        alternatives = []
        ingredient_lower = ingredient.lower()
        
        # Vegetarian alternatives
        if any('vegetarian' in str(dr).lower() for dr in profile.dietary_preferences.dietary_restrictions):
            if any(meat in ingredient_lower for meat in ['chicken', 'beef', 'pork', 'turkey', 'fish']):
                alternatives.append({
                    'original': ingredient,
                    'alternatives': ['tofu', 'tempeh', 'beans', 'lentils'],
                    'reason': 'Vegetarian alternative'
                })
        
        # Dairy-free alternatives
        if any('dairy' in str(dr).lower() for dr in profile.dietary_preferences.dietary_restrictions):
            dairy_alternatives = {
                'milk': ['almond milk', 'oat milk', 'soy milk'],
                'cheese': ['nutritional yeast', 'cashew cheese'],
                'yogurt': ['coconut yogurt', 'almond yogurt'],
                'butter': ['olive oil', 'coconut oil']
            }
            
            for dairy_item, alts in dairy_alternatives.items():
                if dairy_item in ingredient_lower:
                    alternatives.append({
                        'original': ingredient,
                        'alternatives': alts,
                        'reason': 'Dairy-free alternative'
                    })
        
        return alternatives
    
    def _generate_shopping_tips(self, categorized_items: Dict[str, List], 
                              profile: UserProfile) -> List[str]:
        """Generate helpful shopping tips"""
        tips = []
        
        # Budget tips
        if profile.daily_budget and profile.daily_budget < 20:
            tips.append("Shop seasonal produce for better prices")
            tips.append("Consider frozen vegetables as cost-effective alternatives")
            tips.append("Buy grains and legumes in bulk to save money")
        
        # Storage tips
        if 'Fruits' in categorized_items and len(categorized_items['Fruits']) > 3:
            tips.append("Store fruits at different ripeness levels to last the full week")
        
        if 'Vegetables' in categorized_items:
            tips.append("Prep vegetables when you get home to save cooking time")
        
        # Meal prep tips
        tips.append("Consider batch cooking grains and proteins for the week")
        tips.append("Check your pantry before shopping to avoid duplicates")
        
        # Quality tips
        tips.append("Choose organic for the 'Dirty Dozen' produce items when budget allows")
        
        return tips
    
    def _generate_preparation_notes(self, shopping_items: List[Dict[str, Any]]) -> List[str]:
        """Generate preparation and storage notes"""
        notes = []
        
        # Check for items that need prep
        prep_items = [item['item'] for item in shopping_items 
                     if any(word in item['item'].lower() for word in ['rice', 'quinoa', 'lentils', 'beans'])]
        
        if prep_items:
            notes.append(f"Soak/prep items that require longer cooking: {', '.join(prep_items[:3])}")
        
        # Storage notes
        notes.append("Store proteins in coldest part of refrigerator")
        notes.append("Keep fruits and vegetables in separate crisper drawers")
        notes.append("Freeze any proteins you won't use within 2-3 days")
        
        return notes