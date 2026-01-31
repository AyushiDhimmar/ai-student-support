"""
Learning Gap Analyzer Module
Uses ML to identify student learning gaps
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class LearningGapAnalyzer:
    def __init__(self):
        self.subjects = ['math', 'science', 'english', 'history', 'geography', 'computer']
        self.scaler = StandardScaler()
        
    def analyze_gaps(self, student_marks):
        """
        Analyze student marks and identify learning gaps
        
        Args:
            student_marks: dict with subject names as keys and marks (0-100) as values
            
        Returns:
            dict with weak_areas, strong_areas, and recommendations
        """
        # Convert marks to numpy array
        marks = np.array([student_marks.get(subject, 0) for subject in self.subjects])
        
        # Calculate statistics
        avg_marks = np.mean(marks)
        std_marks = np.std(marks)
        
        # Identify weak and strong areas
        weak_areas = []
        strong_areas = []
        moderate_areas = []
        
        for i, subject in enumerate(self.subjects):
            mark = marks[i]
            gap = avg_marks - mark
            
            if mark < avg_marks - std_marks:  # Critical gap
                severity = "Critical" if mark < 40 else "High"
                weak_areas.append({
                    'subject': subject.title(),
                    'marks': int(mark),
                    'gap': round(gap, 2),
                    'severity': severity
                })
            elif mark < avg_marks:  # Moderate gap
                moderate_areas.append({
                    'subject': subject.title(),
                    'marks': int(mark),
                    'gap': round(gap, 2),
                    'severity': 'Moderate'
                })
            else:  # Strong area
                strong_areas.append({
                    'subject': subject.title(),
                    'marks': int(mark),
                    'advantage': round(mark - avg_marks, 2)
                })
        
        # Sort by severity
        weak_areas.sort(key=lambda x: x['gap'], reverse=True)
        strong_areas.sort(key=lambda x: x['advantage'], reverse=True)
        
        return {
            'average': round(avg_marks, 2),
            'weak_areas': weak_areas,
            'moderate_areas': moderate_areas,
            'strong_areas': strong_areas,
            'overall_performance': self._get_performance_category(avg_marks)
        }
    
    def _get_performance_category(self, avg):
        """Categorize overall performance"""
        if avg >= 80:
            return "Excellent"
        elif avg >= 60:
            return "Good"
        elif avg >= 40:
            return "Average"
        else:
            return "Needs Improvement"
    
    def get_subject_wise_analysis(self, student_marks):
        """Get detailed subject-wise breakdown"""
        analysis = []
        
        for subject in self.subjects:
            mark = student_marks.get(subject, 0)
            
            analysis.append({
                'subject': subject.title(),
                'marks': int(mark),
                'grade': self._get_grade(mark),
                'status': self._get_status(mark)
            })
        
        return analysis
    
    def _get_grade(self, marks):
        """Convert marks to grade"""
        if marks >= 90:
            return "A+"
        elif marks >= 80:
            return "A"
        elif marks >= 70:
            return "B+"
        elif marks >= 60:
            return "B"
        elif marks >= 50:
            return "C"
        elif marks >= 40:
            return "D"
        else:
            return "F"
    
    def _get_status(self, marks):
        """Get status for each subject"""
        if marks >= 70:
            return "Strong"
        elif marks >= 50:
            return "Average"
        else:
            return "Needs Attention"