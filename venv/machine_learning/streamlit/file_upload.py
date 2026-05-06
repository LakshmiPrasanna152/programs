import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

# Page config
st.set_page_config(page_title="Data Dashboard", layout="wide")

st.title("📊 Interactive Data Dashboard")

# Upload file
uploaded = st.sidebar.file_uploader(
    "Upload file",
    type=["csv", "xlsx"]
)

# Stop if no file
if uploaded is None:
    st.warning("Please upload a file to continue")
    st.stop()

# Load file safely
def load_file(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

df = load_file(uploaded)

# Detect numeric & categorical
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include="object").columns.tolist()

# Sidebar filters
st.sidebar.subheader("Filters")

df_filtered = df.copy()

# Category filter
for col in cat_cols[:3]:
    values = df[col].dropna().unique()
    selected = st.sidebar.multiselect(col, values, default=values)
    df_filtered = df_filtered[df_filtered[col].isin(selected)]

# Numeric filter
for col in num_cols[:2]:
    min_val = float(df[col].min())
    max_val = float(df[col].max())
    val = st.sidebar.slider(col, min_val, max_val, (min_val, max_val))
    df_filtered = df_filtered[(df_filtered[col] >= val[0]) & (df_filtered[col] <= val[1])]

# Chart
st.subheader("📈 Chart")

chart_type = st.selectbox("Select chart", ["Bar", "Line", "Scatter"])

x = st.selectbox("X-axis", df.columns)
y = st.selectbox("Y-axis", num_cols)

if chart_type == "Bar":
    fig = px.bar(df_filtered, x=x, y=y)
elif chart_type == "Line":
    fig = px.line(df_filtered, x=x, y=y)
else:
    fig = px.scatter(df_filtered, x=x, y=y)

st.plotly_chart(fig, use_container_width=True)

# Show data
st.subheader("📋 Data")
st.dataframe(df_filtered)

# Download
st.subheader("⬇️ Download")

csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "data.csv", "text/csv")