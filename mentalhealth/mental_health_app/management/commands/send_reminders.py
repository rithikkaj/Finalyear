from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from mental_health_app.models import UserProfile
import random
import requests

class Command(BaseCommand):
    help = 'Send daily self-care reminders to users who have opted in'

    def handle(self, *args, **options):
        reminders = [
            "Take a break and breathe deeply",
            "Drink a glass of water",
            "Go for a short walk outside",
            "Do a breathing exercise",
            "Smile at yourself in the mirror",
            "Listen to your favorite song",
            "Stretch your body gently",
            "Write down one thing you're grateful for",
            "Call a friend or loved one",
            "Take 5 minutes to meditate",
            "Eat something nutritious",
            "Get some fresh air",
            "Practice positive self-talk",
            "Do something that makes you laugh",
            "Rest your eyes for a moment",
            "Give yourself a compliment",
            "Step away from your screen",
            "Do a quick body scan meditation",
            "Have a healthy snack",
            "Take deep, slow breaths"
        ]

        # Get users who have opted in for reminders
        email_users = UserProfile.objects.filter(email_reminders=True)
        sms_users = UserProfile.objects.filter(sms_reminders=True)

        reminder_message = random.choice(reminders)

        # Send email reminders
        for profile in email_users:
            try:
                send_mail(
                    'Daily Self-Care Reminder',
                    f'Hello {profile.user.first_name or profile.user.username},\n\n{reminder_message}\n\nTake care of yourself today!\n\n- Students Care Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [profile.user.email],
                    fail_silently=False,
                )
                self.stdout.write(f'Sent email reminder to {profile.user.email}')
            except Exception as e:
                self.stderr.write(f'Failed to send email to {profile.user.email}: {e}')

        # Send SMS reminders (using Twilio or similar service)
        for profile in sms_users:
            if profile.phone:
                try:
                    # This is a placeholder for SMS sending
                    # You would integrate with Twilio, AWS SNS, or another SMS service
                    self.send_sms(profile.phone, reminder_message)
                    self.stdout.write(f'Sent SMS reminder to {profile.phone}')
                except Exception as e:
                    self.stderr.write(f'Failed to send SMS to {profile.phone}: {e}')

        self.stdout.write('Daily reminders sent successfully!')

    def send_sms(self, phone_number, message):
        # Placeholder for SMS sending functionality
        # Integrate with your preferred SMS service (Twilio, AWS SNS, etc.)
        # Example with Twilio:
        # from twilio.rest import Client
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(
        #     body=message,
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=phone_number
        # )
        pass
