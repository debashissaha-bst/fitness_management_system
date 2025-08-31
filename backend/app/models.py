from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.utcnow()
        self.level = 1
        self.experience = 0
        self.badges = []
        self.milestones = []
        self.preferences = None 

class UserPreferences:
    def __init__(self, age_group, dietary_preference, fitness_goal):
        self.age_group = age_group  
        self.dietary_preference = dietary_preference  
        self.fitness_goal = fitness_goal 
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow() 

class Meal:
    def __init__(self, name, tags, meal_type):
        self.name = name
        self.tags = tags  
        self.meal_type = meal_type  
        self.created_at = datetime.utcnow()

class GeneratedMealPlan:
    def __init__(self, user_id, date, breakfast, lunch, dinner):
        self.user_id = user_id
        self.date = date
        self.breakfast = breakfast  
        self.lunch = lunch  
        self.dinner = dinner 
        self.created_at = datetime.utcnow()

class Badge:
    def __init__(self, name, description, icon, category, requirement_value):
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category 
        self.requirement_value = requirement_value 
        self.created_at = datetime.utcnow()

class Milestone:
    def __init__(self, name, description, icon, category, requirement_value):
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category  
        self.requirement_value = requirement_value
        self.created_at = datetime.utcnow()

class FitnessChallenge:
    def __init__(self, name, description, duration_days, challenge_type, requirements):
        self.name = name
        self.description = description
        self.duration_days = duration_days
        self.challenge_type = challenge_type 
        self.requirements = requirements 
        self.created_at = datetime.utcnow()

class UserChallenge:
    def __init__(self, user_id, challenge_id, start_date, end_date, progress):
        self.user_id = user_id
        self.challenge_id = challenge_id
        self.start_date = start_date
        self.end_date = end_date
        self.progress = progress 
        self.completed = False
        self.completed_at = None
        self.created_at = datetime.utcnow()

class Task:
    def __init__(self, user_id, title, description, task_type, completed, due_date):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.task_type = task_type  
        self.completed = completed
        self.due_date = due_date
        self.completed_at = None
        self.created_at = datetime.utcnow()
