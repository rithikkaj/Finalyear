#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealth.settings')
django.setup()

from django.contrib.auth.models import User
from mental_health_app.models import UserProfile

def create_admin():
    # Check if admin already exists
    if User.objects.filter(username='admin').exists():
        print("Admin user 'admin' already exists!")
        return

    # Create admin user
    admin = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )

    # Create UserProfile
    UserProfile.objects.create(user=admin)

    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
    print("Email: admin@example.com")

if __name__ == '__main__':
    create_admin()
