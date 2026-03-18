import nltk
import json
import random
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
def download_nltk_data():
    packages = ['punkt', 'stopwords', 'wordnet', 'punkt_tab']
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

download_nltk_data()

lemmatizer = WordNetLemmatizer()

# ── Intent definitions ────────────────────────────────────────────────────────
INTENTS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening", "howdy", "sup", "what's up"],
        "responses": [
            "Hey! 👋 I'm CollegeBot. Ask me anything about college life!",
            "Hi there! Need help with college stuff? I'm here!",
            "Hello! 😊 What can I help you with today?"
        ]
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "later", "take care", "exit", "quit"],
        "responses": [
            "Goodbye! Good luck with your studies! 📚",
            "See you! Don't forget to revise! ✌️",
            "Take care! Go ace those exams! 🎯"
        ]
    },
    "thanks": {
        "patterns": ["thanks", "thank you", "thx", "appreciate", "helpful"],
        "responses": [
            "You're welcome! 😊",
            "Happy to help! Anything else?",
            "Anytime! That's what I'm here for!"
        ]
    },
    "exam_tips": {
        "patterns": ["exam", "study", "tips", "how to study", "prepare", "revision", "test", "marks", "score"],
        "responses": [
            "📖 Exam Tips:\n  • Use the Pomodoro technique (25 min study + 5 min break)\n  • Make mind maps for complex topics\n  • Practice past papers\n  • Teach concepts to others to solidify understanding\n  • Sleep well before the exam!",
            "🎯 Study Smart:\n  • Space out your revision (spaced repetition)\n  • Focus on weak areas first\n  • Use flashcards for memorization\n  • Stay hydrated and take breaks!"
        ]
    },
    "time_management": {
        "patterns": ["time", "manage", "schedule", "timetable", "deadline", "procrastinate", "busy", "organize"],
        "responses": [
            "⏰ Time Management Tips:\n  • Make a weekly timetable\n  • Use apps like Notion or Google Calendar\n  • Prioritize tasks using the Eisenhower Matrix\n  • Break big tasks into smaller chunks\n  • Set realistic daily goals!",
            "📅 Beat Procrastination:\n  • Start with the 2-minute rule — if it takes <2 mins, do it now\n  • Use a to-do list and check things off\n  • Remove distractions (put your phone away!)\n  • Reward yourself after completing tasks"
        ]
    },
    "career": {
        "patterns": ["career", "job", "internship", "placement", "resume", "interview", "linkedin", "future", "work"],
        "responses": [
            "💼 Career Advice:\n  • Build your resume early (use templates from Canva or Overleaf)\n  • Apply for internships from 2nd year onward\n  • Create a strong LinkedIn profile\n  • Work on side projects and put them on GitHub\n  • Practice mock interviews!",
            "🚀 Getting Placed:\n  • Focus on DSA (Data Structures & Algorithms)\n  • Contribute to open source\n  • Network with alumni on LinkedIn\n  • Attend hackathons and coding contests"
        ]
    },
    "mental_health": {
        "patterns": ["stress", "anxiety", "mental health", "overwhelmed", "burnout", "depressed", "sad", "tired", "pressure"],
        "responses": [
            "💙 It's okay to feel overwhelmed sometimes. Here's what helps:\n  • Talk to a friend or counselor\n  • Take short walks or exercise regularly\n  • Practice deep breathing or meditation\n  • Don't compare yourself to others\n  • Remember: grades don't define your worth!",
            "🌿 Self-care Tips:\n  • Get 7-8 hours of sleep\n  • Eat healthy and stay hydrated\n  • Take breaks — all work and no play leads to burnout\n  • It's okay to ask for help 💪"
        ]
    },
    "notes_resources": {
        "patterns": ["notes", "resources", "books", "material", "pdf", "reference", "where to study", "website"],
        "responses": [
            "📚 Free Study Resources:\n  • Khan Academy — great for fundamentals\n  • MIT OpenCourseWare — free lecture notes\n  • GeeksforGeeks — CS topics\n  • Coursera / edX — free audit options\n  • YouTube — search '[topic] full course'",
            "🔗 Useful Sites:\n  • NPTEL — free Indian university courses\n  • Studocu / SlideShare — peer notes\n  • GitHub — open source code & projects\n  • Stack Overflow — coding doubts"
        ]
    },
    "attendance": {
        "patterns": ["attendance", "bunk", "skip", "absent", "proxy", "percentage", "minimum"],
        "responses": [
            "🎓 Attendance Matters:\n  • Most colleges require 75% minimum attendance\n  • Check your college portal regularly\n  • If you're falling short, talk to your professor early\n  • Medical leaves can sometimes be compensated — check your college policy",
            "⚠️ Don't bunk too much! Low attendance can bar you from exams.\n  Formula: (Classes attended / Total classes) × 100 ≥ 75%"
        ]
    },
    "cgpa_gpa": {
        "patterns": ["cgpa", "gpa", "grade", "pointer", "marks", "percentage", "calculate"],
        "responses": [
            "📊 CGPA Tips:\n  • CGPA = Average of all semester GPAs\n  • Focus on scoring well in internals/assignments — they add up!\n  • Even if one sem was bad, you can recover in the next\n  • Many companies have a 6.5+ or 7+ CGPA cutoff for placements",
            "🧮 Quick Formula:\n  Percentage ≈ CGPA × 9.5 (common approximation)\n  Work consistently each semester rather than cramming at the end!"
        ]
    },
    "project_ideas": {
        "patterns": ["project", "idea", "build", "make", "develop", "mini project", "final year", "python project"],
        "responses": [
            "💡 Project Ideas for Students:\n  • Python: Chatbot, Web Scraper, To-do App, Quiz App\n  • Web Dev: Portfolio site, Blog, E-commerce clone\n  • ML/AI: Sentiment Analyzer, Image Classifier, Recommendation System\n  • App Dev: College Utility App, Attendance Tracker",
            "🛠️ Final Year Project Ideas:\n  • Smart Attendance System (face recognition)\n  • AI-based Resume Screener\n  • Mental Health Chatbot\n  • Campus Lost & Found Portal\n  • Peer Tutoring Platform"
        ]
    },
    "hostel_food": {
        "patterns": ["hostel", "food", "mess", "canteen", "hungry", "eat", "meal"],
        "responses": [
            "🍛 Hostel Life Hacks:\n  • Keep instant noodles, oats and dry snacks stocked\n  • Mess food boring? Try mixing things up with sauces and spices\n  • Find the best canteen deals on campus 😄\n  • Cook simple meals if your hostel allows it — saves money!",
            "🥗 Stay Healthy in Hostel:\n  • Don't skip breakfast!\n  • Eat fruits and drink enough water\n  • Avoid too much junk food — it kills your energy\n  • A healthy body = a sharper mind 🧠"
        ]
    },
    "default": {
        "responses": [
            "Hmm, I'm not sure about that. Try asking about: exams, time management, career, projects, CGPA, resources, or mental health!",
            "I didn't quite get that 🤔 I can help with: study tips, career advice, project ideas, attendance, and more!",
            "Could you rephrase that? I'm best at helping with college-related topics like exams, internships, and student life!"
        ]
    }
}

# ── NLP Processing ────────────────────────────────────────────────────────────
def preprocess(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(t) for t in tokens
              if t not in string.punctuation and t not in stop_words]
    return tokens

def match_intent(user_input):
    tokens = preprocess(user_input)
    best_intent = None
    best_score = 0

    for intent, data in INTENTS.items():
        if intent == "default":
            continue
        patterns = data.get("patterns", [])
        score = 0
        for pattern in patterns:
            pattern_tokens = preprocess(pattern)
            matches = sum(1 for pt in pattern_tokens if pt in tokens)
            score = max(score, matches)
        if score > best_score:
            best_score = score
            best_intent = intent

    # Also do a raw substring match as fallback
    if best_score == 0:
        lower_input = user_input.lower()
        for intent, data in INTENTS.items():
            if intent == "default":
                continue
            for pattern in data.get("patterns", []):
                if pattern in lower_input:
                    return intent
        return "default"

    return best_intent

def get_response(intent):
    responses = INTENTS[intent]["responses"]
    return random.choice(responses)

# ── CLI Interface ─────────────────────────────────────────────────────────────
def print_banner():
    banner = """
╔══════════════════════════════════════════════════════╗
║         🎓  COLLEGE ASSISTANT CHATBOT  🎓            ║
║                                                      ║
║  Ask me about: exams • career • projects • CGPA      ║
║                resources • time management • more!   ║
║                                                      ║
║  Type 'help' for topics  |  Type 'quit' to exit      ║
╚══════════════════════════════════════════════════════╝
"""
    print(banner)

def print_help():
    print("""
📋 I can help you with:
  1. 📖 Exam & Study Tips
  2. ⏰ Time Management
  3. 💼 Career & Internships
  4. 💙 Mental Health & Stress
  5. 📚 Notes & Resources
  6. 🎓 Attendance & CGPA
  7. 💡 Project Ideas
  8. 🍛 Hostel & Food Tips
""")

def chat():
    print_banner()
    print("Bot: Hey! I'm CollegeBot 🤖 How can I help you today?\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! Best of luck! 🎓")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            print("Bot:", get_response("farewell"))
            break

        if user_input.lower() == "help":
            print_help()
            continue

        intent = match_intent(user_input)
        response = get_response(intent)
        print(f"\nBot: {response}\n")

if __name__ == "__main__":
    chat()
