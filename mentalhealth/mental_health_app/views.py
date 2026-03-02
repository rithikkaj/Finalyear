from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import models
from django.conf import settings
from .models import UserProfile, Assessment, ChatLog, Game, MeditationSession, Article, StressAssessment, AnxietyAssessment, DepressionAssessment
import random
import json
import openai

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

            # ✅ ALL USERS REDIRECT TO ADMIN DASHBOARD
            target_dashboard = 'admin_dashboard'
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
    from django.utils import timezone
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

    return render(request, 'dashboard.html', {
        'assessments': assessments,
        'chart_data': chart_data,
        'recommendations': recommendations,
        'today_date': timezone.now()
    })

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
            result_data = {
                'assessment_type': 'Mental Health',
                'level': risk_level,
                'score': overall_score,
                'ai_analysis': f"Based on your assessment, you are showing {risk_level.lower()} levels of mental health concerns. Your stress score is {stress_score}/10, anxiety score is {anxiety_score}/10, and depression score is {depression_score}/10. {'This indicates a need for immediate professional support.' if risk_level == 'High Risk' else 'Consider incorporating the recommended lifestyle changes and monitoring your symptoms.'}",
                'recommendations': recommendations['food'] + recommendations['exercise']
            }
            return render(request, 'assessment_result.html', {'result': result_data})

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

        message = request.POST['message']
        if not message.strip():
            response = "I didn't receive a message. How can I help you today?"
        else:
            try:
                # Set OpenAI API key
                openai.api_key = settings.OPENAI_API_KEY

                # Get recent chat history for context (last 5 messages)
                recent_logs = ChatLog.objects.filter(user=request.user).order_by('-timestamp')[:5]
                chat_history = []
                for log in reversed(recent_logs):
                    chat_history.append({"role": "user", "content": log.message})
                    chat_history.append({"role": "assistant", "content": log.response})

                # Add current message
                chat_history.append({"role": "user", "content": message})

                # System prompt for mental health support
                system_prompt = """You are a compassionate and supportive mental health assistant for students. Your role is to:
                - Listen actively and empathetically to students' concerns
                - Provide emotional support and validation
                - Offer practical coping strategies and self-care tips
                - Encourage professional help when appropriate
                - Maintain confidentiality and create a safe space
                - Be non-judgmental and supportive
                - Keep responses conversational and natural
                - Avoid giving medical diagnoses or prescribing treatments
                - Suggest resources like counseling services when needed

                Remember: You are not a substitute for professional mental health care. Always encourage seeking help from qualified professionals when appropriate."""

                # Make API call to OpenAI
                response_obj = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *chat_history
                    ],
                    max_tokens=500,
                    temperature=0.7
                )

                response = response_obj.choices[0].message.content.strip()

            except Exception as e:
                # Fallback to basic responses if API fails
                print(f"OpenAI API error: {e}")
                fallback_responses = [
                    "I'm here to listen. What's been on your mind?",
                    "It's okay to feel this way. How can I support you today?",
                    "Take a deep breath. I'm here for you.",
                    "Your feelings are valid. What would you like to talk about?"
                ]
                response = random.choice(fallback_responses)

        # Save to chat log
        ChatLog.objects.create(user=request.user, message=message, response=response)

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
