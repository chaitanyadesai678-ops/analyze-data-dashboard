
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Data Analysis Dashboard")
st.write("Analyze your dataset using statistics and charts.")

# Load dataset
file_path = Path("cleaned_dataset.csv")

if file_path.exists():
    df = pd.read_csv(file_path)
else:
    uploaded_file = st.file_uploader(
        "Upload your CSV dataset",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info("Please upload a CSV file to begin.")
        st.stop()

    df = pd.read_csv(uploaded_file)

# Check dataset
if df.empty:
    st.error("The dataset is empty.")
    st.stop()

# Dataset overview
st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Total Columns", len(df.columns))
col3.metric("Missing Values", int(df.isna().sum().sum()))

# Display dataset
st.header("Dataset Preview")
st.dataframe(df, use_container_width=True)

# Missing value analysis
st.header("Missing Value Analysis")

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isna().sum().values
})

st.dataframe(missing, use_container_width=True)

# Statistical analysis and visualization
numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

if numeric_columns:
    st.header("Statistical Analysis")

    st.dataframe(
        df[numeric_columns].describe(),
        use_container_width=True
    )

    selected_column = st.selectbox(
        "Select a column to visualize",
        numeric_columns
    )

    chart_type = st.selectbox(
        "Select chart type",
        ["Histogram", "Bar Chart", "Line Chart"]
    )

    fig, ax = plt.subplots(figsize=(9, 4))

    values = df[selected_column].dropna()

    if chart_type == "Histogram":
        ax.hist(values, bins=10)
        ax.set_ylabel("Frequency")

    elif chart_type == "Bar Chart":
        values = values.head(20)
        ax.bar(range(len(values)), values)
        ax.set_xlabel("Record")
        ax.set_ylabel(selected_column)

    else:
        ax.plot(values.reset_index(drop=True))
        ax.set_xlabel("Record")
        ax.set_ylabel(selected_column)

    ax.set_title(f"{chart_type}: {selected_column}")
    st.pyplot(fig)
    plt.close(fig)

else:
    st.warning("No numeric columns found for visualization.")

# Download analyzed dataset
st.header("Download Dataset")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="analyzed_dataset.csv",
    mime="text/csv"
)

st.success("Data analysis completed successfully!")
