from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email_reminders = models.BooleanField(default=False)
    sms_reminders = models.BooleanField(default=False)
    reminder_time = models.TimeField(null=True, blank=True)  # Preferred time for reminders
    is_first_login = models.BooleanField(default=True)  # Track first-time login for welcome message

    def __str__(self):
        return self.user.username

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    # Individual responses (0-4 scale)
    responses = models.JSONField(default=dict)  # Store all question responses
    stress_score = models.IntegerField()  # 0-20
    anxiety_score = models.IntegerField()  # 0-20
    depression_score = models.IntegerField()  # 0-20
    work_hours = models.IntegerField(null=True, blank=True)  # Hours per day
    sleep_hours = models.IntegerField(null=True, blank=True)  # Hours per night
    prediction = models.CharField(max_length=50)  # e.g., 'Low Risk', 'Moderate Risk', 'High Risk'

    def __str__(self):
        return f"{self.user.username} - {self.date_taken}"

class StressAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    responses = models.JSONField(default=dict)  # Store question responses
    score = models.IntegerField()  # 0-20
    level = models.CharField(max_length=20)  # e.g., 'Low', 'Moderate', 'High'

    def __str__(self):
        return f"{self.user.username} - Stress Assessment - {self.date_taken}"

class AnxietyAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    responses = models.JSONField(default=dict)  # Store question responses
    score = models.IntegerField()  # 0-20
    level = models.CharField(max_length=20)  # e.g., 'Low', 'Moderate', 'High'

    def __str__(self):
        return f"{self.user.username} - Anxiety Assessment - {self.date_taken}"

class DepressionAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    responses = models.JSONField(default=dict)  # Store question responses
    score = models.IntegerField()  # 0-20
    level = models.CharField(max_length=20)  # e.g., 'Low', 'Moderate', 'High'

    def __str__(self):
        return f"{self.user.username} - Depression Assessment - {self.date_taken}"

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()  # Link to the game or embedded code

    def __str__(self):
        return self.name

class MeditationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField()  # Duration in minutes
    date_completed = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # Track if session was completed

    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes} min - {self.date_completed}"

    class Meta:
        ordering = ['-date_completed']

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']
