"""
Career Direction Suggestion Module
Provides career recommendations based on strengths
"""

class CareerSuggester:
    def __init__(self):
        # Career mapping based on subject strengths
        self.career_database = {
            'Math': ['Engineering', 'Data Science', 'Actuarial Science', 'Finance', 'Accounting'],
            'Science': ['Medicine', 'Research', 'Biotechnology', 'Environmental Science', 'Pharmacy'],
            'English': ['Journalism', 'Content Writing', 'Law', 'Teaching', 'Publishing'],
            'History': ['Archaeology', 'Museum Curator', 'Teaching', 'Civil Services', 'Law'],
            'Geography': ['Urban Planning', 'Environmental Consultant', 'GIS Specialist', 'Civil Services'],
            'Computer': ['Software Development', 'AI/ML Engineer', 'Cybersecurity', 'Data Science', 'Game Development']
        }
        
        # Combination-based careers
        self.combination_careers = {
            ('Math', 'Computer'): ['Software Engineering', 'Data Science', 'AI/ML', 'Blockchain Development'],
            ('Math', 'Science'): ['Engineering', 'Medical Research', 'Biotechnology', 'Physics Research'],
            ('Science', 'Computer'): ['Bioinformatics', 'Health Informatics', 'Computational Biology'],
            ('English', 'Computer'): ['Technical Writing', 'UX Writing', 'Content Strategy', 'Digital Marketing'],
            ('History', 'English'): ['Journalism', 'Law', 'Civil Services', 'Publishing', 'Education'],
            ('Geography', 'Science'): ['Environmental Science', 'Climate Research', 'Urban Planning']
        }
        
        # Career details
        self.career_details = {
            'Engineering': {
                'description': 'Design, build, and maintain systems, structures, and technologies',
                'growth': 'High demand across multiple sectors',
                'education': 'B.Tech/B.E. in relevant specialization'
            },
            'Data Science': {
                'description': 'Extract insights from data using statistical and ML techniques',
                'growth': 'Extremely high growth potential',
                'education': 'B.Tech/M.Tech in CS/Data Science or related field'
            },
            'Medicine': {
                'description': 'Diagnose, treat, and prevent diseases',
                'growth': 'Consistent demand with good job security',
                'education': 'MBBS followed by specialization'
            },
            'Law': {
                'description': 'Provide legal advice and represent clients',
                'growth': 'Growing field with diverse opportunities',
                'education': 'LLB (3-year or 5-year integrated)'
            },
            'Software Development': {
                'description': 'Design and develop software applications',
                'growth': 'Very high demand globally',
                'education': 'B.Tech/BCA/MCA in Computer Science'
            }
            # Add more as needed
        }
    
    def suggest_careers(self, strong_areas):
        """
        Suggest career paths based on strong subjects
        
        Args:
            strong_areas: list of dicts with subject and marks
            
        Returns:
            list of career recommendations with details
        """
        if not strong_areas:
            return self._get_default_suggestions()
        
        # Get top 2-3 strong subjects
        top_subjects = [area['subject'] for area in strong_areas[:3]]
        
        # Find careers based on individual subjects
        individual_careers = set()
        for subject in top_subjects:
            if subject in self.career_database:
                individual_careers.update(self.career_database[subject])
        
        # Find careers based on subject combinations
        combination_careers = set()
        if len(top_subjects) >= 2:
            for combo_key, careers in self.combination_careers.items():
                if all(subj in top_subjects for subj in combo_key):
                    combination_careers.update(careers)
        
        # Prioritize combination careers
        all_careers = list(combination_careers) + list(individual_careers - combination_careers)
        
        # Get top 5 recommendations with details
        recommendations = []
        for career in all_careers[:5]:
            rec = {
                'career': career,
                'match_score': self._calculate_match_score(career, top_subjects),
                'related_subjects': self._get_related_subjects(career, top_subjects)
            }
            
            # Add details if available
            if career in self.career_details:
                rec.update(self.career_details[career])
            else:
                rec.update({
                    'description': f'Exciting career path in {career}',
                    'growth': 'Good opportunities available',
                    'education': 'Relevant undergraduate/postgraduate degree'
                })
            
            recommendations.append(rec)
        
        return recommendations
    
    def _calculate_match_score(self, career, strong_subjects):
        """Calculate how well career matches with subjects"""
        # Simple scoring: check how many strong subjects relate to this career
        related_count = 0
        for subject, careers in self.career_database.items():
            if career in careers and subject in strong_subjects:
                related_count += 1
        
        # Score out of 100
        max_possible = min(len(strong_subjects), 3)
        score = (related_count / max_possible) * 100 if max_possible > 0 else 50
        
        return round(score, 0)
    
    def _get_related_subjects(self, career, strong_subjects):
        """Get which of the strong subjects relate to this career"""
        related = []
        for subject, careers in self.career_database.items():
            if career in careers and subject in strong_subjects:
                related.append(subject)
        return related
    
    def _get_default_suggestions(self):
        """Default suggestions if no strong areas"""
        return [
            {
                'career': 'General Engineering',
                'description': 'Versatile field with multiple specializations',
                'growth': 'Stable career option',
                'education': 'B.Tech/B.E.',
                'match_score': 50
            },
            {
                'career': 'Business Administration',
                'description': 'Management and business operations',
                'growth': 'Good opportunities in corporate sector',
                'education': 'BBA/MBA',
                'match_score': 50
            }
        ]
    
    def get_subject_career_map(self):
        """Return complete subject-career mapping for reference"""
        return self.career_database