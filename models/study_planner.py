from datetime import datetime, timedelta

class StudyPlanner:
    def __init__(self):
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.study_hours_per_day = 4  # Total daily study hours
        
    def generate_plan(self, weak_areas, moderate_areas, strong_areas):
        """
        Generate a weekly study plan based on learning gaps
        
        Args:
            weak_areas: list of subjects needing attention
            moderate_areas: list of subjects with moderate gaps
            strong_areas: list of strong subjects
            
        Returns:
            dict with weekly_schedule and daily_breakdown
        """
        # Calculate time allocation
        total_weak = len(weak_areas)
        total_moderate = len(moderate_areas)
        total_strong = len(strong_areas)
        
        # Allocate study time (weighted by severity)
        time_allocation = {}
        
        # Weak areas get 60% of time
        if weak_areas:
            time_per_weak = (self.study_hours_per_day * 0.6) / total_weak
            for area in weak_areas:
                time_allocation[area['subject']] = {
                    'hours_per_day': round(time_per_weak, 1),
                    'priority': 'High',
                    'focus': 'Concept building & practice'
                }
        
        # Moderate areas get 30% of time
        if moderate_areas:
            time_per_moderate = (self.study_hours_per_day * 0.3) / total_moderate
            for area in moderate_areas:
                time_allocation[area['subject']] = {
                    'hours_per_day': round(time_per_moderate, 1),
                    'priority': 'Medium',
                    'focus': 'Regular practice'
                }
        
        # Strong areas get 10% of time (revision)
        if strong_areas:
            time_per_strong = (self.study_hours_per_day * 0.1) / max(total_strong, 1)
            for area in strong_areas[:2]:  # Top 2 strong subjects only
                time_allocation[area['subject']] = {
                    'hours_per_day': round(time_per_strong, 1),
                    'priority': 'Low',
                    'focus': 'Revision & advanced topics'
                }
        
        # Generate weekly schedule
        weekly_schedule = self._create_weekly_schedule(time_allocation)
        
        # Generate daily tips
        daily_tips = self._generate_study_tips(weak_areas)
        
        return {
            'time_allocation': time_allocation,
            'weekly_schedule': weekly_schedule,
            'daily_tips': daily_tips,
            'total_hours_per_week': self.study_hours_per_day * 7
        }
    
    def _create_weekly_schedule(self, time_allocation):
        """Create day-by-day schedule"""
        schedule = {}
        subjects = list(time_allocation.keys())
        
        for i, day in enumerate(self.days):
            daily_subjects = []
            
            # Rotate subjects across the week
            for j, subject in enumerate(subjects):
                if (i + j) % len(self.days) < 4:  # Study each subject 4 days a week
                    daily_subjects.append({
                        'subject': subject,
                        'duration': time_allocation[subject]['hours_per_day'],
                        'focus': time_allocation[subject]['focus']
                    })
            
            schedule[day] = daily_subjects
        
        return schedule
    
    def _generate_study_tips(self, weak_areas):
        """Generate personalized study tips"""
        tips = [
            "Start with the most challenging topics when your mind is fresh",
            "Take 10-minute breaks every hour to maintain focus",
            "Practice previous year questions for weak subjects",
            "Use visual aids and diagrams for better understanding",
            "Teach concepts to others to reinforce your learning"
        ]
        
        if weak_areas:
            top_weak = weak_areas[0]['subject']
            tips.insert(0, f"Prioritize {top_weak} - focus on fundamentals first")
        
        return tips
    
    def get_weekly_summary(self, time_allocation):
        """Get summary of weekly study plan"""
        summary = {
            'high_priority_subjects': [],
            'medium_priority_subjects': [],
            'revision_subjects': []
        }
        
        for subject, details in time_allocation.items():
            if details['priority'] == 'High':
                summary['high_priority_subjects'].append(subject)
            elif details['priority'] == 'Medium':
                summary['medium_priority_subjects'].append(subject)
            else:
                summary['revision_subjects'].append(subject)
        
        return summary