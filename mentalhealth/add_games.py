import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealth.settings')
django.setup()

from mental_health_app.models import Game

# Clear existing games
Game.objects.all().delete()

# Add sample games
Game.objects.create(
    name='Breathing Exercise',
    description='A simple breathing game to help you relax.',
    url='/games/breathing/'
)
Game.objects.create(
    name='Puzzle Game',
    description='Solve puzzles to distract your mind.',
    url='/games/puzzle/'
)
Game.objects.create(
    name='Memory Puzzle',
    description='Match pairs of colored tiles to improve memory and focus.',
    url='/games/memory-puzzle/'
)
Game.objects.create(
    name='Meditation Timer',
    description='Guided meditation to reduce stress.',
    url='/games/meditation/'
)

print('Sample games added successfully!')
