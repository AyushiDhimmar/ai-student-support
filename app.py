"""
Main Flask Application
AI Student Support System
"""

from flask import Flask, render_template, request, jsonify
import json
from models.gap_analyzer import LearningGapAnalyzer
from models.study_planner import StudyPlanner
from models.career_suggest import CareerSuggester

app = Flask(__name__)

# Initialize models
gap_analyzer = LearningGapAnalyzer()
study_planner = StudyPlanner()
career_suggester = CareerSuggester()

@app.route('/')
def home():
    """Landing page"""
    return render_template('index.html')

@app.route('/analyze')
def analyze_page():
    """Student data input page"""
    return render_template('input.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_student():
    """
    API endpoint to analyze student data
    Expects JSON with student marks
    """
    try:
        data = request.get_json()
        
        # Extract student information
        student_name = data.get('name', 'Student')
        marks = {
            'math': float(data.get('math', 0)),
            'science': float(data.get('science', 0)),
            'english': float(data.get('english', 0)),
            'history': float(data.get('history', 0)),
            'geography': float(data.get('geography', 0)),
            'computer': float(data.get('computer', 0))
        }
        
        # Validate marks
        for subject, mark in marks.items():
            if mark < 0 or mark > 100:
                return jsonify({
                    'success': False,
                    'error': f'Invalid marks for {subject}. Must be between 0-100.'
                }), 400
        
        # Run analysis
        gap_analysis = gap_analyzer.analyze_gaps(marks)
        subject_analysis = gap_analyzer.get_subject_wise_analysis(marks)
        
        # Generate study plan
        study_plan = study_planner.generate_plan(
            gap_analysis['weak_areas'],
            gap_analysis['moderate_areas'],
            gap_analysis['strong_areas']
        )
        
        # Get career suggestions
        career_suggestions = career_suggester.suggest_careers(gap_analysis['strong_areas'])
        
        # Compile results
        results = {
            'success': True,
            'student_name': student_name,
            'gap_analysis': gap_analysis,
            'subject_analysis': subject_analysis,
            'study_plan': study_plan,
            'career_suggestions': career_suggestions
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/results')
def results_page():
    """Results display page"""
    return render_template('results.html')

@app.route('/api/demo', methods=['GET'])
def demo_data():
    """Get demo student data for testing"""
    demo_marks = {
        'name': 'Demo Student',
        'math': 85,
        'science': 78,
        'english': 92,
        'history': 45,
        'geography': 55,
        'computer': 88
    }
    return jsonify(demo_marks)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)