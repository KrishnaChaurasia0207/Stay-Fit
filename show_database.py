import json

# Load and display nutrition database
with open('data/nutrition_db.json', 'r') as f:
    data = json.load(f)

foods = data['foods']
print(f'🥗 Nutrition Database ({len(foods)} foods):')
print('   Name              Calories  Protein  Category')
print('   ' + '-' * 50)

for i, food in enumerate(foods):
    name = food['name'][:15].ljust(15)
    cal = f"{food['calories_per_100g']:3.0f}".rjust(3)
    protein = f"{food['protein_g']:4.1f}g".rjust(6)
    category = food['category']
    print(f'   {name} {cal} cal  {protein}  {category}')

print(f'\n✅ All {len(foods)} foods loaded and ready for meal planning!')