from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# Train
model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Cancer - Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))