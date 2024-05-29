import requests
from django.core.management.base import BaseCommand
from que_forum.models import Course  # Replace 'your_app' with the actual name of your app

class Command(BaseCommand):
    help = 'Fetch courses from Udemy API and store them in the database'

    def handle(self, *args, **kwargs):
        url = 'https://www.udemy.com/instructor-api/v1/taught-courses/courses/'
        headers = {
            'Authorization': 'Bearer Y1hu9Z9lzvM3WZmjCdoo97huuIlnB4BL'  # Replace with your actual Udemy API access token
        }
        
        while url:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            for course_data in data['results']:
                course_id = course_data['id']
                title = course_data['title']
                description = course_data.get('description', '')  # Assuming description might not be available
                
                # Check if the course already exists
                course, created = Course.objects.update_or_create(
                    udemy_course_id=course_id,
                    defaults={
                        'title': title,
                        'description': description
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Course "{title}" created successfully.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Course "{title}" updated successfully.'))
            
            # Move to the next page, if available
            url = data['next']

        self.stdout.write(self.style.SUCCESS('Finished fetching courses from Udemy API.'))
