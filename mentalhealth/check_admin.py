import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealth.settings')
django.setup()

from django.contrib.auth.models import User

def check_admin_users():
    print("Checking admin users in the database...")
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(is_staff=True)

    print(f"\nSuperusers ({superusers.count()}):")
    for user in superusers:
        print(f"  - Username: {user.username}, Email: {user.email}, Active: {user.is_active}")

    print(f"\nStaff users ({staff_users.count()}):")
    for user in staff_users:
        print(f"  - Username: {user.username}, Email: {user.email}, Active: {user.is_active}")

    # Check for user "Rithikka"
    try:
        rithikka = User.objects.get(username='Rithikka')
        print(f"\nUser 'Rithikka' details:")
        print(f"  - Username: {rithikka.username}")
        print(f"  - Email: {rithikka.email}")
        print(f"  - Is superuser: {rithikka.is_superuser}")
        print(f"  - Is staff: {rithikka.is_staff}")
        print(f"  - Is active: {rithikka.is_active}")
        print(f"  - Password hash: {rithikka.password[:20]}...")
    except User.DoesNotExist:
        print("\nUser 'Rithikka' does not exist in the database.")

if __name__ == '__main__':
    check_admin_users()
