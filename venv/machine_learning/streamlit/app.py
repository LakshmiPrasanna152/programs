import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import datetime

st.set_page_config(layout="wide")

st.title(" Graphs Dashboard with Streamlit")

# ----------------------
# STEP 1: DATA
# ----------------------
@st.cache_data
def create_data():
    df = pd.DataFrame({
        "Index": range(1, 101),
        "Sales": np.random.randint(50, 500, 100),
        "Profit": np.random.randint(10, 200, 100),
        "Model": np.random.choice(["Model_A", "Model_B", "Model_C"], 100)
    })
    return df

df = create_data()

st.subheader("1️⃣ Sample Data")
st.dataframe(df.head(20))

# ----------------------
# STEP 2: CHART OPTIONS
# ----------------------
st.subheader("2️⃣ Select Chart")

chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter", "Histogram"])

x_col = st.selectbox("X-axis", df.columns)
y_col = st.selectbox("Y-axis", df.select_dtypes(include=np.number).columns)

model_selected = st.selectbox("Select Model", ["All", "Model_A", "Model_B", "Model_C"])

filtered_df = df if model_selected == "All" else df[df["Model"] == model_selected]

# ----------------------
# STEP 3: SHOW CHART
# ----------------------
st.subheader("3️⃣ Chart Output")

if chart_type == "Line":
    fig = px.line(filtered_df, x=x_col, y=y_col, color="Model")
elif chart_type == "Bar":
    fig = px.bar(filtered_df, x=x_col, y=y_col, color="Model")
elif chart_type == "Scatter":
    fig = px.scatter(filtered_df, x=x_col, y=y_col, color="Model")
elif chart_type == "Histogram":
    fig = px.histogram(filtered_df, x=y_col, color="Model")

st.plotly_chart(fig, use_container_width=True)

# ----------------------
# STEP 4: SAVE FILE
# ----------------------
st.subheader("4️⃣ Save Chart as File")

output_folder = "chart_files"
os.makedirs(output_folder, exist_ok=True)

if st.button("Save Chart File"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_tag = model_selected if model_selected != "All" else "AllModels"

    filename = f"{chart_type}_{model_tag}_{x_col}_{y_col}_{timestamp}.html"
    filepath = os.path.join(output_folder, filename)

    fig.write_html(filepath)
    st.success(f"Saved: {filename}")

# ----------------------
# STEP 5: FILE DASHBOARD
# ----------------------
st.subheader("5️⃣ File Dashboard")

files = os.listdir(output_folder) if os.path.exists(output_folder) else []

# MULTI FILTERS
col1, col2 = st.columns(2)

with col1:
    chart_filter = st.multiselect(
        "Filter by Chart Type",
        ["Line", "Bar", "Scatter", "Histogram"],
        default=["Line", "Bar", "Scatter", "Histogram"]
    )

with col2:
    model_filter = st.multiselect(
        "Filter by Model",
        ["Model_A", "Model_B", "Model_C", "AllModels"],
        default=["Model_A", "Model_B", "Model_C", "AllModels"]
    )

keyword = st.text_input("Search file name")

# FILTER LOGIC
filtered_files = []

for f in files:
    if not any(f.startswith(c) for c in chart_filter):
        continue
    if not any(m in f for m in model_filter):
        continue
    if keyword.lower() not in f.lower():
        continue
    filtered_files.append(f)

st.write(f"📁 Total Files: {len(filtered_files)}")

# ----------------------
# STEP 6: PREVIEW
# ----------------------
st.subheader("📂 Preview File")

if filtered_files:
    selected_file = st.selectbox("Select file to preview", filtered_files)

    file_path = os.path.join(output_folder, selected_file)

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=500, scrolling=True)
else:
    st.warning("No files found")

# ----------------------
# FINAL STATUS
# ----------------------
st.success("✅ Complete Flow: Data → Chart → Save → Filter → Preview")