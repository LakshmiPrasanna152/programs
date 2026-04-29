import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Dataset
data = {
    "message": [
        "Win a FREE iPhone now! Click here!!!",
        "Hey, are we still on for lunch tomorrow?",
        "URGENT: You've won $1,000,000! Claim now!",
        "Can you send me the meeting notes?",
        "Congratulations! You are selected for a cash prize!",
        "Let's catch up this weekend.",
        "Get cheap meds online, no prescription needed!",
        "I'll be late to the office today.",
        "You have been chosen for a special offer!",
        "What time does the movie start?",
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# 2. Split
X = df["message"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y   # ✅ FIX
)

# 3. TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# 5. Predict
y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:\n",
      classification_report(
          y_test, y_pred,
          target_names=["Ham", "Spam"],
          zero_division=0   # ✅ FIX
      ))

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 6. Test new messages
new_msgs = ["You won a free car!", "See you at 5pm today"]
new_tfidf = vectorizer.transform(new_msgs)
predictions = model.predict(new_tfidf)

for msg, pred in zip(new_msgs, predictions):
    print(f'"{msg}" → {"SPAM 🚨" if pred == 1 else "HAM ✅"}')