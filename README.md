#  College Assistant Chatbot

A rule-based CLI chatbot built with Python and NLTK that helps college students with academics, career, mental health, and campus life — **no API key required!**

---

## 💡 Features

- 🧠 NLP-powered intent matching using NLTK (tokenization, lemmatization, stopword removal)
- 📖 Study & exam tips
- ⏰ Time management advice
- 💼 Career, internship & resume guidance
- 💙 Mental health & stress support
- 📚 Free study resources & websites
- 🎓 Attendance & CGPA help
- 💡 Project ideas for students
- 🍛 Hostel & food tips

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/college-chatbot.git
cd college-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the chatbot
```bash
python chatbot.py
```

---

## 🖥️ Demo

```
╔══════════════════════════════════════════════════════╗
║         🎓  COLLEGE ASSISTANT CHATBOT  🎓            ║
╚══════════════════════════════════════════════════════╝

Bot: Hey! I'm CollegeBot 🤖 How can I help you today?

You: how do i prepare for exams?

Bot: 📖 Exam Tips:
  • Use the Pomodoro technique (25 min study + 5 min break)
  • Make mind maps for complex topics
  • Practice past papers
  • Teach concepts to others to solidify understanding
  • Sleep well before the exam!

You: any project ideas?

Bot: 💡 Project Ideas for Students:
  • Python: Chatbot, Web Scraper, To-do App, Quiz App
  • Web Dev: Portfolio site, Blog, E-commerce clone
  • ML/AI: Sentiment Analyzer, Image Classifier ...
```

---

## 📁 Project Structure

```
college-chatbot/
│
├── chatbot.py          # Main chatbot script
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🛠️ How It Works

1. **Input** — User types a message
2. **Preprocessing** — Text is tokenized, lowercased, stopwords removed, and lemmatized using NLTK
3. **Intent Matching** — Preprocessed tokens are matched against keyword patterns for each intent
4. **Response** — A random response from the matched intent is returned

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `nltk`  | Natural Language Processing (tokenization, lemmatization, stopwords) |

---

## 🔧 Extending the Bot

To add a new topic, add a new intent to the `INTENTS` dictionary in `chatbot.py`:

```python
"your_topic": {
    "patterns": ["keyword1", "keyword2", "phrase to match"],
    "responses": [
        "Your response here!",
        "Another response variant!"
    ]
}
```

---

## 🙋‍♂️ Author

Built with ❤️ for students, by a student.
```
⭐ Star this repo if it helped you!
```
