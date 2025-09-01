from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from bson import ObjectId
from .extensions import mongo
from .services import meal_generation_service

predefined_challenges = [ 
    {"_id": "1", "name": "7-Day Push-up Power", "details": "Do push-ups daily for a week.", "type": "7-Day", "duration": 7, "lvl": "Easy", "xp": 50},  
    {"_id": "2", "name": "7-Day Morning Stretch", "details": "Start your day with stretches for 7 days.", "type": "7-Day", "duration": 7, "lvl": "Easy", "xp": 50},
    {"_id": "3", "name": "7-Day Hydration Boost", "details": "Drink enough water daily for a week.", "type": "7-Day", "duration": 7, "lvl": "Easy", "xp": 50},
    {"_id": "4", "name": "7-Day Step Goal", "details": "Hit your step goal every day for a week.", "type": "7-Day", "duration": 7, "lvl": "Medium", "xp": 75},
    {"_id": "5", "name": "7-Day Sugar-Free", "details": "Go sugar-free for a week.", "type": "7-Day", "duration": 7, "lvl": "Hard", "xp": 100},
    {"_id": "6", "name": "14-Day Core Strength", "details": "Build core strength over 14 days.", "type": "14-Day", "duration": 14, "lvl": "Medium", "xp": 150},
    {"_id": "7", "name": "14-Day Cardio Blast", "details": "Improve cardio with daily sessions.", "type": "14-Day", "duration": 14, "lvl": "Medium", "xp": 150},
    {"_id": "8", "name": "14-Day Sleep Reset", "details": "Reset your sleep routine in 14 days.", "type": "14-Day", "duration": 14, "lvl": "Easy", "xp": 100},
    {"_id": "9", "name": "14-Day Mindfulness", "details": "Practice mindfulness daily.", "type": "14-Day", "duration": 14, "lvl": "Easy", "xp": 100},
    {"_id": "10", "name": "14-Day Veggie Boost", "details": "Eat more veggies for 14 days.", "type": "14-Day", "duration": 14, "lvl": "Medium", "xp": 150},
    {"_id": "11", "name": "30-Day Full Body Fitness", "details": "A month of full-body workouts.", "type": "30-Day", "duration": 30, "lvl": "Hard", "xp": 300},
    {"_id": "12", "name": "30-Day Yoga Journey", "details": "Daily yoga for a month.", "type": "30-Day", "duration": 30, "lvl": "Medium", "xp": 250},
    {"_id": "13", "name": "30-Day Running Challenge", "details": "Run regularly for 30 days.", "type": "30-Day", "duration": 30, "lvl": "Hard", "xp": 300},
    {"_id": "14", "name": "30-Day Strength Builder", "details": "Build strength over a month.", "type": "30-Day", "duration": 30, "lvl": "Hard", "xp": 300},
    {"_id": "15", "name": "30-Day Healthy Eating", "details": "Eat healthy for 30 days.", "type": "30-Day", "duration": 30, "lvl": "Medium", "xp": 250}
]    

STATIC_CHALLENGE_MAP = {c["_id"]: c for c in predefined_challenges}

meal_plans_bp = Blueprint('meal_plans', __name__)
badges_bp = Blueprint('badges', __name__)
challenges_bp = Blueprint('challenges', __name__)
preferences_bp = Blueprint('preferences', __name__)

@preferences_bp.route('/preferences', methods=['POST'])
@jwt_required()
def set_user_preferences():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    preferences = {
        'user_id': user_id,
        'age_group': data['age_group'],
        'dietary_preference': data['dietary_preference'],
        'fitness_goal': data['fitness_goal'],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    existing_preferences = mongo.db.user_preferences.find_one({'user_id': user_id})
    
    if existing_preferences:
        result = mongo.db.user_preferences.update_one(
            {'user_id': user_id},
            {'$set': {
                'age_group': data['age_group'],
                'dietary_preference': data['dietary_preference'],
                'fitness_goal': data['fitness_goal'],
                'updated_at': datetime.utcnow()
            }}
        )
        preferences['_id'] = str(existing_preferences['_id'])
    else:
        result = mongo.db.user_preferences.insert_one(preferences)
        preferences['_id'] = str(result.inserted_id)
    
    return jsonify({'success': True, 'preferences': preferences}), 201

@preferences_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_user_preferences():
    user_id = get_jwt_identity()
    
    preferences = mongo.db.user_preferences.find_one({'user_id': user_id})
    if not preferences:
        return jsonify({'success': False, 'error': 'Preferences not found'}), 404

    preferences['_id'] = str(preferences['_id'])
    preferences['created_at'] = preferences['created_at'].isoformat()
    preferences['updated_at'] = preferences['updated_at'].isoformat()

    return jsonify({'success': True, 'preferences': preferences}), 200

@preferences_bp.route('/generate-meal-plan', methods=['POST'])
@jwt_required()
def generate_meal_plan():
    user_id = get_jwt_identity()
    
    user_preferences = mongo.db.user_preferences.find_one({'user_id': user_id})
    if not user_preferences:
        return jsonify({'success': False, 'error': 'Please set your preferences first'}), 400
    
    meal_plan = meal_generation_service.generate_meal_plan(
        user_preferences['age_group'],
        user_preferences['dietary_preference'],
        user_preferences['fitness_goal']  
    )
    
    meal_plan_data = {
        'user_id': user_id,
        'date': datetime.utcnow(),
        'breakfast': meal_plan['breakfast'],
        'lunch': meal_plan['lunch'],
        'dinner': meal_plan['dinner'],
        'generated_at': datetime.utcnow()
    }
    
    result = mongo.db.generated_meal_plans.insert_one(meal_plan_data)
    meal_plan_data['_id'] = str(result.inserted_id)
    
    return jsonify({
        'success': True, 
        'meal_plan': meal_plan,
        'saved_plan_id': meal_plan_data['_id']
    }), 201

@preferences_bp.route('/meal-plans/history', methods=['GET'])
@jwt_required()
def get_meal_plan_history():
    user_id = get_jwt_identity()
    
    x = datetime.utcnow() - timedelta(days=7)
    
    meal_plans = list(mongo.db.generated_meal_plans.find({
        'user_id': user_id,
        'generated_at': {'$gte': x}
    }).sort('generated_at', -1))
    
    for plan in meal_plans:
        plan['_id'] = str(plan['_id'])
        plan['date'] = plan['date'].isoformat()
        plan['generated_at'] = plan['generated_at'].isoformat()
    
    return jsonify({'success': True, 'meal_plans': meal_plans}), 200

@preferences_bp.route('/meals/available', methods=['GET'])
@jwt_required()
def get_available_meals():
    user_id = get_jwt_identity()
    
    user_preferences = mongo.db.user_preferences.find_one({'user_id': user_id})
    if not user_preferences:
        return jsonify({'success': False, 'error': 'Please set your preferences first'}), 400
    
    filtered_meals = meal_generation_service.filter_meals_by_preferences(
        user_preferences['age_group'],
        user_preferences['dietary_preference'],
        user_preferences['fitness_goal']
    )
    
    return jsonify({'success': True, 'available_meals': filtered_meals}), 200

@meal_plans_bp.route('/meal-plans', methods=['POST'])
@jwt_required()
def create_meal_plan():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    meal_plan = {
        'user_id': user_id,
        'meal_type': data['meal_type'],
        'meal_name': data['meal_name'],
        'quantity': data['quantity'],
        'date': datetime.strptime(data['date'], '%Y-%m-%d'),
        'created_at': datetime.utcnow()
    }
    
    result = mongo.db.meal_plans.insert_one(meal_plan)
    meal_plan['_id'] = str(result.inserted_id)
    
    return jsonify({'success': True, 'meal_plan': meal_plan}), 201

@meal_plans_bp.route('/meal-plans/<date>', methods=['GET'])
@jwt_required()
def get_meal_plans_by_date(date):
    user_id = get_jwt_identity()
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    meal_plans = list(mongo.db.meal_plans.find({
        'user_id': user_id,
        'date': date_obj
    }))
    
    for plan in meal_plans:
        plan['_id'] = str(plan['_id'])
        plan['date'] = plan['date'].strftime('%Y-%m-%d')
        plan['created_at'] = plan['created_at'].isoformat()
    
    return jsonify({'success': True, 'meal_plans': meal_plans}), 200

@meal_plans_bp.route('/meal-plans/<meal_plan_id>', methods=['PUT'])
@jwt_required()
def update_meal_plan(meal_plan_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    update_data = {
        'meal_name': data['meal_name'],
        'quantity': data['quantity']
    }
    
    result = mongo.db.meal_plans.update_one(
        {'_id': ObjectId(meal_plan_id), 'user_id': user_id},
        {'$set': update_data}
    )
    
    return jsonify({'success': True, 'message': 'Meal plan updated'}), 200

@meal_plans_bp.route('/meal-plans/<meal_plan_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_plan(meal_plan_id):
    user_id = get_jwt_identity()
    
    result = mongo.db.meal_plans.delete_one({
        '_id': ObjectId(meal_plan_id),
        'user_id': user_id
    })
    
    return jsonify({'success': True, 'message': 'Meal plan deleted'}), 200

@badges_bp.route('/badges', methods=['GET'])
@jwt_required()
def get_user_badges():
    user_id = get_jwt_identity()
    
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    badges = user.get('badges', [])
    
    return jsonify({'success': True, 'badges': badges}), 200

@badges_bp.route('/milestones', methods=['GET'])
@jwt_required()
def get_user_milestones():
    user_id = get_jwt_identity()
    
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    milestones = user.get('milestones', [])
    
    return jsonify({'success': True, 'milestones': milestones}), 200

@badges_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_user_progress():
    user_id = get_jwt_identity()
    
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    progress = {
        'level': user.get('level', 1),
        'experience': user.get('experience', 0),
        'badges_count': len(user.get('badges', [])),
        'milestones_count': len(user.get('milestones', []))
    }
    
    return jsonify({'success': True, 'progress': progress}), 200

@challenges_bp.route('/challenges', methods=['GET'])
@jwt_required()
def get_available_challenges():
    user_id = get_jwt_identity()
    user_challenges = list(mongo.db.user_challenges.find({'user_id': user_id}))
    joined_ids = {str(uc['challenge_id']) for uc in user_challenges}
    completed_ids = {str(uc['challenge_id']) for uc in user_challenges if uc.get('completed')}

    challenges_with_status = []
    for ch in predefined_challenges:
        ch_copy = ch.copy()
        ch_copy['joined'] = ch['_id'] in joined_ids
        ch_copy['completed'] = ch['_id'] in completed_ids
        challenges_with_status.append(ch_copy)

    return jsonify({'success': True, 'challenges': challenges_with_status}), 200

@challenges_bp.route('/challenges/<challenge_id>/join', methods=['POST'])
@jwt_required()
def join_challenge(challenge_id):
    user_id = get_jwt_identity()
    
    challenge = STATIC_CHALLENGE_MAP.get(str(challenge_id))
    
    existing_user_challenge = mongo.db.user_challenges.find_one({
        'user_id': user_id,
        'challenge_id': challenge_id
    })
    
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=challenge['duration'])
    
    progress = {}
    for i in range(challenge['duration']):
        day = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        progress[day] = False
    
    user_challenge = {
        'user_id': user_id,
        'challenge_id': challenge_id,
        'start_date': start_date,
        'end_date': end_date,
        'progress': progress,
        'completed': False,
        'created_at': datetime.utcnow()
    }
    
    result = mongo.db.user_challenges.insert_one(user_challenge)
    user_challenge['_id'] = str(result.inserted_id)
    
    return jsonify({'success': True, 'user_challenge': user_challenge}), 201

@challenges_bp.route('/user-challenges', methods=['GET'])
@jwt_required()
def get_user_challenges():
    user_id = get_jwt_identity()
    
    user_challenges = list(mongo.db.user_challenges.find({'user_id': user_id}))
    
    for user_challenge in user_challenges:
        user_challenge['_id'] = str(user_challenge['_id'])
        user_challenge['start_date'] = user_challenge['start_date'].isoformat()
        user_challenge['end_date'] = user_challenge['end_date'].isoformat()
        user_challenge['created_at'] = user_challenge['created_at'].isoformat()
        
        challenge = STATIC_CHALLENGE_MAP.get(str(user_challenge['challenge_id']))
        if challenge:
            user_challenge['challenge_name'] = challenge['name']
            user_challenge['challenge_description'] = challenge['details']
            user_challenge['type'] = challenge['type']
    
    return jsonify({'success': True, 'user_challenges': user_challenges}), 200

@challenges_bp.route('/user-challenges/<user_challenge_id>/complete-day', methods=['POST'])
@jwt_required()
def complete_challenge_day(user_challenge_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    day = data['day']
    
    result = mongo.db.user_challenges.update_one(
        {
            '_id': ObjectId(user_challenge_id),
            'user_id': user_id
        },
        {
            '$set': {f'progress.{day}': True}
        }
    )
    
    user_challenge = mongo.db.user_challenges.find_one({
        '_id': ObjectId(user_challenge_id)
    })
    
    if user_challenge:
        progress = user_challenge['progress']
        all_completed = all(progress.values())
        
        if all_completed:
            mongo.db.user_challenges.update_one(
                {'_id': ObjectId(user_challenge_id)},
                {
                    '$set': {
                        'completed': True,
                        'completed_at': datetime.utcnow()
                    }
                }
            )
            
            ch = STATIC_CHALLENGE_MAP.get(str(user_challenge.get('challenge_id')))
            awarded_xp = ch.get('xp', 100) if ch else 100
            mongo.db.users.update_one(
                {'_id': ObjectId(user_id)},
                {
                    '$inc': {'experience': awarded_xp},
                    '$push': {
                        'badges': {
                            'name': 'Challenge Master',
                            'details': 'Completed a fitness challenge',
                            'icon': '🏆',
                            'category': 'challenge',
                            'awarded_at': datetime.utcnow()
                        }
                    }
                }
            )
            
            user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if user:
                current_level = user.get('level', 1)
                current_exp = user.get('experience', 0)
                required_exp = current_level * 100
                if current_exp >= required_exp:
                    new_level = current_level + 1
                    mongo.db.users.update_one(
                        {'_id': ObjectId(user_id)},
                        {
                            '$set': {'level': new_level},
                            '$push': {
                                'milestones': {
                                    'name': f'Level {new_level}',
                                    'details': f'Reached level {new_level}',
                                    'icon': '⭐',
                                    'category': 'level',
                                    'awarded_at': datetime.utcnow()
                                }
                            }
                        }
                    )
    
    return jsonify({'success': True, 'message': 'Day completed'}), 200