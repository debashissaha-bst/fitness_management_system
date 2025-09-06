import random
import copy
from typing import List, Dict, Any
from datetime import datetime, date

class MealGenerationService:
    def __init__(self):
        self.meals_database = self._initialize_meals_database()
    
    def _initialize_meals_database(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Paratha with Aloo Bhaji", "tags": ["vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Chirer Polao (Beaten Rice with Veggies)", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Vegetable Upma", "tags": ["vegetarian", "weight_loss", "adult", "older"]},
            {"name": "Moong Dal Cheela", "tags": ["vegetarian", "weight_loss", "adult", "young"]},
            {"name": "Idli with Coconut Chutney", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Dosa with Sambar", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Oats Porridge with Fruits", "tags": ["vegetarian", "weight_loss", "adult", "older"]},
            {"name": "Vegetable Upma with Nuts", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Masala Omelette with Brown Bread", "tags": ["non_vegetarian", "stay_fit", "adult", "young"]},
            {"name": "Vegetable Poha", "tags": ["vegetarian", "weight_loss", "adult", "young"]},
            {"name": "Ragi Dosa with Chutney", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Vegetable Semolina Pancakes", "tags": ["vegetarian", "stay_fit", "adult", "older"]},

            {"name": "Shutki Maach Bhuna with Rice", "tags": ["non_vegetarian", "weight_loss", "adult", "older"]},
            {"name": "Shorshe Ilish with Rice", "tags": ["non_vegetarian", "stay_fit", "adult", "young"]},
            {"name": "Dim Curry with Ruti", "tags": ["non_vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Chicken Curry with Rice", "tags": ["non_vegetarian", "stay_fit", "adult", "young"]},
            {"name": "Beef Rezala with Paratha", "tags": ["non_vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Mutton Korma with Rice", "tags": ["non_vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Aloo Posto with Rice", "tags": ["vegetarian", "weight_loss", "adult", "older"]},
            {"name": "Lau Ghonto with Dal", "tags": ["vegetarian", "weight_loss", "adult", "older"]},
            {"name": "Chingri Malai Curry with Rice", "tags": ["non_vegetarian", "stay_fit", "adult", "young"]},
            {"name": "Rohu Curry with Rice", "tags": ["non_vegetarian", "stay_fit", "adult", "young"]},
            {"name": "Vegetable Pulao with Raita", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Fish Curry with Brown Rice", "tags": ["non_vegetarian", "weight_loss", "adult", "older"]},
            {"name": "Chicken Tikka with Chapati", "tags": ["non_vegetarian", "weight_loss", "adult", "young"]},
            {"name": "Mixed Vegetable Curry with Roti", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Masoor Dal with Steamed Rice", "tags": ["vegetarian", "weight_loss", "adult", "older"]},

            {"name": "Khichuri with Beguni", "tags": ["vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Chicken Khichuri", "tags": ["non_vegetarian", "stay_fit", "adult", "older"]},
            {"name": "Vegetable Tehari", "tags": ["vegetarian", "stay_fit", "adult", "young"]},
            {"name": "Beef Tehari", "tags": ["non_vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Biriyani with Egg & Mutton", "tags": ["non_vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Paratha with Beef Curry", "tags": ["non_vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Paneer Butter Masala with Naan", "tags": ["vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Cholar Dal with Luchi", "tags": ["vegetarian", "weight_gain", "adult", "young"]},
            {"name": "Steamed Hilsa with Mustard", "tags": ["non_vegetarian", "weight_loss", "adult", "young", "no_sugar"]},
            {"name": "Steamed Vegetables with Paneer", "tags": ["vegetarian", "weight_loss", "adult", "older", "no_sugar"]},
            {"name": "Chicken Stew with Vegetables", "tags": ["non_vegetarian", "weight_loss", "adult", "older", "no_sugar"]},
            {"name": "Moong Dal Soup", "tags": ["vegetarian", "weight_loss", "adult", "older", "no_sugar"]},
            {"name": "Grilled Pomfret with Salad", "tags": ["non_vegetarian", "weight_loss", "adult", "older", "no_sugar"]},
            {"name": "Vegetable Clear Soup with Tofu", "tags": ["vegetarian", "weight_loss", "adult", "older", "no_sugar"]},
]    

     
    def filter_meals_by_preferences(self, age_group: str, dietary_preference: str, fitness_goal: str) -> List[Dict]:    
    
        filtered_meals: List[Dict] = [] 
        for meal in self.meals_database:
            if self._meal_matches_preferences(meal, age_group, dietary_preference, fitness_goal):
                filtered_meals.append(meal)
        return filtered_meals
    
    def _meal_matches_preferences(self, meal: Dict, age_group: str, dietary_preference: str, fitness_goal: str) -> bool:
    
        tags = meal["tags"]
        
    
        if age_group not in tags:
            return False
        
        if dietary_preference == "vegetarian" and "non_vegetarian" in tags:
            return False
        elif dietary_preference == "non_vegetarian" and "vegetarian" in tags:
            return False
        
        if fitness_goal not in tags:
            return False
        
        if dietary_preference == "no_sugar" and "no_sugar" not in tags:
            return False
        
        return True 
    
    def generate_meal_plan(self, age_group: str, dietary_preference: str, fitness_goal: str) -> Dict[str, Any]:
        """Generate a meal plan using genetic algorithm"""
        filtered_meals = self.filter_meals_by_preferences(age_group, dietary_preference, fitness_goal)
        
        # Ensure we have enough options overall
        if len(filtered_meals) < 3:
            filtered_meals = self._get_fallback_meals(age_group, dietary_preference, fitness_goal)
        
        # Use genetic algorithm to optimize meal selection
        best_meal_plan = self._genetic_algorithm_optimization(filtered_meals, fitness_goal)
        
        return best_meal_plan
    
    def _get_fallback_meals(self, age_group: str, dietary_preference: str, fitness_goal: str) -> List[Dict]:
        """Get fallback meals when strict filtering doesn't provide enough options"""
        fallback_meals: List[Dict] = []
        for meal in self.meals_database:
            # Relax some constraints: still align with dietary preference and goal
            tags = meal["tags"]
            if dietary_preference == "vegetarian" and "non_vegetarian" in tags:
                continue
            elif dietary_preference == "non_vegetarian" and "vegetarian" in tags:
                continue
            if fitness_goal not in tags:
                continue
            fallback_meals.append(meal)
            if len(fallback_meals) >= 9:
                break
        return fallback_meals
    
    def _genetic_algorithm_optimization(self, filtered_meals: List[Dict], fitness_goal: str) -> Dict[str, Any]:
        """Optimize meal selection using genetic algorithm"""
        population_size = 50
        generations = 100
        mutation_rate = 0.1
        
        # Initialize population
        population = self._initialize_population(filtered_meals, population_size)
        
        # Evolution loop
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = [self._calculate_fitness(individual, fitness_goal) for individual in population]
            
            # Selection
            new_population = []
            for _ in range(population_size):
                parent1 = self._tournament_selection(population, fitness_scores)
                parent2 = self._tournament_selection(population, fitness_scores)
                
                # Crossover
                child = self._crossover(parent1, parent2)
                
                # Mutation
                if random.random() < mutation_rate:
                    child = self._mutate(child, filtered_meals)
                
                new_population.append(child)
            
            population = new_population
        
        # Get best individual
        best_individual = max(population, key=lambda x: self._calculate_fitness(x, fitness_goal))
        
        return self._format_meal_plan(best_individual, filtered_meals)
    
    def _initialize_population(self, filtered_meals: List[Dict], population_size: int) -> List[List[int]]:
        """Initialize population with random meal selections (3 indices)"""
        population: List[List[int]] = []
        total = max(len(filtered_meals), 1)
        for _ in range(population_size):
            if total >= 3:
                individual = random.sample(range(total), 3)
            else:
                individual = [0, 0, 0]
            population.append(individual)
        return population
    
    def _calculate_fitness(self, individual: List[int], fitness_goal: str) -> float:
        """Calculate fitness score for an individual"""
        
        fitness_score = 100.0
        
        # Bonus for variety (different meals)
        if len(set(individual)) == 3:
            fitness_score += 20
        
        # Bonus for fitness goal alignment
        if fitness_goal == "weight_loss":
            fitness_score += 15
        elif fitness_goal == "weight_gain":
            fitness_score += 15
        else:  # stay_fit
            fitness_score += 10
        
        return fitness_score
    
    def _tournament_selection(self, population: List[List[int]], fitness_scores: List[float]) -> List[int]:
        """Tournament selection for parent selection"""
        tournament_size = 3
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        
        winner_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return population[winner_index]
    
    def _crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """Single-point crossover between two parents"""
        crossover_point = random.randint(1, 2)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child
    
    def _mutate(self, individual: List[int], filtered_meals: List[Dict]) -> List[int]:
        """Mutate an individual by changing one meal index"""
        mutation_point = random.randint(0, 2)
        total = len(filtered_meals)
        if total > 0:
            individual[mutation_point] = random.randint(0, total - 1)
        return individual
    
    def _format_meal_plan(self, individual: List[int], filtered_meals: List[Dict]) -> Dict[str, Any]:
        """Format the best individual into a meal plan mapped to breakfast/lunch/dinner"""
        meal_plan: Dict[str, Any] = {}
        labels = ["breakfast", "lunch", "dinner"]
        for i, label in enumerate(labels):
            idx = individual[i] if i < len(individual) else 0
            if filtered_meals and 0 <= idx < len(filtered_meals):
                meal_plan[label] = filtered_meals[idx]
            else:
                meal_plan[label] = {"name": "Default Meal"}
        meal_plan["generated_at"] = datetime.utcnow().isoformat()
        return meal_plan

meal_generation_service = MealGenerationService() 
