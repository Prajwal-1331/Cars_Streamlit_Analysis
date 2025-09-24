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

    # Group by Model and take top 10
    top_models = (
        filtered_type.groupby('Model_Type')['MPG_City']
        .sum()
        .nlargest(10)
        .reset_index()
    )
    st.write(top_models)

    fig, ax = plt.subplots(figsize=(8, 5))
    sb.barplot(
        data=top_models,
        x="Model_Type",
        y="MPG_City",
        palette="coolwarm",
        ax=ax
    )
    plt.xticks(rotation=45, ha="right")
    ax.set_xlabel("Model Type")
    ax.set_ylabel("Total City MPG")
    st.pyplot(fig)

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
    ax2.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.axis("equal")  # Equal aspect ratio
    st.pyplot(fig2)

elif chart_choice == "Weight Distribution (KDE)":
    st.subheader("⚖️ Weight Distribution (KDE)")

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sb.kdeplot(filtered_make.Weight, ax=ax3, fill=True, color="purple", alpha=0.5, linewidth=2)
    ax3.set_xlabel("Car Weight")
    ax3.set_ylabel("Density")
    st.pyplot(fig3)

# --- Footer ---
st.markdown("---")
st.markdown("💡 *Tip: Use the sidebar to filter data and switch between visualizations.*")
