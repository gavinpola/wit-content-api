#!/usr/bin/env python3
"""
Simple API Server for Railway Deployment
Minimal dependencies to avoid import issues
"""

import json
import time
import random
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError:
    print("Installing Flask dependencies...")
    import subprocess
    subprocess.check_call(["pip", "install", "Flask==2.3.3", "Werkzeug==2.3.7", "Flask-CORS==4.0.0"])
    from flask import Flask, request, jsonify
    from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get port from environment (Railway sets this)
PORT = int(os.environ.get('PORT', 5000))

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "environment": "production",
        "features": ["question_generation", "daily_challenges", "validation", "bulk_processing"]
    })

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    """Generate questions for a specific domain"""
    try:
        data = request.get_json()
        domain = data.get('domain', 'quant')
        count = data.get('count', 10)
        difficulty_range = data.get('difficulty_range', 'intermediate')
        source = data.get('source', 'n8n_workflow')
        
        questions = generate_questions_for_domain(domain, count, difficulty_range, source)
        
        return jsonify({
            "success": True,
            "questions": questions,
            "count": len(questions),
            "domain": domain,
            "difficulty_range": difficulty_range
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-daily-challenge', methods=['POST'])
def generate_daily_challenge():
    """Generate a daily challenge for a specific date"""
    try:
        data = request.get_json()
        target_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        challenge_type = data.get('type', 'auto')
        
        challenge = generate_daily_challenge_for_date(target_date, challenge_type)
        
        return jsonify({
            "success": True,
            "challenge": challenge,
            "date": target_date,
            "type": challenge_type
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-bulk-questions', methods=['POST'])
def generate_bulk_questions():
    """Generate bulk questions for 10k goal"""
    try:
        data = request.get_json()
        domains = data.get('domains', ['quant', 'verbal', 'spatial', 'logic', 'data'])
        questions_per_domain = data.get('questions_per_domain', 100)
        difficulty_distribution = data.get('difficulty_distribution', {
            'basic': 0.3,
            'intermediate': 0.4,
            'advanced': 0.2,
            'expert': 0.1
        })
        
        all_questions = []
        
        for domain in domains:
            for difficulty, percentage in difficulty_distribution.items():
                count = int(questions_per_domain * percentage)
                if count > 0:
                    questions = generate_questions_for_domain(domain, count, difficulty, 'bulk_generation')
                    all_questions.extend(questions)
        
        return jsonify({
            "success": True,
            "questions": all_questions,
            "total_count": len(all_questions),
            "domains": domains,
            "distribution": difficulty_distribution
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-daily-challenges-bulk', methods=['POST'])
def generate_daily_challenges_bulk():
    """Generate 2 years of daily challenges"""
    try:
        data = request.get_json()
        start_date = data.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        days = data.get('days', 730)  # 2 years
        
        challenges = []
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        for i in range(days):
            challenge_date = current_date + timedelta(days=i)
            challenge = generate_daily_challenge_for_date(
                challenge_date.strftime('%Y-%m-%d'), 
                'auto'
            )
            challenges.append(challenge)
        
        return jsonify({
            "success": True,
            "challenges": challenges,
            "total_count": len(challenges),
            "start_date": start_date,
            "end_date": (current_date + timedelta(days=days-1)).strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate_questions():
    """Simple validation endpoint"""
    try:
        data = request.get_json()
        questions_data = data.get('questions', [])
        
        if not questions_data:
            return jsonify({"error": "No questions provided"}), 400
        
        # Simple validation - just check structure
        valid_questions = []
        invalid_questions = []
        
        for question in questions_data:
            # Basic structure validation
            required_fields = ['stem', 'choices', 'answer', 'domain', 'difficulty']
            is_valid = all(field in question for field in required_fields)
            
            if is_valid and len(question.get('choices', [])) == 4:
                valid_questions.append(question)
            else:
                invalid_questions.append(question)
        
        return jsonify({
            "success": True,
            "valid_count": len(valid_questions),
            "invalid_count": len(invalid_questions),
            "total_count": len(questions_data),
            "success_rate": len(valid_questions) / len(questions_data) if questions_data else 0,
            "valid_questions": valid_questions,
            "invalid_questions": invalid_questions
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_questions_for_domain(domain: str, count: int, difficulty_range: str, source: str) -> List[Dict]:
    """Generate questions for a specific domain"""
    questions = []
    
    # Get difficulty range
    difficulty_mapping = {
        'basic': (400, 600),
        'intermediate': (700, 1000),
        'advanced': (1100, 1400),
        'expert': (1500, 2000)
    }
    
    min_diff, max_diff = difficulty_mapping.get(difficulty_range, (700, 1000))
    
    # Sample questions for each domain
    sample_questions = {
        'quant': [
            ("What is 25% of 80?", ["15", "20", "25", "30"], "20", 600),
            ("If a rectangle has length 8 and width 6, what is its area?", ["14", "28", "48", "56"], "48", 700),
            ("What is 15% of 200?", ["20", "25", "30", "35"], "30", 600),
            ("If 3x + 5 = 20, what is x?", ["3", "5", "7", "15"], "5", 800),
            ("What is the square root of 64?", ["6", "7", "8", "9"], "8", 600),
            ("What is 2^5?", ["16", "32", "64", "128"], "32", 700),
            ("If a circle has radius 5, what is its area?", ["25π", "50π", "75π", "100π"], "25π", 900),
            ("What is the slope of the line y = 2x + 3?", ["1", "2", "3", "5"], "2", 800),
            ("What is 1/3 + 1/6?", ["1/2", "1/3", "1/6", "2/9"], "1/2", 700),
            ("If a triangle has angles 30°, 60°, and 90°, what type is it?", ["Equilateral", "Isosceles", "Right", "Obtuse"], "Right", 600),
        ],
        'verbal': [
            ("What is the opposite of 'generous'?", ["kind", "stingy", "friendly", "helpful"], "stingy", 500),
            ("Complete the analogy: Hot is to Cold as Light is to ___", ["Bright", "Dark", "Warm", "Shine"], "Dark", 800),
            ("What is a synonym for 'happy'?", ["sad", "joyful", "angry", "tired"], "joyful", 400),
            ("What is the opposite of 'brave'?", ["strong", "cowardly", "smart", "fast"], "cowardly", 500),
            ("Complete the analogy: Dog is to Puppy as Cat is to ___", ["Kitten", "Baby", "Young", "Small"], "Kitten", 600),
            ("What is a synonym for 'big'?", ["small", "large", "tiny", "little"], "large", 400),
            ("Complete the analogy: Book is to Read as Movie is to ___", ["Watch", "See", "Look", "View"], "Watch", 600),
            ("What is the opposite of 'fast'?", ["quick", "slow", "rapid", "speedy"], "slow", 400),
            ("What is a synonym for 'smart'?", ["dumb", "intelligent", "stupid", "foolish"], "intelligent", 500),
            ("Complete the analogy: Teacher is to Student as Doctor is to ___", ["Nurse", "Patient", "Hospital", "Medicine"], "Patient", 700),
        ],
        'spatial': [
            ("If you face north and turn right twice, which direction are you facing?", ["North", "South", "East", "West"], "South", 600),
            ("You walk 3 blocks east, then 2 blocks north. How far are you from your starting point?", ["3 blocks", "4 blocks", "5 blocks", "6 blocks"], "5 blocks", 1000),
            ("If you turn left from facing west, which direction are you facing?", ["North", "South", "East", "West"], "South", 500),
            ("You walk 4 blocks south, then 3 blocks west. How far are you from your starting point?", ["5 blocks", "6 blocks", "7 blocks", "8 blocks"], "5 blocks", 900),
            ("If you face east and turn right three times, which direction are you facing?", ["North", "South", "East", "West"], "North", 700),
            ("You walk 6 blocks north, then 8 blocks east. How far are you from your starting point?", ["10 blocks", "12 blocks", "14 blocks", "16 blocks"], "10 blocks", 1100),
            ("If you turn right from facing south, which direction are you facing?", ["North", "South", "East", "West"], "West", 500),
            ("You walk 5 blocks west, then 12 blocks north. How far are you from your starting point?", ["13 blocks", "15 blocks", "17 blocks", "19 blocks"], "13 blocks", 1200),
            ("If you face north and turn left twice, which direction are you facing?", ["North", "South", "East", "West"], "South", 600),
            ("You walk 9 blocks east, then 12 blocks south. How far are you from your starting point?", ["15 blocks", "18 blocks", "21 blocks", "24 blocks"], "15 blocks", 1300),
        ],
        'logic': [
            ("Complete the sequence: 2, 4, 8, 16, ___", ["20", "24", "32", "30"], "32", 900),
            ("If all birds can fly and a penguin is a bird, what can be concluded?", ["Penguins can fly", "Penguins cannot fly", "No conclusion can be drawn", "Some birds cannot fly"], "No conclusion can be drawn", 1200),
            ("What comes next: 1, 3, 6, 10, ___", ["12", "15", "16", "18"], "15", 800),
            ("If all students study and John is a student, what can be concluded?", ["John studies", "John does not study", "No conclusion can be drawn", "Some students don't study"], "John studies", 1000),
            ("Complete the sequence: 1, 2, 4, 7, 11, ___", ["14", "15", "16", "17"], "16", 1000),
            ("If all mammals have hair and a whale is a mammal, what can be concluded?", ["Whales have hair", "Whales don't have hair", "No conclusion can be drawn", "Some mammals don't have hair"], "Whales have hair", 900),
            ("What comes next: 3, 6, 12, 24, ___", ["36", "48", "30", "42"], "48", 800),
            ("If all cars have wheels and this is a car, what can be concluded?", ["This has wheels", "This doesn't have wheels", "No conclusion can be drawn", "Some cars don't have wheels"], "This has wheels", 700),
            ("Complete the sequence: 1, 4, 9, 16, ___", ["20", "25", "30", "35"], "25", 900),
            ("If all doctors are smart and Sarah is a doctor, what can be concluded?", ["Sarah is smart", "Sarah is not smart", "No conclusion can be drawn", "Some doctors are not smart"], "Sarah is smart", 800),
        ],
        'data': [
            ("In a survey of 100 people, 60 prefer apples and 40 prefer oranges. What percentage prefer apples?", ["40%", "50%", "60%", "70%"], "60%", 500),
            ("If a company's revenue increased from $1000 to $1200, what was the percentage increase?", ["15%", "20%", "25%", "30%"], "20%", 800),
            ("In a class of 25 students, 15 are boys. What is the ratio of boys to girls?", ["3:2", "2:3", "3:5", "5:3"], "3:2", 700),
            ("If a basketball player scores 20, 25, and 15 points in three games, what was their average?", ["18", "20", "22", "25"], "20", 600),
            ("In a survey of 200 people, 120 own a car and 80 don't. What percentage don't own a car?", ["30%", "35%", "40%", "45%"], "40%", 600),
            ("If a stock price increases from $50 to $60, what is the percentage increase?", ["15%", "20%", "25%", "30%"], "20%", 700),
            ("In a group of 80 people, 32 are women. What percentage are men?", ["40%", "50%", "60%", "70%"], "60%", 600),
            ("If a test has 40 questions and you get 32 correct, what is your percentage score?", ["70%", "75%", "80%", "85%"], "80%", 600),
            ("In a survey of 150 people, 90 support a policy and 60 oppose it. What is the ratio of supporters to opponents?", ["2:1", "3:2", "4:3", "5:3"], "3:2", 700),
            ("If a company's profit increased from $5000 to $7000, what was the percentage increase?", ["30%", "35%", "40%", "45%"], "40%", 800),
        ]
    }
    
    domain_questions = sample_questions.get(domain, [])
    
    # Generate questions by repeating and varying the samples
    for i in range(count):
        if i < len(domain_questions):
            stem, choices, answer, base_difficulty = domain_questions[i]
        else:
            # Create variations of existing questions
            base_question = domain_questions[i % len(domain_questions)]
            stem, choices, answer, base_difficulty = base_question
            
            # Vary the question slightly
            if domain == 'quant':
                # Vary numbers in quantitative questions
                stem = stem.replace("80", str(80 + (i * 5) % 100))
                stem = stem.replace("200", str(200 + (i * 10) % 300))
            elif domain == 'verbal':
                # Vary words in verbal questions
                stem = stem.replace("generous", ["kind", "brave", "honest", "wise"][i % 4])
            elif domain == 'spatial':
                # Vary directions in spatial questions
                stem = stem.replace("north", ["north", "south", "east", "west"][i % 4])
            elif domain == 'logic':
                # Vary sequences in logic questions
                stem = stem.replace("2, 4, 8, 16", f"{2+i}, {4+i}, {8+i}, {16+i}")
            elif domain == 'data':
                # Vary numbers in data questions
                stem = stem.replace("100", str(100 + (i * 20) % 200))
        
        # Adjust difficulty to match requested range
        difficulty = random.randint(min_diff, max_diff)
        
        question = {
            "stem": stem,
            "choices": choices,
            "answer": answer,
            "domain": domain,
            "difficulty": difficulty,
            "explanation": f"Explanation for {stem}",
            "source": source,
            "created_at": datetime.now().isoformat()
        }
        questions.append(question)
    
    return questions

def generate_daily_challenge_for_date(target_date: str, challenge_type: str) -> Dict:
    """Generate a daily challenge for a specific date"""
    
    # Parse the date to determine challenge type
    date_obj = datetime.strptime(target_date, '%Y-%m-%d')
    day_of_year = date_obj.timetuple().tm_yday
    
    challenge_types = [
        'multi_step_quant',
        'cross_domain_logic', 
        'pattern_recognition',
        'data_analysis',
        'spatial_reasoning'
    ]
    
    challenge_type = challenge_types[day_of_year % len(challenge_types)]
    
    # Generate challenge based on type
    if challenge_type == 'multi_step_quant':
        challenge = {
            "stem": "A train leaves Station A at 2:00 PM traveling 60 mph. Another train leaves Station B at 2:30 PM traveling 80 mph toward Station A. If the stations are 200 miles apart, at what time will they meet?",
            "choices": ["3:15 PM", "3:30 PM", "3:45 PM", "4:00 PM"],
            "answer": "3:30 PM",
            "domain": "quant",
            "difficulty": 1800,
            "explanation": "This requires solving: 60(t) + 80(t-0.5) = 200. Solving gives t = 1.5 hours, so they meet at 3:30 PM.",
            "source": "daily_challenge",
            "metadata": {
                "is_daily_challenge": True,
                "challenge_date": target_date,
                "challenge_type": challenge_type
            },
            "created_at": datetime.now().isoformat()
        }
    
    elif challenge_type == 'cross_domain_logic':
        challenge = {
            "stem": "In a game tournament, players are ranked by their scores. Alice has a higher score than Bob, Bob has a higher score than Charlie, and David has a higher score than Alice. If exactly one of these statements is false, who has the highest score?",
            "choices": ["Alice", "Bob", "Charlie", "David"],
            "answer": "David",
            "domain": "logic",
            "difficulty": 1600,
            "explanation": "If David > Alice > Bob > Charlie, then all statements are true. If David > Alice > Charlie > Bob, then 'Bob > Charlie' is false. David must have the highest score.",
            "source": "daily_challenge",
            "metadata": {
                "is_daily_challenge": True,
                "challenge_date": target_date,
                "challenge_type": challenge_type
            },
            "created_at": datetime.now().isoformat()
        }
    
    elif challenge_type == 'pattern_recognition':
        challenge = {
            "stem": "Complete the pattern: 2, 6, 12, 20, 30, 42, ___. What comes next?",
            "choices": ["50", "56", "62", "68"],
            "answer": "56",
            "domain": "logic",
            "difficulty": 1700,
            "explanation": "The pattern adds consecutive even numbers: +4, +6, +8, +10, +12, +14. So 42 + 14 = 56.",
            "source": "daily_challenge",
            "metadata": {
                "is_daily_challenge": True,
                "challenge_date": target_date,
                "challenge_type": challenge_type
            },
            "created_at": datetime.now().isoformat()
        }
    
    elif challenge_type == 'data_analysis':
        challenge = {
            "stem": "A company's revenue for 5 years was: $100K, $120K, $150K, $180K, $220K. If this trend continues, what will the revenue be in year 7?",
            "choices": ["$280K", "$300K", "$320K", "$340K"],
            "answer": "$300K",
            "domain": "data",
            "difficulty": 1600,
            "explanation": "The increases are: +20K, +30K, +30K, +40K. Following the pattern, year 6 would be +50K ($270K), year 7 would be +30K ($300K).",
            "source": "daily_challenge",
            "metadata": {
                "is_daily_challenge": True,
                "challenge_date": target_date,
                "challenge_type": challenge_type
            },
            "created_at": datetime.now().isoformat()
        }
    
    else:  # spatial_reasoning
        challenge = {
            "stem": "You start at point (0,0) and walk 3 units east, then 4 units north, then 3 units west, then 4 units south. How far are you from your starting point?",
            "choices": ["0 units", "2 units", "4 units", "6 units"],
            "answer": "0 units",
            "domain": "spatial",
            "difficulty": 1500,
            "explanation": "You end up back at (0,0): (0,0) → (3,0) → (3,4) → (0,4) → (0,0). So you're 0 units from the start.",
            "source": "daily_challenge",
            "metadata": {
                "is_daily_challenge": True,
                "challenge_date": target_date,
                "challenge_type": challenge_type
            },
            "created_at": datetime.now().isoformat()
        }
    
    return challenge

if __name__ == '__main__':
    print("🚀 Starting Simple Wit Content Generation API Server...")
    print("📡 API Endpoints:")
    print("  GET  /health - Health check")
    print("  POST /generate-questions - Generate domain questions")
    print("  POST /generate-daily-challenge - Generate daily challenge")
    print("  POST /generate-bulk-questions - Generate 10k questions")
    print("  POST /generate-daily-challenges-bulk - Generate 2 years of challenges")
    print("  POST /validate - Validate questions")
    print(f"🌐 Server running on port {PORT}")
    
    app.run(host='0.0.0.0', port=PORT, debug=False) 