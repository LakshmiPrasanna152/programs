# Text Classification Example using Naive Bayes on 20 Newsgroups Dataset
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Load dataset (2 categories for simplicity)
categories = ['rec.sport.baseball', 'sci.space']
train = fetch_20newsgroups(subset='train', categories=categories)
test  = fetch_20newsgroups(subset='test',  categories=categories)

# Convert text → numbers
vectorizer = TfidfVectorizer(stop_words='english')
X_train = vectorizer.fit_transform(train.data)
X_test  = vectorizer.transform(test.data)

# Train
model = MultinomialNB()
model.fit(X_train, train.target)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(test.target, y_pred))