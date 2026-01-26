import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealth.settings')
django.setup()

from mental_health_app.models import Article

# Clear existing articles
Article.objects.all().delete()

# Add sample articles
Article.objects.create(
    title='Understanding Anxiety: Causes and Coping Strategies',
    slug='understanding-anxiety-causes-coping-strategies',
    content='''
    <h2>What is Anxiety?</h2>
    <p>Anxiety is a normal human emotion that everyone experiences from time to time. However, when anxiety becomes excessive, persistent, and interferes with daily life, it may indicate an anxiety disorder.</p>

    <h2>Common Causes of Anxiety</h2>
    <ul>
        <li>Stress from work, school, or relationships</li>
        <li>Traumatic life events</li>
        <li>Genetic predisposition</li>
        <li>Chemical imbalances in the brain</li>
        <li>Medical conditions or medications</li>
    </ul>

    <h2>Effective Coping Strategies</h2>
    <ol>
        <li><strong>Practice deep breathing:</strong> Try the 4-7-8 technique - inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds.</li>
        <li><strong>Regular exercise:</strong> Physical activity releases endorphins that naturally reduce anxiety.</li>
        <li><strong>Mindfulness and meditation:</strong> Apps like Headspace or Calm can help you stay present.</li>
        <li><strong>Healthy sleep habits:</strong> Aim for 7-9 hours of quality sleep per night.</li>
        <li><strong>Limit caffeine and alcohol:</strong> Both can worsen anxiety symptoms.</li>
        <li><strong>Seek professional help:</strong> Therapy and medication can be very effective when needed.</li>
    </ol>

    <p>Remember, seeking help is a sign of strength, not weakness. If anxiety is significantly impacting your life, don't hesitate to consult a mental health professional.</p>
    ''',
    author='Dr. Sarah Johnson',
)

Article.objects.create(
    title='The Importance of Mental Health Days',
    slug='importance-mental-health-days',
    content='''
    <h2>Why Mental Health Days Matter</h2>
    <p>In our fast-paced world, taking time for mental health is often overlooked. Mental health days are crucial for maintaining overall wellbeing and preventing burnout.</p>

    <h2>Benefits of Taking Mental Health Days</h2>
    <ul>
        <li><strong>Reduced stress:</strong> A day off allows you to recharge and reset.</li>
        <li><strong>Improved productivity:</strong> Paradoxically, taking breaks can make you more productive when you return.</li>
        <li><strong>Better physical health:</strong> Mental stress often manifests physically.</li>
        <li><strong>Enhanced creativity:</strong> Time away from routine tasks can spark new ideas.</li>
        <li><strong>Stronger relationships:</strong> Quality time with loved ones improves emotional connections.</li>
    </ul>

    <h2>How to Make the Most of Your Mental Health Day</h2>
    <ol>
        <li><strong>Disconnect from work:</strong> Avoid checking emails or taking calls.</li>
        <li><strong>Engage in enjoyable activities:</strong> Read, walk in nature, or pursue a hobby.</li>
        <li><strong>Practice self-care:</strong> Take a relaxing bath, meditate, or get a massage.</li>
        <li><strong>Spend time with loved ones:</strong> Connect with friends or family.</li>
        <li><strong>Reflect and journal:</strong> Process your thoughts and emotions.</li>
    </ol>

    <p>Mental health days should be guilt-free. Your wellbeing is worth prioritizing, and taking care of yourself allows you to better care for others.</p>
    ''',
    author='Dr. Michael Chen',
)

Article.objects.create(
    title='Building Resilience: Strategies for Emotional Strength',
    slug='building-resilience-strategies-emotional-strength',
    content='''
    <h2>What is Resilience?</h2>
    <p>Resilience is the ability to bounce back from adversity, adapt to challenges, and keep going in the face of difficulties. It's not about avoiding stress, but learning to thrive despite it.</p>

    <h2>Key Components of Resilience</h2>
    <ul>
        <li><strong>Emotional regulation:</strong> Managing your emotions effectively</li>
        <li><strong>Optimism:</strong> Maintaining a positive outlook</li>
        <li><strong>Problem-solving skills:</strong> Finding solutions to challenges</li>
        <li><strong>Social support:</strong> Having a strong network of relationships</li>
        <li><strong>Self-care:</strong> Prioritizing your physical and mental health</li>
    </ul>

    <h2>Practical Strategies to Build Resilience</h2>
    <ol>
        <li><strong>Develop a growth mindset:</strong> View challenges as opportunities for learning.</li>
        <li><strong>Practice gratitude:</strong> Regularly acknowledge what you're thankful for.</li>
        <li><strong>Build strong relationships:</strong> Cultivate supportive friendships and family connections.</li>
        <li><strong>Learn from setbacks:</strong> Analyze what went wrong and how to improve next time.</li>
        <li><strong>Maintain physical health:</strong> Exercise, eat well, and get enough sleep.</li>
        <li><strong>Set realistic goals:</strong> Break large tasks into manageable steps.</li>
        <li><strong>Practice mindfulness:</strong> Stay present and reduce worry about the future.</li>
    </ol>

    <h2>Remember: Resilience Takes Time</h2>
    <p>Building resilience is a lifelong process. Be patient with yourself and celebrate small victories along the way. If you're struggling, consider speaking with a mental health professional who can provide personalized guidance.</p>
    ''',
    author='Dr. Emily Rodriguez',
)

Article.objects.create(
    title='Sleep and Mental Health: The Critical Connection',
    slug='sleep-mental-health-critical-connection',
    content='''
    <h2>The Sleep-Mental Health Link</h2>
    <p>Sleep and mental health are deeply interconnected. Poor sleep can worsen mental health issues, while mental health problems can disrupt sleep patterns. Understanding this relationship is key to improving both.</p>

    <h2>How Sleep Affects Mental Health</h2>
    <ul>
        <li><strong>Mood regulation:</strong> Sleep deprivation increases irritability and emotional reactivity.</li>
        <li><strong>Cognitive function:</strong> Lack of sleep impairs decision-making and concentration.</li>
        <li><strong>Stress response:</strong> Poor sleep heightens the body's stress response.</li>
        <li><strong>Emotional processing:</strong> Sleep helps process emotions and consolidate memories.</li>
    </ul>

    <h2>Mental Health Conditions and Sleep</h2>
    <ul>
        <li><strong>Depression:</strong> Often causes insomnia or oversleeping</li>
        <li><strong>Anxiety:</strong> Can lead to racing thoughts that prevent sleep</li>
        <li><strong>PTSD:</strong> May cause nightmares and sleep disturbances</li>
        <li><strong>Bipolar disorder:</strong> Sleep patterns often fluctuate with mood episodes</li>
    </ul>

    <h2>Tips for Better Sleep</h2>
    <ol>
        <li><strong>Maintain a consistent schedule:</strong> Go to bed and wake up at the same time daily.</li>
        <li><strong>Create a sleep-friendly environment:</strong> Keep your bedroom cool, dark, and quiet.</li>
        <li><strong>Limit screen time:</strong> Avoid screens at least an hour before bed.</li>
        <li><strong>Establish a bedtime routine:</strong> Relaxing activities signal it's time to sleep.</li>
        <li><strong>Watch your diet:</strong> Avoid caffeine and heavy meals close to bedtime.</li>
        <li><strong>Exercise regularly:</strong> But not too close to bedtime.</li>
        <li><strong>Manage stress:</strong> Practice relaxation techniques before bed.</li>
    </ol>

    <p>If sleep problems persist, consult a healthcare provider. They can help identify underlying issues and recommend appropriate treatments.</p>
    ''',
    author='Dr. James Wilson',
)

Article.objects.create(
    title='Mindfulness for Beginners: Getting Started',
    slug='mindfulness-beginners-getting-started',
    content='''
    <h2>What is Mindfulness?</h2>
    <p>Mindfulness is the practice of being fully present and engaged in the current moment, without judgment. It's about paying attention to your thoughts, feelings, and surroundings with acceptance and curiosity.</p>

    <h2>Benefits of Mindfulness Practice</h2>
    <ul>
        <li><strong>Reduced stress and anxiety:</strong> Mindfulness helps calm the mind</li>
        <li><strong>Improved focus:</strong> Better concentration and attention span</li>
        <li><strong>Enhanced emotional regulation:</strong> Better handling of difficult emotions</li>
        <li><strong>Increased self-awareness:</strong> Greater understanding of your thoughts and behaviors</li>
        <li><strong>Better sleep:</strong> Reduced racing thoughts at night</li>
    </ul>

    <h2>Simple Mindfulness Exercises for Beginners</h2>
    <h3>1. Mindful Breathing</h3>
    <p>Sit comfortably and focus on your breath. Notice the sensation of air entering and leaving your nostrils. When your mind wanders, gently bring it back to your breath.</p>

    <h3>2. Body Scan</h3>
    <p>Lie down and systematically focus on different parts of your body, starting from your toes and moving up to your head. Notice any sensations without judgment.</p>

    <h3>3. Mindful Eating</h3>
    <p>Eat a small piece of food slowly, paying attention to its texture, taste, and aroma. Notice how your body feels as you eat.</p>

    <h3>4. Walking Meditation</h3>
    <p>Walk slowly, paying attention to the sensation of your feet touching the ground and the movement of your body.</p>

    <h3>5. Loving-Kindness Meditation</h3>
    <p>Sit quietly and silently repeat phrases like "May I be happy, may I be healthy, may I be at peace" while visualizing yourself and others.</p>

    <h2>Tips for Starting a Mindfulness Practice</h2>
    <ol>
        <li><strong>Start small:</strong> Begin with just 5 minutes a day</li>
        <li><strong>Be consistent:</strong> Practice at the same time each day</li>
        <li><strong>Be patient:</strong> Your mind will wander - that's normal</li>
        <li><strong>Use apps:</strong> Headspace, Calm, or Insight Timer can guide you</li>
        <li><strong>Join a group:</strong> Group practice can provide support and motivation</li>
    </ol>

    <p>Mindfulness is a skill that improves with practice. Be gentle with yourself as you learn, and remember that every moment is an opportunity to begin again.</p>
    ''',
    author='Dr. Lisa Park',
)

print('Sample articles added successfully!')
