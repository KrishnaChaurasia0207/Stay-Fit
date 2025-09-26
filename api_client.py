"""
API Integration layer for external nutrition data sources
Handles Spoonacular and USDA FoodData Central APIs with intelligent caching
"""

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from config import Config


class APICache:
    """Intelligent caching system for API responses"""
    
    def __init__(self, cache_path: str = None):
        self.cache_path = cache_path or Config.CACHE_DB_PATH
        self.cache_data = self._load_cache()
        self.max_size = Config.CACHE_MAX_SIZE
        self.expiry_hours = Config.CACHE_EXPIRY_HOURS
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache from disk"""
        cache_path = Path(self.cache_path)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        cache_path = Path(self.cache_path)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove expired entries before saving
        self._cleanup_expired()
        
        # Limit cache size
        if len(self.cache_data) > self.max_size:
            # Remove oldest entries
            sorted_items = sorted(
                self.cache_data.items(),
                key=lambda x: x[1].get('timestamp', 0)
            )
            self.cache_data = dict(sorted_items[-self.max_size:])
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _cleanup_expired(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, value in self.cache_data.items():
            if current_time - value.get('timestamp', 0) > (self.expiry_hours * 3600):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache_data[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key not in self.cache_data:
            return None
        
        entry = self.cache_data[key]
        if time.time() - entry.get('timestamp', 0) > (self.expiry_hours * 3600):
            del self.cache_data[key]
            return None
        
        return entry.get('data')
    
    def set(self, key: str, value: Any):
        """Cache a value with timestamp"""
        self.cache_data[key] = {
            'data': value,
            'timestamp': time.time()
        }
        self._save_cache()


class NutritionAPIClient:
    """Main API client for nutrition data from multiple sources"""
    
    def __init__(self):
        self.config = Config.get_api_config()
        self.cache = APICache()
        self.session = requests.Session()
        self.session.timeout = 30
    
    def search_food(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for food items across all available sources
        Returns standardized nutrition data
        """
        cache_key = f"search_{query}_{limit}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        results = []
        
        # Try Spoonacular first
        try:
            spoonacular_results = self._search_spoonacular(query, limit)
            results.extend(spoonacular_results)
        except Exception as e:
            print(f"Spoonacular API error: {e}")
        
        # Try USDA if we need more results
        if len(results) < limit:
            try:
                usda_results = self._search_usda(query, limit - len(results))
                results.extend(usda_results)
            except Exception as e:
                print(f"USDA API error: {e}")
        
        # Cache results
        self.cache.set(cache_key, results)
        return results
    
    def get_food_nutrition(self, food_id: str, source: str = "spoonacular") -> Optional[Dict[str, Any]]:
        """
        Get detailed nutrition information for a specific food item
        """
        cache_key = f"nutrition_{source}_{food_id}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            if source == "spoonacular":
                result = self._get_spoonacular_nutrition(food_id)
            elif source == "usda":
                result = self._get_usda_nutrition(food_id)
            else:
                return None
            
            if result:
                self.cache.set(cache_key, result)
            return result
        
        except Exception as e:
            print(f"API error getting nutrition for {food_id}: {e}")
            return None
    
    def _search_spoonacular(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search Spoonacular API for food items"""
        url = f"{self.config['spoonacular']['base_url']}/food/ingredients/search"
        params = {
            'apiKey': self.config['spoonacular']['key'],
            'query': query,
            'number': limit,
            'addChildren': 'true'
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            standardized = self._standardize_spoonacular_item(item)
            if standardized:
                results.append(standardized)
        
        return results
    
    def _search_usda(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search USDA FoodData Central API"""
        url = f"{self.config['usda']['base_url']}/foods/search"
        params = {
            'api_key': self.config['usda']['key'],
            'query': query,
            'pageSize': limit,
            'dataType': ['Foundation', 'SR Legacy']
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('foods', []):
            standardized = self._standardize_usda_item(item)
            if standardized:
                results.append(standardized)
        
        return results
    
    def _get_spoonacular_nutrition(self, food_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed nutrition from Spoonacular"""
        url = f"{self.config['spoonacular']['base_url']}/food/ingredients/{food_id}/information"
        params = {
            'apiKey': self.config['spoonacular']['key'],
            'amount': 100,
            'unit': 'grams'
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return self._standardize_spoonacular_nutrition(data)
    
    def _get_usda_nutrition(self, food_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed nutrition from USDA"""
        url = f"{self.config['usda']['base_url']}/food/{food_id}"
        params = {'api_key': self.config['usda']['key']}
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return self._standardize_usda_nutrition(data)
    
    def _standardize_spoonacular_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Spoonacular item to standardized format"""
        return {
            'id': str(item.get('id')),
            'name': item.get('name', ''),
            'source': 'spoonacular',
            'category': self._categorize_food(item.get('name', '')),
            'image': item.get('image')
        }
    
    def _standardize_usda_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Convert USDA item to standardized format"""
        return {
            'id': str(item.get('fdcId')),
            'name': item.get('description', ''),
            'source': 'usda',
            'category': self._categorize_food(item.get('description', '')),
            'brand': item.get('brandOwner')
        }
    
    def _standardize_spoonacular_nutrition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Spoonacular nutrition to standardized format"""
        nutrition = data.get('nutrition', {})
        nutrients = {n['name']: n['amount'] for n in nutrition.get('nutrients', [])}
        
        return {
            'name': data.get('name'),
            'calories_per_100g': nutrients.get('Calories', 0),
            'protein_g': nutrients.get('Protein', 0),
            'carbs_g': nutrients.get('Carbohydrates', 0),
            'fat_g': nutrients.get('Fat', 0),
            'fiber_g': nutrients.get('Fiber', 0),
            'sugar_g': nutrients.get('Sugar', 0),
            'sodium_mg': nutrients.get('Sodium', 0),
            'source': 'spoonacular'
        }
    
    def _standardize_usda_nutrition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert USDA nutrition to standardized format"""
        nutrient_map = {
            'Energy': 'calories_per_100g',
            'Protein': 'protein_g',
            'Carbohydrate, by difference': 'carbs_g',
            'Total lipid (fat)': 'fat_g',
            'Fiber, total dietary': 'fiber_g',
            'Sugars, total including NLEA': 'sugar_g',
            'Sodium, Na': 'sodium_mg'
        }
        
        nutrition = {'source': 'usda', 'name': data.get('description')}
        
        for nutrient in data.get('foodNutrients', []):
            nutrient_name = nutrient.get('nutrient', {}).get('name')
            if nutrient_name in nutrient_map:
                key = nutrient_map[nutrient_name]
                value = nutrient.get('amount', 0)
                
                # Convert sodium from mg to mg (already correct)
                # Convert other nutrients to per 100g basis
                nutrition[key] = value
        
        return nutrition
    
    def _categorize_food(self, name: str) -> str:
        """Categorize food based on name"""
        name_lower = name.lower()
        
        if any(word in name_lower for word in ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'tuna', 'egg']):
            return 'protein'
        elif any(word in name_lower for word in ['rice', 'bread', 'pasta', 'oat', 'quinoa', 'potato']):
            return 'carbohydrate'
        elif any(word in name_lower for word in ['oil', 'butter', 'avocado', 'nuts', 'almond']):
            return 'fat'
        elif any(word in name_lower for word in ['milk', 'cheese', 'yogurt']):
            return 'dairy'
        elif any(word in name_lower for word in ['apple', 'banana', 'berry', 'orange', 'grape']):
            return 'fruit'
        elif any(word in name_lower for word in ['broccoli', 'spinach', 'carrot', 'pepper', 'lettuce']):
            return 'vegetable'
        else:
            return 'other'