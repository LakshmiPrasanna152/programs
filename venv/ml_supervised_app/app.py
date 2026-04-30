import streamlit as st  # type: ignore[import]
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report,
                             r2_score, mean_absolute_error, mean_squared_error)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import plotly.express as px  # type: ignore[import]

st.set_page_config(page_title="ML Supervised Learning Studio", layout="wide")

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
st.sidebar.title("🧠 ML Studio")
tab = st.sidebar.radio("Navigate", ["Data", "Train Model", "Evaluation", "Predict", "Visualize"])

# Dataset selection
dataset_name = st.sidebar.selectbox("Dataset", [
    "Iris", "Breast Cancer", "Wine", "Digits", "Diabetes (Regression)"
])

test_size = st.sidebar.slider("Test size", 0.1, 0.5, 0.2)
random_state = st.sidebar.number_input("Random seed", 0, 999, 42)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data(name):
    mapping = {
        "Iris": datasets.load_iris,
        "Breast Cancer": datasets.load_breast_cancer,
        "Wine": datasets.load_wine,
        "Digits": datasets.load_digits,
        "Diabetes (Regression)": datasets.load_diabetes
    }
    data = mapping[name]()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    task = "regression" if name == "Diabetes (Regression)" else "classification"
    target_names = getattr(data, 'target_names', ['value'])
    return X, y, target_names, task

X, y, target_names, task = load_data(dataset_name)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=int(random_state)
)

# ─── PREPROCESSING ───────────────────────────────────────────────────────────
scale = st.sidebar.checkbox("Feature scaling", True)
apply_pca = st.sidebar.checkbox("Apply PCA", False)
n_components = 2

scaler = StandardScaler()
X_train_p = scaler.fit_transform(X_train) if scale else X_train.values
X_test_p = scaler.transform(X_test) if scale else X_test.values

if apply_pca:
    n_components = st.sidebar.slider("PCA components", 2, min(X.shape[1], 10), 2)
    pca = PCA(n_components=n_components)
    X_train_p = pca.fit_transform(X_train_p)
    X_test_p = pca.transform(X_test_p)

# ─── MODEL SELECTION ─────────────────────────────────────────────────────────
if task == "classification":
    model_name = st.sidebar.selectbox("Model", [
        "KNN", "Logistic Regression", "Decision Tree",
        "Random Forest", "SVM", "Naive Bayes"
    ])
else:
    model_name = st.sidebar.selectbox("Model", [
        "Linear Regression", "Ridge", "Lasso",
        "Decision Tree", "Random Forest"
    ])

# Hyperparameters
def get_model(name, task):
    if name == "KNN":
        k = st.sidebar.slider("K", 1, 20, 5)
        return KNeighborsClassifier(n_neighbors=k)
    elif name == "Logistic Regression":
        C = st.sidebar.slider("C", 0.01, 10.0, 1.0)
        return LogisticRegression(C=C, max_iter=1000)
    elif name == "Decision Tree":
        depth = st.sidebar.slider("Max depth", 1, 20, 5)
        return DecisionTreeClassifier(max_depth=depth) if task == "classification" else DecisionTreeRegressor(max_depth=depth)
    elif name == "Random Forest":
        n = st.sidebar.slider("N estimators", 10, 200, 100, 10)
        depth = st.sidebar.slider("Max depth", 1, 20, 5)
        return RandomForestClassifier(n_estimators=n, max_depth=depth) if task == "classification" else RandomForestRegressor(n_estimators=n, max_depth=depth)
    elif name == "SVM":
        C = st.sidebar.slider("C", 0.01, 10.0, 1.0)
        kernel = st.sidebar.selectbox("Kernel", ["rbf", "linear", "poly"])
        return SVC(C=C, kernel=kernel, probability=True)
    elif name == "Naive Bayes":
        return GaussianNB()
    elif name == "Linear Regression":
        return LinearRegression()
    elif name == "Ridge":
        alpha = st.sidebar.slider("Alpha", 0.01, 10.0, 1.0)
        return Ridge(alpha=alpha)
    elif name == "Lasso":
        alpha = st.sidebar.slider("Alpha", 0.001, 1.0, 0.1)
        return Lasso(alpha=alpha)

model = get_model(model_name, task)

# ─── TRAIN ───────────────────────────────────────────────────────────────────
if st.sidebar.button("🚀 Train Model"):
    with st.spinner("Training..."):
        model.fit(X_train_p, y_train)
        st.session_state['model'] = model
        st.session_state['trained'] = True
        st.success("Model trained!")

# ─── TABS ─────────────────────────────────────────────────────────────────────
if tab == "Data":
    st.title("Dataset Explorer")
    col1, col2, col3 = st.columns(3)
    col1.metric("Samples", X.shape[0])
    col2.metric("Features", X.shape[1])
    col3.metric("Task", task.capitalize())
    st.dataframe(X.head(20))
    st.subheader("Class distribution")
    fig = px.histogram(x=y, color=y.astype(str))
    st.plotly_chart(fig, use_container_width=True)

elif tab == "Train Model":
    st.title("Model Training")
    st.info(f"Selected: **{model_name}** | Task: **{task}**")
    if 'trained' in st.session_state:
        st.success("Model is trained and ready.")

elif tab == "Evaluation":
    st.title("Model Evaluation")
    if 'model' not in st.session_state:
        st.warning("Train a model first.")
    else:
        m = st.session_state['model']
        y_pred = m.predict(X_test_p)
        if task == "classification":
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accuracy", f"{accuracy_score(y_test, y_pred):.3f}")
            col2.metric("Precision", f"{precision_score(y_test, y_pred, average='weighted'):.3f}")
            col3.metric("Recall", f"{recall_score(y_test, y_pred, average='weighted'):.3f}")
            col4.metric("F1", f"{f1_score(y_test, y_pred, average='weighted'):.3f}")
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            fig = px.imshow(cm, text_auto=True, color_continuous_scale='Blues',
                           labels=dict(x="Predicted", y="Actual"))
            st.plotly_chart(fig, use_container_width=True)
            # Classification report
            st.text(classification_report(y_test, y_pred, target_names=target_names.astype(str)))
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("R²", f"{r2_score(y_test, y_pred):.3f}")
            col2.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.3f}")
            col3.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_p, y_train, cv=5)
        st.metric("CV Mean", f"{cv_scores.mean():.3f}", f"±{cv_scores.std():.3f}")
        # Feature importance
        if hasattr(m, 'feature_importances_'):
            names = [f"PC{i+1}" for i in range(X_train_p.shape[1])] if apply_pca else list(X.columns)
            imp_df = pd.DataFrame({'feature': names, 'importance': m.feature_importances_})
            imp_df = imp_df.sort_values('importance', ascending=True)
            fig = px.bar(imp_df, x='importance', y='feature', orientation='h')
            st.plotly_chart(fig, use_container_width=True)

elif tab == "Predict":
    st.title("Make Predictions")
    if 'model' not in st.session_state:
        st.warning("Train a model first.")
    else:
        cols = st.columns(min(4, X.shape[1]))
        vals = []
        for i, feat in enumerate(X.columns):
            with cols[i % 4]:
                v = st.number_input(feat, value=float(X[feat].mean()), format="%.4f")
                vals.append(v)
        if st.button("Predict"):
            inp = np.array([vals])
            if scale: inp = scaler.transform(inp)
            if apply_pca: inp = pca.transform(inp)
            pred = st.session_state['model'].predict(inp)
            if task == "classification" and hasattr(st.session_state['model'], 'predict_proba'):
                proba = st.session_state['model'].predict_proba(inp)[0]
                st.success(f"Prediction: **{target_names[pred[0]]}**")
                prob_df = pd.DataFrame({'class': target_names, 'probability': proba})
                fig = px.bar(prob_df, x='class', y='probability', color='probability', color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success(f"Predicted value: **{pred[0]:.4f}**")

elif tab == "Visualize":
    st.title("Data Visualization")
    viz_type = st.selectbox("Chart", ["Scatter", "Histogram", "Correlation heatmap", "Box plot", "Pair plot"])
    if viz_type == "Scatter":
        fx = st.selectbox("X-axis", X.columns)
        fy = st.selectbox("Y-axis", X.columns, index=1)
        fig = px.scatter(X, x=fx, y=fy, color=y.astype(str))
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "Histogram":
        feat = st.selectbox("Feature", X.columns)
        fig = px.histogram(X, x=feat, color=y.astype(str))
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "Correlation heatmap":
        fig = px.imshow(X.corr(), color_continuous_scale='RdBu', text_auto='.2f')
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "Box plot":
        feat = st.selectbox("Feature", X.columns)
        fig = px.box(X, y=feat, color=y.astype(str))
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "Pair plot":
        st.info("Showing first 4 features")
        fig = px.scatter_matrix(X.iloc[:, :4], color=y.astype(str))
        st.plotly_chart(fig, use_container_width=True)