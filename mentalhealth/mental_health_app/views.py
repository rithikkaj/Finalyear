from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import models
from .models import UserProfile, Assessment, ChatLog, Game, MeditationSession, Article, StressAssessment, AnxietyAssessment, DepressionAssessment
import random
import json

def home(request):
    return render(request, 'home.html')

def login_choice(request):
    return render(request, 'login_choice.html')

def signup_choice(request):
    return render(request, 'signup_choice.html')

def login_view(request):
    is_admin = request.GET.get('admin', 'false').lower() == 'true'
    template = 'admin_login.html' if is_admin else 'login.html'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # ❌ Block user trying admin login
            if is_admin and not user.is_staff:
                messages.error(request, 'Invalid admin credentials')
                return render(request, template, {'is_admin': is_admin})

            login(request, user)

            # ✅ ROLE-BASED REDIRECT USING DICTIONARY MAPPING
            # Map user roles to their respective dashboards
            dashboard_redirects = {
                True: 'admin_dashboard',   # Admin users (is_staff=True)
                False: 'dashboard'         # Regular users (is_staff=False)
            }

            # Get the appropriate dashboard based on user role
            target_dashboard = dashboard_redirects.get(user.is_staff, 'dashboard')
            return redirect(target_dashboard)

        else:
            messages.error(request, 'Invalid credentials')

    return render(request, template, {'is_admin': is_admin})


def signup_view(request):
    is_admin = request.GET.get('admin', 'false').lower() == 'true'
    # If accessed directly without admin param, default to user signup
    if not request.GET.get('admin'):
        is_admin = False
    template = 'admin_signup.html' if is_admin else 'signup.html'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if is_admin:
                user.is_staff = True
                user.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('admin_login' if is_admin else 'login')
    else:
        form = UserCreationForm()
    return render(request, template, {'form': form, 'is_admin': is_admin})

def generate_recommendations(assessment):
    """
    Generate personalized food and exercise recommendations based on assessment scores.
    """
    stress = assessment.stress_score
    anxiety = assessment.anxiety_score
    depression = assessment.depression_score
    prediction = assessment.prediction

    # Food recommendations based on conditions
    food_recommendations = []

    if stress > 7:
        food_recommendations.extend([
            "Magnesium-rich foods: Leafy greens, nuts, seeds, and whole grains to help reduce stress.",
            "Complex carbohydrates: Oatmeal, sweet potatoes, and brown rice for sustained energy."
        ])
    elif stress > 4:
        food_recommendations.append("Include foods rich in B vitamins: Eggs, lean meats, and fortified cereals.")

    if anxiety > 7:
        food_recommendations.extend([
            "Omega-3 fatty acids: Fatty fish like salmon, walnuts, and flaxseeds to support brain health.",
            "Probiotics: Yogurt, kefir, and fermented foods for gut-brain connection."
        ])
    elif anxiety > 4:
        food_recommendations.append("Foods high in antioxidants: Berries, dark chocolate, and green tea.")

    if depression > 7:
        food_recommendations.extend([
            "Foods rich in folate: Leafy greens, asparagus, and citrus fruits.",
            "Vitamin D sources: Fatty fish, fortified milk, and sunlight exposure."
        ])
    elif depression > 4:
        food_recommendations.append("Complex carbohydrates and lean proteins for mood stabilization.")

    # General recommendations if scores are low
    if not food_recommendations:
        food_recommendations = [
            "Maintain a balanced diet with plenty of fruits, vegetables, and whole grains.",
            "Stay hydrated and consider herbal teas like chamomile for relaxation."
        ]

    # Exercise recommendations based on conditions and risk level
    exercise_recommendations = []

    if prediction == 'High Risk':
        exercise_recommendations.extend([
            "Start with gentle activities: Short walks (10-15 minutes) or light stretching.",
            "Practice mindfulness: Try guided meditation or deep breathing exercises.",
            "Consider professional guidance: Consult a therapist or doctor before starting intense activities."
        ])
    elif prediction == 'Moderate Risk':
        exercise_recommendations.extend([
            "Moderate aerobic exercise: Brisk walking, swimming, or cycling for 20-30 minutes, 3-4 times per week.",
            "Yoga or tai chi: Gentle movements combined with breathing for stress reduction.",
            "Strength training: Light weights or resistance bands 2-3 times per week."
        ])
    else:  # Low Risk
        exercise_recommendations.extend([
            "Regular cardio: Running, dancing, or team sports for 30-45 minutes most days.",
            "High-intensity interval training (HIIT): Short bursts of intense activity for mood boosting.",
            "Outdoor activities: Hiking, gardening, or nature walks for additional mental health benefits."
        ])

    # Condition-specific exercise recommendations
    if max(stress, anxiety, depression) > 7:
        exercise_recommendations.append("Focus on activities that promote relaxation and endorphin release.")
    elif max(stress, anxiety, depression) > 4:
        exercise_recommendations.append("Incorporate movement breaks throughout your day to manage symptoms.")

    return {
        'food': food_recommendations[:3],  # Limit to top 3 recommendations
        'exercise': exercise_recommendations[:3]
    }

@login_required
def dashboard(request):
    assessments = Assessment.objects.filter(user=request.user).order_by('-date_taken')[:5]
    latest_assessment = assessments.first() if assessments else None
    chart_data = None
    recommendations = None
    if latest_assessment:
        # Prepare data for pie chart: only stress, anxiety, and depression levels
        factors = {
            'Stress': latest_assessment.stress_score,
            'Anxiety': latest_assessment.anxiety_score,
            'Depression': latest_assessment.depression_score,
        }

        chart_data = {
            'labels': list(factors.keys()),
            'data': list(factors.values()),
            'prediction': latest_assessment.prediction
        }

        # Generate personalized recommendations based on assessment
        recommendations = generate_recommendations(latest_assessment)

    return render(request, 'dashboard.html', {'assessments': assessments, 'chart_data': chart_data, 'recommendations': recommendations})

@login_required
def assessment(request):
    # Default to step 1 if no step specified
    step = int(request.GET.get('step', 1))
    form_data = {}

    if request.method == 'POST':
        current_step = int(request.POST.get('step', 1))
        form_data = {k: v for k, v in request.POST.items() if k.startswith('q')}

        if current_step == 1:
            # Move to step 2
            step = 2
        elif current_step == 2:
            # Move to step 3
            step = 3
        elif current_step == 3:
            # Process all responses and show results
            # Collect all responses
            all_responses = {}
            for i in range(1, 16):
                key = f'q{i}'
                all_responses[key] = int(request.POST.get(key, 0))

            # Calculate scores
            stress_score = sum(all_responses[f'q{i}'] for i in range(1, 6))
            anxiety_score = sum(all_responses[f'q{i}'] for i in range(6, 11))
            depression_score = sum(all_responses[f'q{i}'] for i in range(11, 16))

            # Normalize scores to 0-10 scale (since template shows /10)
            stress_score = min(stress_score, 10)
            anxiety_score = min(anxiety_score, 10)
            depression_score = min(depression_score, 10)

            # Determine risk level
            max_score = max(stress_score, anxiety_score, depression_score)
            if max_score <= 3:
                risk_level = 'Low Risk'
            elif max_score <= 7:
                risk_level = 'Moderate Risk'
            else:
                risk_level = 'High Risk'

            # Calculate overall score (average of normalized scores)
            overall_score = int((stress_score + anxiety_score + depression_score) / 3 * 10)

            # Save assessment
            assessment = Assessment.objects.create(
                user=request.user,
                responses=all_responses,
                stress_score=stress_score,
                anxiety_score=anxiety_score,
                depression_score=depression_score,
                prediction=risk_level
            )

            # Generate recommendations
            recommendations = generate_recommendations(assessment)

            # Prepare context for results page
            context = {
                'step': 'results',
                'overall_score': overall_score,
                'risk_level': risk_level,
                'scores': {
                    'stress': stress_score,
                    'anxiety': anxiety_score,
                    'depression': depression_score
                },
                'recommendations': recommendations
            }
            return render(request, 'assessment.html', context)

    # For GET or intermediate steps
    context = {
        'step': step,
        'form_data': form_data
    }
    return render(request, 'assessment.html', context)

@login_required
def chatbot(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Authentication required'}, status=401)
            else:
                return redirect('login')
        message = request.POST['message'].lower()
        # Context-aware chatbot responses
        if 'sleep' in message or 'trouble sleeping' in message:
            response = "Having trouble sleeping is common when stressed. Try establishing a bedtime routine, avoid screens before bed, and consider relaxation techniques like deep breathing. If it persists, talking to a healthcare professional can help."
        elif 'anxious' in message or 'anxiety' in message:
            response = "Anxiety can be overwhelming, but you're not alone. Try grounding techniques like the 5-4-3-2-1 method (name 5 things you see, 4 you can touch, etc.). Consider mindfulness apps or speaking with a therapist for support."
        elif 'lonely' in message or 'alone' in message:
            response = "Feeling lonely is tough, but remember you're not alone. Consider reaching out to friends, joining support groups, or connecting with online communities. Professional counseling can also provide valuable support."
        elif 'stressed' in message or 'stress' in message:
            response = "Stress is a normal response, but managing it is important. Try exercise, meditation, or talking to someone you trust. If it's overwhelming, consider professional help."
        elif 'depressed' in message or 'depression' in message:
            response = "Depression can make everything feel heavy. You're taking a positive step by reaching out. Consider activities that bring joy, regular exercise, and talking to a mental health professional."
        else:
            responses = [
                "I'm here to help. How are you feeling today?",
                "It's okay to feel this way. What can I do to support you?",
                "Take a deep breath. What's on your mind?",
                "I'm listening. What's been on your mind lately?"
            ]
            response = random.choice(responses)
        ChatLog.objects.create(user=request.user, message=request.POST['message'], response=response)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'response': response})
        else:
            return redirect('chatbot')
    chat_logs = ChatLog.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chatbot.html', {'chat_logs': chat_logs})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    assessments = Assessment.objects.filter(user=request.user).order_by('-date_taken')[:10]

    # Prepare assessment history data
    assessment_history = []
    for assessment in assessments:
        # Generate recommendations for each assessment
        recommendations = generate_recommendations(assessment)
        assessment_history.append({
            'assessment_type': 'Mental Health Assessment',
            'created_at': assessment.date_taken,
            'score': assessment.stress_score + assessment.anxiety_score + assessment.depression_score,  # Overall score
            'level': assessment.prediction,
            'recommendations': recommendations['food'][:3] + recommendations['exercise'][:3]  # Combine and limit
        })

    if request.method == 'POST':
        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.email_reminders = 'email_reminders' in request.POST
        profile.sms_reminders = 'sms_reminders' in request.POST
        profile.reminder_time = request.POST.get('reminder_time') or None
        profile.save()
        messages.success(request, 'Profile updated')
    return render(request, 'profile.html', {
        'profile': profile,
        'assessment_history': assessment_history
    })

@login_required
def games(request):
    games = Game.objects.all()
    return render(request, 'games.html', {'games': games})

@login_required
def exercise(request):
    return render(request, 'exercise.html')

@login_required
def breathing(request):
    return render(request, 'breathing.html')

@login_required
def puzzle(request):
    return render(request, 'puzzle.html')

@login_required
def memory_puzzle(request):
    return render(request, 'memory_puzzle.html')

@login_required
def meditation(request):
    # Get user's meditation stats
    sessions = MeditationSession.objects.filter(user=request.user, completed=True)
    total_sessions = sessions.count()
    total_minutes = sessions.aggregate(total=models.Sum('duration_minutes'))['total'] or 0

    # Calculate current streak (consecutive days with completed sessions)
    from django.db.models import Count
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now().date()
    streak = 0
    check_date = today

    while True:
        day_sessions = sessions.filter(date_completed__date=check_date)
        if day_sessions.exists():
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    context = {
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'current_streak': streak,
    }
    return render(request, 'meditation.html', context)

@login_required
def save_meditation_session(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        duration_minutes = data.get('duration_minutes', 0)
        completed = data.get('completed', False)

        MeditationSession.objects.create(
            user=request.user,
            duration_minutes=duration_minutes,
            completed=completed
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    users = User.objects.all().order_by('username')
    total_users = users.count()
    total_assessments = Assessment.objects.count()
    low_risk_count = Assessment.objects.filter(prediction='Low Risk').count()
    moderate_risk_count = Assessment.objects.filter(prediction='Moderate Risk').count()
    high_risk_count = Assessment.objects.filter(prediction='High Risk').count()

    # Prepare data for overall line chart (average scores over time)
    assessments = Assessment.objects.all().order_by('date_taken')
    dates = []
    avg_stress = []
    avg_anxiety = []
    avg_depression = []
    current_date = None
    daily_scores = {'stress': [], 'anxiety': [], 'depression': []}

    for assessment in assessments:
        date_str = assessment.date_taken.strftime('%Y-%m-%d')
        if current_date != date_str:
            if current_date is not None:
                # Calculate averages for previous date
                dates.append(current_date)
                avg_stress.append(sum(daily_scores['stress']) / len(daily_scores['stress']) if daily_scores['stress'] else 0)
                avg_anxiety.append(sum(daily_scores['anxiety']) / len(daily_scores['anxiety']) if daily_scores['anxiety'] else 0)
                avg_depression.append(sum(daily_scores['depression']) / len(daily_scores['depression']) if daily_scores['depression'] else 0)
            current_date = date_str
            daily_scores = {'stress': [], 'anxiety': [], 'depression': []}
        daily_scores['stress'].append(assessment.stress_score)
        daily_scores['anxiety'].append(assessment.anxiety_score)
        daily_scores['depression'].append(assessment.depression_score)

    # Add last date
    if current_date:
        dates.append(current_date)
        avg_stress.append(sum(daily_scores['stress']) / len(daily_scores['stress']) if daily_scores['stress'] else 0)
        avg_anxiety.append(sum(daily_scores['anxiety']) / len(daily_scores['anxiety']) if daily_scores['anxiety'] else 0)
        avg_depression.append(sum(daily_scores['depression']) / len(daily_scores['depression']) if daily_scores['depression'] else 0)

    line_chart_data = {
        'dates': dates,
        'avg_stress': avg_stress,
        'avg_anxiety': avg_anxiety,
        'avg_depression': avg_depression
    }

    # Prepare data for bar chart (risk distribution)
    bar_chart_data = {
        'labels': ['Low Risk', 'Moderate Risk', 'High Risk'],
        'data': [low_risk_count, moderate_risk_count, high_risk_count]
    }

    return render(request, 'admin_dashboard.html', {
        'users': users,
        'total_users': total_users,
        'total_assessments': total_assessments,
        'low_risk_count': low_risk_count,
        'moderate_risk_count': moderate_risk_count,
        'high_risk_count': high_risk_count,
        'line_chart_data': line_chart_data,
        'bar_chart_data': bar_chart_data
    })

@login_required
def user_history(request, user_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    try:
        selected_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('admin_dashboard')
    
    assessments = Assessment.objects.filter(user=selected_user).order_by('date_taken')
    
    # Prepare data for line chart
    chart_data = {
        'dates': [assessment.date_taken.strftime('%Y-%m-%d') for assessment in assessments],
        'stress': [assessment.stress_score for assessment in assessments],
        'anxiety': [assessment.anxiety_score for assessment in assessments],
        'depression': [assessment.depression_score for assessment in assessments],
        'predictions': [assessment.prediction for assessment in assessments]
    }
    
    return render(request, 'user_history.html', {
        'selected_user': selected_user,
        'assessments': assessments,
        'chart_data': json.dumps(chart_data)
    })

def articles(request):
    articles = Article.objects.filter(is_published=True).order_by('-publish_date')
    return render(request, 'articles.html', {'articles': articles})

def article_detail(request, slug):
    article = Article.objects.get(slug=slug, is_published=True)
    return render(request, 'article_detail.html', {'article': article})

def logout_view(request):
    logout(request)
    return redirect('home')
