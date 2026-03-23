from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import UserProfile, Assessment, Article, Game
from .forms import AssessmentForm




# -------------------------
# Home Page
# -------------------------
def home(request):
    return render(request, 'home.html')


# -------------------------
# About Page
# -------------------------
def about(request):
    return render(request, 'about.html')


# -------------------------
# Login Choice Page
# -------------------------
def login_choice(request):
    return render(request, 'login_choice.html')


# -------------------------
# Login View
# -------------------------
def login_view(request):

    is_admin = request.path == "/admin_login/"
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

            if is_admin and not user.is_staff:
                messages.error(request, "Invalid admin credentials")
                return render(request, template)

            login(request, user)

            # Check if this is the user's first login for welcome message
            if not is_admin:
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile.is_first_login:
                        # Set session flag for welcome message
                        request.session['show_welcome'] = True
                        # Update the flag to False after first login
                        profile.is_first_login = False
                        profile.save()
                except UserProfile.DoesNotExist:
                    # Create profile if it doesn't exist
                    UserProfile.objects.create(user=user, is_first_login=False)

            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')

        else:
            messages.error(request, "Invalid email or password")

    return render(request, template)


# -------------------------
# Signup View
# -------------------------
def signup_view(request):

    is_admin = request.path == "/admin_signup/"
    template = 'admin_signup.html' if is_admin else 'signup.html'

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = request.POST.get('email')

            if is_admin:
                user.is_staff = True

            user.save()

            # Create UserProfile with is_first_login = True for welcome message
            UserProfile.objects.create(user=user, is_first_login=True)

            messages.success(request, "Account created successfully! Welcome to Students Care!")

            if is_admin:
                return redirect('admin_login')
            else:
                return redirect('user_login')

    else:
        form = UserCreationForm()

    return render(request, template, {'form': form})


# -------------------------
# Student Dashboard
# -------------------------
@login_required
def dashboard(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')

    assessments = Assessment.objects.filter(user=request.user)

    # Check if this is the user's first login (welcome message)
    show_welcome = request.session.pop('show_welcome', False)

    # Get quote of the day (rotating based on day of year)
    import datetime
    quotes = [
        ("Take care of your mind, and your mind will take care of you.", "Anonymous"),
        ("The greatest weapon against stress is our ability to choose one thought over another.", "William James"),
        ("Mental health is not a destination, but a way of life.", "Anonymous"),
        ("You don't have to control your thoughts. You just have to stop letting them control you.", "Dan Millman"),
        ("Almost everything will work again if you unplug it for a few minutes, including you.", "Anne Lamott"),
        ("Self-care is not selfish. You cannot serve from an empty vessel.", "Eleanor Brown"),
        ("There is no health without mental health.", "WHO"),
        ("Recovery is not a race. You don't have to feel guilty if it takes you longer than you thought it would.", "Anonymous"),
    ]
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    quote, quote_author = quotes[day_of_year % len(quotes)]

    return render(request, 'dashboard.html', {
        'assessments': assessments,
        'show_welcome': show_welcome,
        'quote': quote,
        'quote_author': quote_author,
        'today_date': datetime.datetime.now()
    })


# -------------------------
# Admin Dashboard
# -------------------------
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

    return render(request, 'admin_dashboard.html', {
        'users': users,
        'total_users': total_users,
        'total_assessments': total_assessments,
        'low_risk_count': low_risk_count,
        'moderate_risk_count': moderate_risk_count,
        'high_risk_count': high_risk_count,
    })


# -------------------------
# Assessment
# -------------------------
@login_required
def assessment(request):
    
    # Get the current step from the request
    step = request.POST.get('step', '1')
    
    # Initialize form_data from session or POST
    if 'assessment_data' not in request.session:
        request.session['assessment_data'] = {}
    
    form_data = request.session.get('assessment_data', {})
    
    # Update form_data with current POST data
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('q') and key[1:].isdigit():
                form_data[key] = request.POST.get(key)
        
        request.session['assessment_data'] = form_data
        
        # Process based on step
        if step == '1':
            # Move to step 2
            return render(request, 'assessment.html', {
                'step': 2,
                'form_data': form_data
            })
        
        elif step == '2':
            # Move to step 3
            return render(request, 'assessment.html', {
                'step': 3,
                'form_data': form_data
            })
        
        elif step == '3':
            # Calculate scores and save assessment
            responses = form_data
            
            # Calculate stress score (questions 1-5)
            stress_questions = ['q1', 'q2', 'q3', 'q4', 'q5']
            stress_score = sum(int(responses.get(q, 0)) for q in stress_questions)
            
            # Calculate anxiety score (questions 6-10)
            anxiety_questions = ['q6', 'q7', 'q8', 'q9', 'q10']
            anxiety_score = sum(int(responses.get(q, 0)) for q in anxiety_questions)
            
            # Calculate depression score (questions 11-15) - reverse scoring for positive questions
            depression_questions = ['q11', 'q12', 'q13', 'q14', 'q15']
            depression_score = sum(int(responses.get(q, 0)) for q in depression_questions)
            
            # Determine prediction based on total score
            total_score = stress_score + anxiety_score + depression_score
            
            if total_score <= 15:
                prediction = "Low Risk"
            elif total_score <= 30:
                prediction = "Moderate Risk"
            else:
                prediction = "High Risk"
            
            # Save the assessment
            assessment = Assessment.objects.create(
                user=request.user,
                responses=responses,
                stress_score=stress_score,
                anxiety_score=anxiety_score,
                depression_score=depression_score,
                prediction=prediction,
                work_hours=request.POST.get('work_hours'),
                sleep_hours=request.POST.get('sleep_hours')
            )
            
            # Clear session data
            request.session['assessment_data'] = {}
            
            # Calculate scores for display (out of 10)
            scores = {
                'stress': stress_score,
                'anxiety': anxiety_score,
                'depression': depression_score
            }
            
            # Calculate overall score (out of 100)
            overall_score = int((total_score / 60) * 100)
            risk_level = prediction
            
            # Generate recommendations based on scores
            recommendations = {
                'food': [],
                'exercise': []
            }
            
            if stress_score > 2:
                recommendations['food'].extend([
                    'Drink green tea for relaxation',
                    'Eat magnesium-rich foods like nuts and seeds',
                    'Avoid excessive caffeine'
                ])
                recommendations['exercise'].extend([
                    'Take short walks throughout the day',
                    'Try yoga or gentle stretching'
                ])
            
            if anxiety_score > 2:
                recommendations['food'].extend([
                    'Include omega-3 fatty acids in your diet',
                    'Eat complex carbohydrates for steady energy',
                    'Limit sugar intake'
                ])
                recommendations['exercise'].extend([
                    'Practice deep breathing exercises',
                    'Try cardiovascular exercises'
                ])
            
            if depression_score > 2:
                recommendations['food'].extend([
                    'Eat foods rich in vitamin D',
                    'Include B-vitamin rich foods',
                    'Eat regular meals to maintain energy'
                ])
                recommendations['exercise'].extend([
                    'Start with 10-minute walks',
                    'Try dancing or music-based activities'
                ])
            
            messages.success(request, "Assessment submitted successfully")
            
            return render(request, 'assessment.html', {
                'step': 'results',
                'scores': scores,
                'overall_score': overall_score,
                'risk_level': risk_level,
                'recommendations': recommendations if recommendations['food'] or recommendations['exercise'] else None
            })
    
    # Initial GET request - start with step 1
    request.session['assessment_data'] = {}
    return render(request, 'assessment.html', {
        'step': 1,
        'form_data': {}
    })


# -------------------------
# Chatbot Page
# -------------------------
@login_required
def chatbot(request):
    return render(request, 'chatbot.html')

# -------------------------
# Chatbot Response API
# -------------------------
@csrf_exempt
@login_required
# -------------------------
# Chatbot Response (Q&A Based)
# -------------------------
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

def chatbot_response(request):

    if request.method == "POST":
        
        # Handle both form-urlencoded and JSON data
        if request.content_type == 'application/json':
            import json
            try:
                data = json.loads(request.body)
                message = data.get("message", "").lower()
            except:
                message = ""
        else:
            message = request.POST.get("message", "").lower()
        
        print(f"DEBUG: Received message: '{message}'")
        
        if not message:
            return JsonResponse({"error": "No message provided"}, status=400)

        responses = {

            "hello": ("Hello! I'm here to support you. How are you feeling today?", None),
            "hi": ("Hi there! I'm glad you reached out. Tell me what's on your mind.", None),
            "how are you": ("I'm here and ready to listen. How are you feeling today?", None),

            "i feel sad": ("I'm really sorry you're feeling sad. ", "Would you like to talk about what's making you sad?"),
            "i feel lonely": ("Feeling lonely can be hard. ", "Is there someone you'd like to reach out to?"),
            "i feel stressed": ("Stress can be overwhelming. ", "What's been causing you the most stress lately?"),
            "i feel anxious": ("Anxiety is tough. ", "Would you like to try a breathing exercise together?"),
            "i feel depressed": ("I'm sorry you're feeling this way. ", "How long have you been feeling this way?"),
            "i feel angry": ("Anger is natural. ", "Would you like to talk about what's making you angry?"),
            "i feel tired": ("Rest is important. ", "Have you been getting enough sleep?"),

            "exam stress": ("Exam stress is very common. ", "When is your exam? We can make a study plan together."),
            "study stress": ("Break your study sessions into smaller tasks. ", "What's the most challenging subject for you?"),
            "college pressure": ("College pressure can be challenging. ", "Would you like to talk about what's overwhelming you?"),
            "assignment stress": ("Try completing assignments step by step. ", "Do you need help prioritizing your tasks?"),

            "sleep problem": ("Try maintaining a consistent sleep schedule. ", "How many hours of sleep are you getting?"),
            "insomnia": ("Relaxation techniques may help. ", "Would you like me to guide you through some relaxation?"),
            "cant sleep": ("Calming activities before bed can help. ", "What's usually on your mind when you can't sleep?"),

            "overthinking": ("Overthinking can be exhausting. ", "Would writing down your thoughts help?"),
            "panic attack": ("Take slow deep breaths. ", "Focus on 5 things you can see. Can you do that with me?"),
            "fear": ("Fear is natural. ", "What exactly is causing your fear?"),
            "lack of confidence": ("Confidence grows with small successes. ", "What's something small you've accomplished recently?"),

            "motivation": ("Start with small achievable goals. ", "What's one thing you want to achieve this week?"),
            "no motivation": ("Sometimes rest and self-care help. ", "Have you been taking breaks throughout your day?"),
            "procrastination": ("Break tasks into small steps. ", "What's the easiest first step you can take?"),

            "relationship problems": ("Healthy communication is important. ", "Would you like tips on how to communicate better?"),
            "family problems": ("Family conflicts can be hard. ", "Would you like to talk about what's happening?"),
            "friend problems": ("Friendship issues happen. ", "Would you like advice on how to handle this?"),

            "feeling overwhelmed": ("Take things one step at a time. ", "What's the most urgent thing on your list?"),
            "burnout": ("Burnout happens when you're overworked. ", "When was your last break?"),
            "mental health": ("Mental health is important. ", "Would you like information about counseling services?"),

            "self care": ("Self-care can include many things. ", "What's one self-care activity you enjoy?"),
            "exercise": ("Physical activity improves mood. ", "Would you like suggestions for easy exercises?"),
            "meditation": ("Meditation calms the mind. ", "Would you like a quick guided meditation?"),
            "breathing exercise": ("Let's do breathing together. ", "Ready? Breathe in for 4 seconds..."),

            "i feel hopeless": ("You're not alone. ", "Who is someone you trust that you could talk to?"),
            "i feel worthless": ("Your feelings matter. ", "What's one thing you like about yourself?"),
            "i feel nervous": ("Nervousness is common. ", "Would breathing exercises help?"),

            "thank you": ("You're welcome! ", "Is there anything else you'd like to talk about?"),
            "thanks": ("I'm glad I could help. ", "Feel free to talk anytime."),
            "bye": ("Take care! ", "Remember you're stronger than you think."),
            "goodbye": ("Goodbye! ", "I'm here anytime you need support.")
        }

        reply = "I'm here to listen. Could you tell me more about how you're feeling?"
        follow_up = None

        for key in responses:
            if key in message:
                reply, follow_up = responses[key]
                break
        
        # Combine reply with follow-up question if exists
        if follow_up:
            full_response = reply + " " + follow_up
        else:
            full_response = reply

        return JsonResponse({
            "response": full_response
        })

    return JsonResponse({"error": "Invalid request"})


# -------------------------
# Profile
# -------------------------
@login_required
def profile(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    return render(request, 'profile.html', {
        'profile': profile
    })


# -------------------------
# Games
# -------------------------
@login_required
def games(request):
    games_list = Game.objects.all()
    return render(request, 'games.html', {'games': games_list})


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
    return render(request, 'meditation.html')


# -------------------------
# Exercise
# -------------------------
@login_required
def exercise(request):
    return render(request, 'exercise.html')


# -------------------------
# User History (Admin)
# -------------------------
@login_required
def user_history(request, user_id):

    if not request.user.is_staff:
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)

    assessments = Assessment.objects.filter(user=user)

    return render(request, 'user_history.html', {
        'selected_user': user,
        'assessments': assessments
    })


# -------------------------
# Articles
# -------------------------
def articles(request):

    articles = Article.objects.all()

    return render(request, 'articles.html', {
        'articles': articles
    })


def article_detail(request, slug):

    article = get_object_or_404(Article, slug=slug)

    return render(request, 'article_detail.html', {
        'article': article
    })


# -------------------------
# Logout
# -------------------------
def logout_view(request):

    logout(request)

    return redirect('home')