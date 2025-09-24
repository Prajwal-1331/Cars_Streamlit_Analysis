import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Apply Seaborn theme
sb.set_theme(style="whitegrid")

# Load Data
df = pd.read_csv("CARS.csv")

# Data Cleaning
df = df.fillna(0)
df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('int64')
df.Invoice = df.Invoice.replace('[$,]', '', regex=True).astype('int64')
df = df.drop('Length', axis=1)
df = df.rename(columns={'Model': 'Model_Type'})

# App Title
st.title("🚗 Car Data Explorer Dashboard")

# Show dataset
if st.checkbox("Show Raw Data"):
    st.write(df)

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filters")

make_choice = st.sidebar.selectbox("Select Make Type", df.Make.unique())
filtered_make = df[df.Make == make_choice]

type_choice = st.sidebar.selectbox("Select Car Type", filtered_make.Type.unique())
filtered_type = filtered_make[filtered_make.Type == type_choice]

# --- Visualization Choice ---
chart_choice = st.sidebar.radio(
    "📊 Choose a visualization:",
    ("Top 10 Models by City MPG (Bar)", 
     "Car Type Distribution (Pie)", 
     "Weight Distribution (KDE)")
)

# --- Plots ---
if chart_choice == "Top 10 Models by City MPG (Bar)":
    st.subheader("🌟 Top 10 Models by City MPG")

    top_models = filtered_type.groupby('Model_Type')['MPG_City'].sum().nlargest(10)
    st.write(top_models)

    fig, ax = plt.subplots(figsize=(8, 5))
    sb.barplot(x=filtered_type.Model_Type, y=filtered_type.MPG_City, ax=ax, palette="coolwarm")
    plt.xticks(rotation=90)
    ax.set_xlabel("Model Type")
    ax.set_ylabel("City MPG")
    st.pyplot(fig)

elif chart_choice == "Car Type Distribution (Pie)":
    st.subheader("📊 Distribution of Car Types")

    type_counts = filtered_make.Type.value_counts()  # <- Dynamic with Make filter

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    colors = sb.color_palette("pastel")[0:len(type_counts)]
    ax2.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', colors=color

